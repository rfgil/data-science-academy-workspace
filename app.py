import os
import json
import pickle
import joblib
import pandas as pd
from flask import Flask, jsonify, request
from peewee import (
    Model, IntegerField, FloatField, BooleanField, DateTimeField,
    TextField, IntegrityError
)
from playhouse.shortcuts import model_to_dict
from playhouse.db_url import connect


########################################
# Begin database stuff

# the connect function checks if there is a DATABASE_URL env var
# if it exists, it uses it to connect to a remote postgres db
# otherwise, it connects to a local sqlite db stored in predictions.db
DB = connect(os.environ.get('DATABASE_URL') or 'sqlite:///predictions.db')

class Prediction(Model):
    proba = FloatField()
    prediction = BooleanField(null=True)

    observation_id = TextField(unique=True)
    age = TextField()
    date = DateTimeField()
    gender = TextField()
    latitude = FloatField()
    longitude = FloatField()
    legislation = TextField()
    object_of_search = TextField()
    officer_defined_ethnicity = TextField()
    self_defined_ethnicity = TextField()
    station  = TextField()
    type_ = TextField()

    # true_class
    label = BooleanField(null=True)

    class Meta:
        database = DB


DB.create_tables([Prediction], safe=True)

# End database stuff
########################################

########################################
# Unpickle the previously-trained model


with open('columns.json') as fh:
    columns = json.load(fh)

pipeline = joblib.load('pipeline.pickle')

with open('dtypes.pickle', 'rb') as fh:
    dtypes = pickle.load(fh)


# End model un-pickling
########################################


########################################
# Begin webserver stuff

app = Flask(__name__)

def verify(request):
    pass


@app.route('/predict', methods=['POST'])
def predict():
    obs_dict = request.get_json()

    model = verify(obs_dict)

    if not isinstance(prediction, Prediction):
        print(prediction)
        response['error'] = prediction # When an error occurs, it returns the str message
        return jsonify(response)


    # Remove observation_id from input
    _id = obs_dict['observation_id']
    del obs_dict['observation_id']


    #df = pd.DataFrame([obs_dict], columns=columns).astype(dtypes)
    proba = 0.5 # pipeline.predict_proba(df)[0, 1]
    prediction = True if proba > 0.5 else False # Set the appropriate threshold

    # Build response
    response = {
        'observation_id': _id,
        'prediction': prediction,
    }

    # Upddate and save the model
    model.proba = proba
    model.prediction = prediction
    try:
        model.save()
    except IntegrityError:
        print('Observation ID: "{}" already exists'.format(_id))

    return jsonify(response)


@app.route('/update', methods=['POST'])
def update():
    obs = request.get_json()

    if not isinstance(obs['label'], bool):
        return jsonify({'error': 'label is not a boolean'})

    try:
        model = Prediction.get(Prediction.observation_id == obs['observation_id'])

        model.label = obs['label']
        model.save()

        return obs
    except Prediction.DoesNotExist:
        error_msg = 'Observation ID: "{}" does not exist'.format(obs['observation_id'])
        return jsonify({'error': error_msg})


@app.route('/sanity_check', methods=['POST'])
def sanity_check():
    obs = request.get_json()

    try:
        model = Prediction.get(Prediction.observation_id == obs['observation_id'])

        return jsonify(model_to_dict(obs))
    except Prediction.DoesNotExist:
        error_msg = 'Observation ID: "{}" does not exist'.format(obs['observation_id'])
        return jsonify({'error': error_msg})



@app.route('/list-db-contents')
def list_db_contents():
    return jsonify([
        model_to_dict(obs) for obs in Prediction.select()
    ])


# End webserver stuff
########################################

if __name__ == "__main__":
    app.run(debug=True, port=5000)
