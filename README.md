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

`poeltl-solver` is backed by a postgres database with a `sqlalchemy` ORM on top of it.
Here are the steps to set up locally.

#### Initialize Database

1. Start postgres.

2. Connect to postgres and run `CREATE DATABASE poeltl;`

3. Run `python -m poeltl.create_database` to create the db tables and insert data.

#### Fetching Raw Data

The NBA player data comes from a freemium NBA API. 
Static data from that API is checked into this repo, but if you need to pull fresh data follow these steps:

1. Obtain an API key from RapidAPI.

2. Set your API key as an environment variable
```shell
export RAPIDAPI_KEY="<your_api_key>"
```

3. Run `python -m poeltl.fetch_data` to pull data from the API and store it in `poeltl/db/raw_data/`
