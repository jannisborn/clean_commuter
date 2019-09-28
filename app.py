from flask import Flask
from flask import jsonify, request
import numpy as np
import json
from compute_scores import compute_score
from backend import get_directions, get_autocomplete

app = Flask(__name__)


@app.route('/query_directions', methods=['GET'])  # api/get_messages
def query_directions():
    weight_str = str(request.args.get('weights'))
    weighting = [int(i) for i in weight_str.split(",")]
    print("WEIGHTS", weighting)

    # TODO: convert coordinates to the correct input for get_directions
    # coordinates = str(request.args.get('dest_coordinates'))
    # googlemapsdic = get_directions(coordinates)
    # print(googlemapsdic)
    # so far: hard coded duration and distances dictionary
    googlemapsdic = {
        "car": {
            "duration": 5,
            "distance": 1000
        },
        "walk": {
            "duration": 10,
            "distance": 1100
        },
        "bike": {
            "duration": 3,
            "distance": 700
        }
    }

    # TODO:
    # - convert from string to whatever you need
    # - import your python file and call your function (taking coordinates as parameters and returning googlemapsdic)
    # I am using googlemapsdic then later for calling my function compute_scores (at the moment hard coded below)

    ## Ninas part:
    # Load metadata from json file
    with open("metadata.json", "r") as infile:
        dic = json.load(infile)

    # Compute scores from google maps data
    out_dic = compute_score(dic, googlemapsdic, weights=weighting)
    return jsonify(out_dic)  # return json file


@app.route('/query_autocomplete', methods=['GET'])  # api/get_messages
def query_autocomplete():
    """
    This method interfaces the SWIFT request to get the autocompleted search queries with the 
    Google Maps API.
    """

    # TODO: What data types are these?
    search_string = str(request.args.get('seach_string'))
    user_location = request.args.get('user_location'))

    return get_autocomplete(search_string, user_location)   



if __name__ == '__main__':
    app.run(debug=True)
