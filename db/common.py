import os


def get_rapidapi_key():
    rapidapi_key = os.environ.get('RAPIDAPI_KEY')
    if rapidapi_key is None:
        raise ValueError('Must set environment variable: RAPIDAPI_KEY')
    return rapidapi_key


API_BASE_URL = 'https://api-nba-v1.p.rapidapi.com'

API_HEADERS = {
	'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com',
	'X-RapidAPI-Key': get_rapidapi_key()
}

CONFERENCES = ('East', 'West')

RAW_DATA_DIRECTORY = 'db/raw_data'
