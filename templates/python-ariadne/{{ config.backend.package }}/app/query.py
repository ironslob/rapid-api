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
    def resolve_get{{ model.graphql_type_name }}ById(
        response,
        info,
        {{ model.graphql_identifier }}
    ):
        # TODO according to https://github.com/mirumee/ariadne/issues/218 we should be able to identify hierarchical fields and joinload them on-demand
        return app.session.query(models.{{ model.database_model_name }}).get({{ model.graphql_identifier }})

    @query.field("get{{ model.graphql_type_name }}")
    def resolve_get{{ model.graphql_type_name }}(
        response,
        info,
        offset: int,
        limit: int,
  {%- for field in model.fields %}
      {%- if field.filters.equal %}
        {{ field.graphql_field_name }}: {{ field.python_type_hint }} = ...,
      {%- endif %}
  {%- endfor %}
    ):
        limit = max(0, min(limit, 25))
        offset = max(0, offset)

        # TODO according to https://github.com/mirumee/ariadne/issues/218 we should be able to identify hierarchical fields and joinload them on-demand
        query = (
            app.session.query(models.{{ model.database_model_name }})
  {%- if model.graphql.hierarchy -%}
            .options(
    {%- for name, relation in model.graphql.hierarchy.items() %}
      {%- if relation.eager_load %}
                joinedload(models.{{ model.database_model_name }}.{{ name }}),
      {%- endif %}
    {%- endfor %}
            )
  {%- endif %}
                # .filter(...)
        )

  {%- for field in model.fields %}
      {%- if field.filters.equal %}

        if {{ field.graphql_field_name }} is not Ellipsis:
            query = query.filter(models.{{ model.database_model_name }}.{{ field.name }} == {{ field.graphql_field_name }})
      {%- endif %}
  {%- endfor %}

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
