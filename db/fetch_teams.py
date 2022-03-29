import json
from pprint import pprint

import requests

from common import API_BASE_URL, API_HEADERS, CONFERENCES, RAW_DATA_DIRECTORY


if __name__ == '__main__':

    for conference in CONFERENCES:

        response = requests.request('GET', API_BASE_URL + '/teams', headers=API_HEADERS, params={'conference': conference})
        response.raise_for_status()

        response_json = response.json()
        team_data = response_json['response']

        with open(f"{RAW_DATA_DIRECTORY}/teams_{conference.lower()}.json", 'w') as json_file:
            json.dump(team_data, json_file, indent=4)
