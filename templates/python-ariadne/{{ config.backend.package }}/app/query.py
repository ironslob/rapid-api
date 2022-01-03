# -*- coding: utf-8 -*-

from datetime import datetime
from ariadne import QueryType
from flask import current_app as app
from sqlalchemy.orm import joinedload
from ..db import models

import logging

logger = logging.getLogger(__name__)


def queries():
    query = QueryType()

{% for name, model in config.datamodel.items() %}
    @query.field("get{{ model.graphql_type_name }}ById")
    def resolve_get{{ model.graphql_type_name }}ById(response, info, {{ model.graphql_identifier }}):
        # TODO according to https://github.com/mirumee/ariadne/issues/218 we should be able to identify hierarchical fields and joinload them
        return app.session.query(models.{{ model.database_model_name }}).get({{ model.graphql_identifier }})

    @query.field("get{{ model.graphql_type_name }}")
    def resolve_get{{ model.graphql_type_name }}(response, info, offset: int, limit: int):
        limit = max(0, min(limit, 25))
        offset = max(0, offset)

        # TODO according to https://github.com/mirumee/ariadne/issues/218 we should be able to identify hierarchical fields and joinload them
        query = (
            app.session.query(models.{{ model.database_model_name }})
                # .filter(...)
        )

        total = query.count()

        data = (
            query
            .limit(limit)
            .offset(offset)
            .all()
        )

        return dict(
            data=data,
            total=total,
        )
{% endfor %}

    return [query]
