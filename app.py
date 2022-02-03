import os
import json
import pickle
import joblib
import pandas as pd
from flask import Flask, jsonify, request
from peewee import (
    Model, IntegerField, FloatField, BooleanField, DateTimeField,
    TextField, IntegrityError, DataError, PeeweeException, DoesNotExist
)
from playhouse.shortcuts import (model_to_dict, dict_to_model)
from playhouse.db_url import connect
import traceback
import uuid
from enum import Enum

########################################
# Begin database stuff

# the connect function checks if there is a DATABASE_URL env var
# if it exists, it uses it to connect to a remote postgres db
# otherwise, it connects to a local sqlite db stored in predictions.db
DB = connect(os.environ.get('DATABASE_URL') or 'postgres://postgres:root@localhost:5432/postgres') #'sqlite:///predictions.db')

class MedicalEncounter(Model):
    # Model preditction
    proba = FloatField(null=True)
    prediction = BooleanField(null=True)

    # True label
    true_label = BooleanField(null=True)

    # --- Parameters ---
    # Generates a random UUID (if not provided) to avoid IntegrityError: UNIQUE constraint failed: medicalencounter.admission_id
    admission_id = TextField(unique=True, default=uuid.uuid1)
    patient_id = TextField(null=True)
    race = TextField(null=True)
    gender = TextField(null=True)
    age = TextField(null=True)
    weight = TextField(null=True)
    admission_type_code = FloatField(null=True)
    discharge_disposition_code = FloatField(null=True)
    admission_source_code = FloatField(null=True)
    time_in_hospital = FloatField(null=True)
    payer_code = TextField(null=True)
    medical_specialty = TextField(null=True)
    has_prosthesis = BooleanField(null=True)
    complete_vaccination_status = TextField(null=True)
    num_lab_procedures = FloatField(null=True)
    num_procedures = FloatField(null=True)
    num_medications = FloatField(null=True)
    number_outpatient = FloatField(null=True)
    number_emergency = FloatField(null=True)
    number_inpatient = FloatField(null=True)
    diag_1 = TextField(null=True)
    diag_2 = TextField(null=True)
    diag_3 = TextField(null=True)
    number_diagnoses = FloatField(null=True)
    blood_type = TextField(null=True)
    hemoglobin_level = FloatField(null=True)
    blood_transfusion = BooleanField(null=True)
    max_glu_serum = TextField(null=True)
    A1Cresult = TextField(null=True)
    diuretics = TextField(null=True)
    insulin = TextField(null=True)
    change = TextField(null=True)
    diabetesMed = TextField(null=True)
    readmitted = TextField(null=True)

    class Meta:
        database = DB


DB.create_tables([MedicalEncounter], safe=True)

# End database stuff
########################################

########################################
# Unpickle the previously-trained model


#with open('columns.json') as fh:
#    columns = json.load(fh)

#pipeline = joblib.load('pipeline.pickle')

#with open('dtypes.pickle', 'rb') as fh:
#    dtypes = pickle.load(fh)

ordered_columns = ['admission_id', 'patient_id', 'race', 'gender', 'age', 'weight',
       'admission_type_code', 'discharge_disposition_code',
       'admission_source_code', 'time_in_hospital', 'payer_code',
       'medical_specialty', 'has_prosthesis', 'complete_vaccination_status',
       'num_lab_procedures', 'num_procedures', 'num_medications',
       'number_outpatient', 'number_emergency', 'number_inpatient', 'diag_1',
       'diag_2', 'diag_3', 'number_diagnoses', 'blood_type',
       'hemoglobin_level', 'blood_transfusion', 'max_glu_serum', 'A1Cresult',
       'diuretics', 'insulin', 'change', 'diabetesMed', 'readmitted']

# End model un-pickling
########################################

########################################
# Begin utils

class ApiError(str, Enum):
    INVALID_REQUEST = "Invalid request"
    DUPLICATED_ADMISSION_ID = "Duplicated request"
    UNKNONW_EXCEPTION = "Unknown exception"
    DOES_NOT_EXIST = "Does not exist"


def build_error_response(message, error_type):
    """
    Builds an error response according to the API's schema
    """
    return {
      "detail": [
        {
          "loc": [],
          "msg": message,
          "type": error_type + ""
        }
      ]
    }


def db_action(action):
    """
    Executes a given databse method and handles its exceptions.

    Returns a tupple with:
        when the action is successful:
        * The action response
        * None
        * Empty dict

        when the action results in an exception:
        * None
        * ApiError enum identifier
        * Error response dict
    """
    try:
        return (action(), None, {})
    except PeeweeException as e:
        DB.rollback() # Database exceptions require a rollback

        if type(e) is DataError:
            # One or more fields have the wrong type
            error_type = ApiError.INVALID_REQUEST
            error_message = str(e.__context__) #.partition('\n')[0])
            print(e.__context__)

        elif type(e) is IntegrityError:
            # The observation already existis in the database
            error_type = ApiError.DUPLICATED_ADMISSION_ID
            error_message = "The provided admission_id already exists in the database"
            print(e.__context__)

        else:
            traceback.print_exc() #traceback.print_exception(type(e), e, e.__traceback__)

    except DoesNotExist as e:
        error_type = ApiError.DOES_NOT_EXIST
        error_message = "The provided admission_id does not exist in the database"
        traceback.print_exc() #traceback.print_exception(type(e), e, e.__traceback__)

    except:
        # Catch all handler, this should never happen
        traceback.print_exc()

        error_type = ApiError.UNKNONW_EXCEPTION
        error_message = "A runtime exception occurred"

    return (None, error_type, build_error_response(error_message, error_type))


def is_readmitted(is_readmitted):
    return "Yes" if is_readmitted else "No"

# End utils
########################################

########################################
# Begin webserver stuff

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    obs_dict = request.get_json()

    medical_encounter, api_error, error_response = db_action(lambda: MedicalEncounter.create(**obs_dict))

    if api_error == ApiError.DUPLICATED_ADMISSION_ID:
        # If the medical encounter already exists in the database, discard new data, and return right away
        medical_encounter, api_error, error_response = db_action(lambda: MedicalEncounter.get(admission_id=obs_dict['admission_id']))
        if api_error == None:
            return {"readmitted": is_readmitted(medical_encounter.prediction)}

    if api_error != None:
        # End execution if an error occurred
        return error_response, 422

    # Convert medical encounter into a pandas dataframe
    df = pd.DataFrame.from_dict([model_to_dict(medical_encounter)])[ordered_columns]

    # Execute pipeline
    proba = 1 #pipeline.predict_proba(df_clean)[0, 1]
    prediction = True if proba >= 0.5 else False

    # Update the model
    medical_encounter.proba = proba
    medical_encounter.prediction = prediction
    _, api_error, error_response = db_action(lambda: medical_encounter.save())


    if api_error != None:
        return error_response, 422
    else:
        return {"readmitted": is_readmitted(prediction)}


@app.route('/update', methods=['POST'])
def update():
    obs_dict = request.get_json()

    admission_id = obs_dict.get('admission_id')
    true_label = obs_dict.get('readmitted')

    if admission_id == None or true_label == None:
        return build_error_response("Required arguments are not available", ApiError.INVALID_REQUEST), 422

    medical_encounter, api_error, error_response = db_action(lambda: MedicalEncounter.get(admission_id=admission_id))

    #if api_error == ApiError.DOES_NOT_EXIST:
    #    medical_encounter, api_error, error_response = db_action(lambda: MedicalEncounter.create(**obs_dict))

    if api_error != None:
        return error_response, 422

    medical_encounter.true_label = (str(true_label).lower() == "yes")

    _, api_error, error_response = db_action(lambda: medical_encounter.save())


    if api_error != None:
        return error_response, 422
    else:
        return {
            "admission_id": medical_encounter.admission_id,
            "actual_readmitted": is_readmitted(medical_encounter.true_label),
            "predicted_readmitted": is_readmitted(medical_encounter.prediction)
        }


@app.route('/list-db-contents')
def list_db_contents():
    return jsonify([
        model_to_dict(obs) for obs in MedicalEncounter.select()
    ])


# End webserver stuff
########################################

if __name__ == "__main__":
    app.run(debug=True, port=5000)
