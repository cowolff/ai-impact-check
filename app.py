from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
from database import AffiliationLocator
import geopandas as gpd

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv('API_KEY')
MAPS_API_KEY = os.getenv('MAPS_API_KEY')
BASE_URL = 'https://api.elsevier.com/content/search/scopus'
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

def get_papers_and_affiliations(query, num_results=10):
    headers = {
        'X-ELS-APIKey': API_KEY,
        'Accept': 'application/json'
    }
    steps = 10
    papers_info = []

    database = AffiliationLocator(api_key=MAPS_API_KEY)

    for i in range(0, num_results, steps):
        params = {'query': query, 'count': steps, 'start': i}
        response = requests.get(BASE_URL, headers=headers, params=params)
        if response.status_code != 200:
            return []

        data = response.json()
        datapoints = data.get('search-results', {}).get('entry', [])
        for entry in datapoints:
            affiliations = entry.get('affiliation', [])
            for affiliation in affiliations:
                lat, lon = database.get_location(affiliation.get('affilname', 'N/A'), affiliation.get('affiliation-country', 'N/A'))
                affiliation_info = {
                    'name': affiliation.get('affilname', 'N/A'),
                    'city': affiliation.get('affiliation-city', 'N/A'),
                    'country': affiliation.get('affiliation-country', 'N/A'),
                    'latitude': lat,
                    'longitude': lon
                }
                papers_info.append(affiliation_info)
        if len(datapoints) == 0:
            break

    return papers_info

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/affiliations', methods=['GET'])
def affiliations():
    query = request.args.get('query')
    num_results = int(request.args.get('num_results', 10))
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    affiliations = get_papers_and_affiliations(query, num_results)
    print(affiliations)
    return jsonify(affiliations)

if __name__ == '__main__':
    app.run(debug=True)
