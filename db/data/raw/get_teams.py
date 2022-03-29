import json
import os
from pprint import pprint

import requests


def get_rapidapi_key():
    rapidapi_key = os.environ.get('RAPIDAPI_KEY')
    if rapidapi_key is None:
        raise ValueError('Must set environment variable: RAPIDAPI_KEY')
    return rapidapi_key


BASE_URL = 'https://api-nba-v1.p.rapidapi.com'
HEADERS = {
	'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com',
	'X-RapidAPI-Key': get_rapidapi_key()
}

for conference in ('East', 'West'):
    query_params = {'conference': conference}
    response = requests.request('GET', BASE_URL + '/teams', headers=HEADERS, params=query_params)

    print(response.text)
    response.raise_for_status()

    response_json = response.json()
    pprint(response_json)

    team_data = response_json['response']

    with open(f"db/data/raw/teams_{conference.lower()}.json", 'w') as json_file:
        json.dump(team_data, json_file, indent=4)
