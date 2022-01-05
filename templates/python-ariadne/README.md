# Python / Flask / Ariadne GraphQL API template

A template to generate a GraphQl API using the datamodel provided, backed by Postgres.

## --option values

- rollbar - will include rollbar in the generated API, will take the rollbar token from environment variables `ROLLBAR_TOKEN`, and environment name from `ROLLBAR_ENV`

## Generate code

There's an example.yaml file provided which will create a datamodel for a simple restaurant review system. There is no authentication or authorisation, just the CRUD work. Run it like so:

```
 ➜  rapid-graphql git:(main) ✗ python3 generator.py  --config example.yaml --template templates/python-ariadne --output test

Generating test/schema.graphql
Generating test/wsgi.py
Generating test/docker-compose.yml
Generating test/internal/constants.py
Generating test/internal/db/session.py
Generating test/internal/db/models.py
Generating test/internal/app/nocache.py
Generating test/internal/app/schema.py
Generating test/internal/app/instance.py
Generating test/internal/app/query.py
Generating test/internal/app/mutation.py
Generating test/internal/app/graphql.py
Generating test/internal/app/resolver.py
Generating test/templates/404.html
 ➜  rapid-graphql git:(main) ✗ 
```

A directory called `test` will be created and contain the code for the generated API.

### Optional - Clean it up

If you'd like to clean it up, I suggest running the code through `black(1)` to make it nicer.

```
$ black test
```

### Setup

We have to do several things:

1. Create a Python virtual environment
2. Run Postgres via docker-compose file
3. Install dependencies in it
4. Run the server

```
 ➜  rapid-graphql git:(main) ✗ cd test
 ➜  test git:(main) ✗ python3 -m venv env
 ➜  test git:(main) ✗ source env/bin/activate
(env)  ➜  test git:(main) ✗ docker-compose up -d
Starting test_db_1 ... done
(env)  ➜  test git:(main) ✗ pip install -r requirements.txt
...
(env)  ➜  test git:(main) ✗ DATABASE_URL="postgresql+psycopg2://postgres:postgres@db:5433/db_test" PYTHONPATH=. python3 -c 'from internal.db import session, models; models.Base.metadata.create_all(session.engine)'
(env)  ➜  test git:(main) ✗ DATABASE_URL="postgresql+psycopg2://postgres:postgres@db:5433/db_test" FLASK_APP=wsgi flask run --reload --without-threads
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
INFO:werkzeug: * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
INFO:werkzeug: * Restarting with stat
```

### Test it!

We're going to issue a simple command - get me all reviews, and corresponding restaurant ids and basic user info:

```
curl 'http://localhost:5000/graphql' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: http://localhost:5000' --data-binary '{"query":"query {\n  getReview {\n    data {\n      reviewId\n      rating\n      restaurant{\n        restaurantId\n      }\n      user {\n        userId\n        username\n      }\n    }\n  }\n}"}' --compressed
```
