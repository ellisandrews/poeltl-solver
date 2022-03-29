# poeltl-solver
Solver for the Poeltl NBA player guessing game

## Notes:

### Project Setup

I am using `pipenv` for dependency and environment management.

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

Using alembic to version the db.

I manually ran `CREATE DATABASE poeltl;` as alembic seems to assume that db already exists.
Might be able to run this in `alembic/env.py` though.

#### Helpful commands

Generate a new revision:
```shell
alembic revision -m "create conferences table"
```

Run migrations
```shell
alembic upgrade head
```


### Data Extraction Steps:

1. Get teams by conference (db/extract/extract_teams.py)
2. Get players by team, using teams from above
