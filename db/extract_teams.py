import json
from pprint import pprint

import requests

from .common import BASE_URL, HEADERS


if __name__ == '__main__':

    for conference in ('East', 'West'):
        query_params = {'conference': conference}
        response = requests.request('GET', BASE_URL + '/teams', headers=HEADERS, params=query_params)

        # print(response.text)
        response.raise_for_status()

        response_json = response.json()
        # pprint(response_json)

        team_data = response_json['response']

        with open(f"db/data/raw/teams_{conference.lower()}.json", 'w') as json_file:
            json.dump(team_data, json_file, indent=4)
