import os
import json
import pickle
import joblib
import pandas as pd
from flask import Flask, jsonify, request
from peewee import (
    Model, IntegerField, FloatField,
    TextField, IntegrityError
)
from playhouse.shortcuts import model_to_dict
from playhouse.db_url import connect

########################################
# Begin webserver stuff

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    json_request = request.get_json()
    # YOUR CODE HERE
    response = {}

    try:
        response["observation_id"] = json_request["observation_id"]
    except:
        response["observation_id"] = None
        response["error"] = "Unavailable observation_id"
        return response

    # Retrieve json_request columns from 'data'
    try:
        json_request_columns = list(json_request["data"].keys())
    except:
        response["error"] = "data does not exist"
        return response


    # Check all json_requested columns are valid
    valid_columns = ["age", "sex", "race", "workclass", "education", "marital-status", "capital-gain", "capital-loss", "hours-per-week"]
    for column in json_request_columns:
        if (column != "observation_id" and
            column != "probability" and
            column != "prediction" and
            column not in valid_columns):
            response["error"] = column + " is not a valid column"
            return response

    # Check if there are missing columns
    for column in valid_columns:
        if(column not in json_request_columns):
            response["error"] = column + " column is missing"
            return response

    # Check if 'sex' column matches expected input
    if json_request["data"]["sex"].lower() not in ['male', 'female'] :
        response["error"] = "Unexpected " + json_request["data"]["sex"] + " category on 'sex' column"
        return response

    # Check if 'race' column matches expected input
    if json_request["data"]["race"].lower() not in ['white', 'black', 'asian-pac-islander', 'amer-indian-eskimo', 'other']:
        response["error"] = "Unexpected " + json_request["data"]["race"] + " category on 'race' column"
        return response

    # Check if 'age' column matches expected input
    age = int(json_request["data"]["age"])
    if age < 0 or age > 100:
        response["error"] = "Unexpected 'age' of " + str(age) + " years old"
        return response

    # Check if 'capital-gain' column matches expected input
    capital_gains = float(json_request["data"]["capital-gain"])
    if capital_gains < 0: # or capital_gains > 99999:
        response["error"] = "Column 'capital-gain' of " + str(capital_gains) + " exceed bounds."
        return response

    # Check if 'capital-loss' column matches expected input
    capital_loss = float(json_request["data"]["capital-loss"])
    if capital_loss < 0:# or capital_loss > 4356:
        response["error"] = "Column 'capital-loss' of " + str(capital_loss) + " exceed bounds."
        return response

    # Check if 'hours-per-week' column matches expected input
    hours_per_week = int(json_request["data"]["hours-per-week"])
    if hours_per_week < 0 or hours_per_week > 168:
        response["error"] = "Column 'hours-per-week' of " + str(hours_per_week) + " exceed bounds."
        return response

    # predict_response = predict(json_request)
    response["prediction"] = True #predict_response["prediction"]
    response["probability"] = float(1) #predict_response["probability"]

    return response

# End webserver stuff
########################################

if __name__ == "__main__":
    app.run(debug=True, port=5000)
