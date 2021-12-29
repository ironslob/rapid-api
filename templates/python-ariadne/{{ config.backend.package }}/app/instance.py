# -*- coding: utf-8 -*-

from flask import (
    _app_ctx_stack,
    Flask,
    abort,
    Response,
    request,
    jsonify,
    render_template,
    render_template_string,
    make_response,
)
from sqlalchemy.orm import scoped_session

{%- if 'rollbar' in options %}
import rollbar.contrib.flask
from flask import got_request_exception
{%- endif %}

from flask_cors import CORS
from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from ariadne.wsgi import GraphQL

from . import nocache
from .graphql import schema
from ..constants import instance_path
from ..db import models
from ..db.session import SessionLocal

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    instance_path=instance_path,
    root_path=instance_path,
    template_folder="templates",
    static_folder="static",
    static_url_path="/",
)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

nocache.init(app)

{%- if 'rollbar' in options %}
# send exceptions from `app` to rollbar, using flask's signal system.
got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
{%- endif %}

graphql = GraphQL(schema)
cors = CORS(app)

@app.teardown_request
def close_db_session(args):
    if app.session.is_active:
        try:
            app.session.remove()

        except Exception as e:
            logger.warning(e)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)

    status_code = 200 if success else 400
    return jsonify(result), status_code
