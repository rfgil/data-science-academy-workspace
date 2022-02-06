import os
import json
import numpy as np
import dill as pickle
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
    admission_type_code = IntegerField(null=True)
    discharge_disposition_code = IntegerField(null=True)
    admission_source_code = IntegerField(null=True)
    time_in_hospital = IntegerField(null=True)
    payer_code = TextField(null=True)
    medical_specialty = TextField(null=True)
    has_prosthesis = BooleanField(null=True)
    complete_vaccination_status = TextField(null=True)
    num_lab_procedures = IntegerField(null=True)
    num_procedures = IntegerField(null=True)
    num_medications = IntegerField(null=True)
    number_outpatient = IntegerField(null=True)
    number_emergency = IntegerField(null=True)
    number_inpatient = IntegerField(null=True)
    diag_1 = TextField(null=True)
    diag_2 = TextField(null=True)
    diag_3 = TextField(null=True)
    number_diagnoses = IntegerField(null=True)
    blood_type = TextField(null=True)
    hemoglobin_level = FloatField(null=True)
    blood_transfusion = BooleanField(null=True)
    max_glu_serum = TextField(null=True)
    A1Cresult = TextField(null=True)
    diuretics = TextField(null=True)
    insulin = TextField(null=True)
    change = TextField(null=True)
    diabetesMed = TextField(null=True)

    class Meta:
        database = DB


DB.create_tables([MedicalEncounter], safe=True)

# End database stuff
########################################

########################################
# Unpickle the previously-trained model


#with open('columns.json') as fh:
#    columns = json.load(fh)

pipeline = joblib.load('pipeline.pickle')

#with open('dtypes.pickle', 'rb') as fh:
    #dtypes = pickle.load(fh)

ordered_columns = ['admission_id', 'patient_id', 'race', 'gender', 'age', 'weight',
       'admission_type_code', 'discharge_disposition_code',
       'admission_source_code', 'time_in_hospital', 'payer_code',
       'medical_specialty', 'has_prosthesis', 'complete_vaccination_status',
       'num_lab_procedures', 'num_procedures', 'num_medications',
       'number_outpatient', 'number_emergency', 'number_inpatient', 'diag_1',
       'diag_2', 'diag_3', 'number_diagnoses', 'blood_type',
       'hemoglobin_level', 'blood_transfusion', 'max_glu_serum', 'A1Cresult',
       'diuretics', 'insulin', 'change', 'diabetesMed']

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
            error_message = str(e.__context__).partition('\n')[0]
            print("INFO: " + str(e.__context__))

        elif type(e) is IntegrityError:
            # The observation already existis in the database
            error_type = ApiError.DUPLICATED_ADMISSION_ID
            error_message = "The provided admission_id already exists in the database"
            print("INFO: " + str(e.__context__))

        else:
            traceback.print_exc() #traceback.print_exception(type(e), e, e.__traceback__)

    except DoesNotExist as e:
        error_type = ApiError.DOES_NOT_EXIST
        error_message = "The provided admission_id does not exist in the database"
        # traceback.print_exc() #traceback.print_exception(type(e), e, e.__traceback__)

    except:
        # Catch all handler, this should never happen
        print("WARN: A runtime exception occurred")
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
    request_dict = request.get_json()

    obs_dict = request_dict.copy()

    # Remove from the dict all values with the string "NaN"
    for key in request_dict.keys():
        if str(obs_dict[key]).lower() == 'nan':
            obs_dict.pop(key, None)

    # There is no point in continuing if admissoion_id is missing,
    # because we won't be able to collect the true label afterwards
    if obs_dict.get('admission_id', None) == None:
        return (build_error_response(
            "admission_id is missing",
            ApiError.INVALID_REQUEST
        ), 422)

    # For some reason (when using the postgres database)
    # the pewee model does not convert strings to integers when creating the model from a dict
    # Thus, we're creating the item (adding it to the DB) and then accessing it right away to have all the types fixed by the DB
    medical_encounter, api_error, error_response = db_action(lambda: MedicalEncounter.get(id=MedicalEncounter.create(**obs_dict).id))

    if api_error == ApiError.DUPLICATED_ADMISSION_ID:
        # If the medical encounter already exists in the database, discard new data, and return right away
        medical_encounter, api_error, error_response = db_action(lambda: MedicalEncounter.get(admission_id=obs_dict['admission_id']))
        if api_error == None:
            return {"readmitted": is_readmitted(medical_encounter.prediction)}

    if api_error != None:
        # End execution if an error occurred
        return error_response, 422

    try:
        # Convert medical encounter into a pandas dataframe
        df = pd.DataFrame.from_dict([model_to_dict(medical_encounter)])[ordered_columns]
        df = df.replace({None: np.nan}) # The pipeline does not like python's None, replace it with nan
        #df = df.astype(dtypes)

        # Execute pipeline
        proba = pipeline.predict_proba(df)[0, 1]
        prediction = True if proba >= 0.61 else False # THRESHOLD
    except:
        print("WARN: An unexpected error occured evalutating while the model")
        traceback.print_exc()
        return (build_error_response(
            "An unexpected error occured evalutating while the model",
            ApiError.UNKNONW_EXCEPTION
        ), 422)

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
