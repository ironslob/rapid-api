# Automated code generator

## Aims

I've written too many CRUD implementations for APIs with ReactJS frontends, so
I thought I'd spend some time making it trivial to generate them from a
datamodel, and then I can spend my time working on the more challenging parts
of a product.

## How does it work?

Define a datamodel, then the generator will run your chosen template with the
config provided and spit out some code that should work for the datamodel
specified.

See example.yaml.

## Does it work?

It should!

## What templates are available?

At the time of writing (5th Jan 2022) there is a single template available -
python-ariadne - which will take your datamodel and spit out a Flask/Ariadne
backed Python application to provide a GraphQL implementation.

## How do I try it out?

### Setup

```
 ➜  ~ git clone git@github.com:ironslob/rapid-api.git
Cloning into 'rapid-api'...
remote: Enumerating objects: 143, done.
remote: Counting objects: 100% (143/143), done.
remote: Compressing objects: 100% (82/82), done.
remote: Total 143 (delta 58), reused 129 (delta 44), pack-reused 0
Receiving objects: 100% (143/143), 26.92 KiB | 362.00 KiB/s, done.
Resolving deltas: 100% (58/58), done.
 ➜  ~ cd rapid-api
 ➜  rapid-api git:(main) python3 -m venv venv
 ➜  rapid-api git:(main) ✗ source venv/bin/activate
(venv)  ➜  rapid-api git:(main) ✗ pip install -r requirements.txt
Collecting click==8.0.3
  Using cached click-8.0.3-py3-none-any.whl (97 kB)
Collecting Jinja2==3.0.3
  Using cached Jinja2-3.0.3-py3-none-any.whl (133 kB)
Collecting MarkupSafe==2.0.1
  Using cached MarkupSafe-2.0.1-cp38-cp38-manylinux2010_x86_64.whl (30 kB)
Collecting pydantic==1.8.2
  Using cached pydantic-1.8.2-cp38-cp38-manylinux2014_x86_64.whl (13.7 MB)
Collecting PyYAML==6.0
  Using cached PyYAML-6.0-cp38-cp38-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (701 kB)
Collecting typing-extensions==4.0.1
  Using cached typing_extensions-4.0.1-py3-none-any.whl (22 kB)
Installing collected packages: click, MarkupSafe, Jinja2, typing-extensions, pydantic, PyYAML
Successfully installed Jinja2-3.0.3 MarkupSafe-2.0.1 PyYAML-6.0 click-8.0.3 pydantic-1.8.2 typing-extensions-4.0.1
```

### Generate code

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
