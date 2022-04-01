import os
import json
from time import sleep

import requests

from .common import CONFERENCES, RAW_DATA_DIRECTORY, slugify


def get_rapidapi_key():
    rapidapi_key = os.environ.get('RAPIDAPI_KEY')
    if rapidapi_key is None:
        raise ValueError('Must set environment variable: RAPIDAPI_KEY')
    return rapidapi_key


API_BASE_URL = 'https://api-nba-v1.p.rapidapi.com/'

API_HEADERS = {
	'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com',
	'X-RapidAPI-Key': get_rapidapi_key()
}


def execute_api_get_request(endpoint, params):
    print(f"Making GET request to /{endpoint} with params {params}")
    response = requests.request('GET', API_BASE_URL+endpoint, headers=API_HEADERS, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':

    # NOTE: With my API key, I can only execute 10 requests/min
    sleep_secs = 10

    # First, fetch team data per conference. Save teams in memory to be used in next round of API calls.
    all_teams = []
    for conference in CONFERENCES:

        response_json = execute_api_get_request('teams', {'conference': conference})
        teams = response_json['response']

        # Filter out some garbage teams we don't want at all
        teams = [team for team in teams if (not team['allStar'] and team['nbaFranchise'])]

        with open(f"{RAW_DATA_DIRECTORY}/teams_{slugify(conference)}.json", 'w') as json_file:
            json.dump(teams, json_file, indent=4)

        all_teams.extend(teams)

    # Next, fetch player data per team returned above
    for team in all_teams:

        print(f"Sleeping {sleep_secs} seconds before next requst...")
        sleep(sleep_secs)

        response_json = execute_api_get_request('players', {'team': team['id'], 'season': 2021})
        players = response_json['response']

        # Filter out some garbage players we dont' want at all
        players = [player for player in players if (player['leagues'].get('standard') and player['leagues']['standard']['active'])]

        with open(f"{RAW_DATA_DIRECTORY}/players_{slugify(team['city'] + ' ' + team['nickname'])}.json", 'w') as json_file:
            json.dump(players, json_file, indent=4)
