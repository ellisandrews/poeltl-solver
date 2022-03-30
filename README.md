# poeltl-solver
Solver for the Poeltl NBA player guessing game

## Notes:

### Project Setup

This projects uses `pipenv` for dependency and environment management.

#### Helpful commands

Install a dependency:
```shell
pipenv install <package>
```

Activate the pipenv shell/virtualenv:
```shell
pipenv shell
```

Exit pipenv shell/virtualenv:
```shell
exit
```

### Database

#### Fetch Data
Data is pulled from an NBA API. To extract the relevant data:

1. Set API key as an environment variable
```shell
export RAPIDAPI_KEY="<your_api_key>"
```
2. Run `python db/fetch_data.py` to pull data from the API and store it in `db/raw_data/`


#### Load Data

This project uses SQLAlchemy ORM for database management.

1. Manually run `CREATE DATABASE poeltl;` as sqlalchemy assumes that db already exists.

2. Run `python db/create_database.py` to create the db tables and insert data.
