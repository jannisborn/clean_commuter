#%%
from flask import Flask
from flask import jsonify, request
import json
from greentastic.compute_scores import compute_score
from greentastic.api_requests import get_directions, get_autocomplete

app = Flask(__name__)


#%%
@app.route('/query_directions', methods=['GET'])  # api/get_messages
def query_directions():
    weight_str = str(request.args.get('weights', "1,1,1,1,1"))
    weighting = [float(i)
                 for i in weight_str.split(",")]  # expects 'weights=1,1,1,1'
    print("WEIGHTS", weighting)

    source = str(request.args.get('source'))
    destination = str(
        request.args.get('destination'))  # 'dest_coordinates=bern straße xy'

    googlemapsdic = get_directions(source, destination)

    # Load metadata from json file
    with open("assets/metadata.json", "r") as infile:
        metadata = json.load(infile)

    # Car type can be any of {"Petrol", "Diesel", "Electric"}
    car_type = request.args.get('car_type', "Petrol")
    metadata['driving']['emissionsProKM'] = metadata['driving'][
        'emissionsProKM'][car_type]
    metadata['driving']['toxicityPerKM'] = metadata['driving'][
        'toxicityPerKM'][car_type]

    # Compute scores from google maps data
    out_dic = compute_score(metadata, googlemapsdic, weights=weighting)
    return jsonify(out_dic)  # return json file


@app.route('/query_autocomplete', methods=['GET'])  # api/get_messages
def query_autocomplete():
    """
    This method interfaces the SWIFT request to get the autocompleted search queries with the
    Google Maps API.
    """

    # TODO: What data types are these?
    search_string = str(request.args.get('search_string'))
    user_location = str(request.args.get('user_location'))

    return jsonify(get_autocomplete(search_string, user_location))


if __name__ == '__main__':
    app.run(debug=True)
