# poeltl-solver

![](demo.gif)

Automated solver for the Poeltl NBA player guessing game: [https://poeltl.dunk.town/](https://poeltl.dunk.town/)


## Development Environment Setup

Below are the steps to get a local development environment set up:

### 1. Clone the repository

Clone the repo and change to the project root directory

```shell
$ git clone git@github.com:ellisandrews/poeltl-solver.git
$ cd poeltl-solver
```

### 2. Install Pipenv

This project uses [Pipenv](https://pipenv.pypa.io/en/latest/) for dependency and environment management.

You can install Pipenv with `pip`:

```shell
$ pip install --user pipenv
```

### 3. Install Dependencies

Install dependencies with Pipenv:

```shell
$ pipenv install --dev
```

### 4. Install ChromeDriver

This project uses [Selenium](https://www.selenium.dev/documentation/) for web browser interactions.

Selenium requires a driver to interface with a browser. `poeltl-solver` is configured to use Google Chrome, so you will need to download the `ChromeDriver` version that is compatible with your machine's Chrome version [here](https://sites.google.com/chromium.org/driver/).

Then unzip the downloaded file and make sure the `chromedriver` executable is on your `$PATH`, likely by putting it in the `/usr/local/bin/` directory:

```shell
$ unzip chromedriver_mac64.zip
$ mv chromedriver /usr/local/bin/
```

Verify chromedriver is on `$PATH`:

```shell
$ which chromedriver
/usr/local/bin/chromedriver
```

If you get this error:

```
“chromedriver” cannot be opened because the developer cannot be verified.
```

You can tell macOS to trust the binary by running the following command:

```shell
$ xattr -d com.apple.quarantine /usr/local/bin/chromedriver
```

### 5. Setup Database

This project is backed by a PostgreSQL database. Ensure postgres is running locally on the default port 5432.

Manually create a new database named `poeltl`:

```shell
$ psql -h localhost -U postgres

postgres=# CREATE DATABASE poeltl;
CREATE DATABASE
```

Then run the following script to create the database schema and load player data:

```shell
$ pipenv run python poeltl/scripts/create_database.py
```

### 6. Verify

You can verify your local dev environment is working by simply executing the main `solve.py` script:

```shell
$ pipenv run python solve.py
```

This should launch a web browser and submit player guesses until the correct solution is reached or the maximum number of attempts is exceeded.


## Fetching New Data

The NBA player data is sourced from [API-NBA](https://api-sports.io/documentation/nba/v2).

Static data from that API for the 2021 NBA season is checked into this repo, but if you need to pull fresh data follow these steps:

### 1. Create a RapidAPI Account

Sign up for a [RapidAPI](https://rapidapi.com/) account and subscribe to [API-NBA](https://rapidapi.com/api-sports/api/api-nba/).

#### 2. Set your API key as an environment variable

```shell
export RAPIDAPI_KEY="<your_api_key>"
```

### 3. Fetch Data

Run the following script to pull data from the API and store it in the `poeltl/db/raw_data/` directory.

:warning: RapidAPI limits both the gross daily number of requests and the rate of requests you can execute for free. You may want to confirm that the script settings are still below the thresholds before running.

```shell
$ pipenv run python poeltl/scripts/fetch_data.py
```

## Helpful Commands

Run a script:

```shell
$ pipenv run python poeltl/scripts/create_database.py
```

Install a dependency:

```shell
$ pipenv install [--dev] <package>
```

Activate the Pipenv shell/virtualenv:

```shell
$ pipenv shell
```

Exit the Pipenv shell/virtualenv:

```shell
(poeltl-solver) $ exit
```
