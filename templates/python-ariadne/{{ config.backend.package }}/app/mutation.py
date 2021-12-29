# -*- coding: utf-8 -*-

from datetime import date
from ariadne import MutationType, convert_kwargs_to_snake_case
from typing import List
from flask import current_app as app
from urllib import request

from .db import models
from .schema import MutationResponse, ParameterError

import logging

logger = logging.getLogger(__name__)

def mutations():
    mutation = MutationType()

{% for name, model in config.backend.datamodel.items() %}
  {%- if model.graphql.create %}
    @mutation.field("create{{ model.graphql_type_name }}")
    def resolve_create{{ model.graphql_type_name }}(
        response,
        info,
    {%- for field in model.fields %}
        {%- if field.name != model.primary_key %}
        {{ field.graphql_field_name }}: {{ field.python_type_hint }},
        {%- endif %}
    {%- endfor %}
    ):
        errors = []
        success = False

        # TODO validation goes here
        # obj = app.session.query(models.{{ model.database_model_name }}).get({{ model.graphql_identifier }})

        if not errors:
            obj = models.{{ model.database_model_name }}(
    {%- for field in model.fields %}
                {{ field.database_field_name }}={{ field.graphql_field_name }},
    {%- endfor %}
            )

            app.session.add(obj)
            app.session.commit()

            success = True

            # TODO handle hierarchy

        response = MutationResponse(
            success=success,
            errors=errors or None,
        )

        return response.dict()

  {% endif %}
  {%- if model.graphql.update %}
    @mutation.field("update{{ model.graphql_type_name }}")
    def resolve_update{{ model.graphql_type_name }}(
        response,
        info,
    {%- for field in model.fields %}
        {{ field.graphql_field_name }}: {{ field.python_type_hint }},
    {%- endfor %}
    ):
        errors = []
        success = False

        # TODO validation goes here
        obj = app.session.query(models.{{ model.database_model_name }}).get({{ model.graphql_identifier }})

        if not obj:
            errors.append('{{ model.graphql_type_name }} not found')

        if not errors:
    {%- for field in model.fields %}
        {%- if field.name != model.primary_key %}
            obj.{{ field.database_field_name }} = {{ field.graphql_field_name }}
        {%- endif %}
    {%- endfor %}

            app.session.commit()

            success = True

            # TODO handle hierarchy

        response = MutationResponse(
            success=success,
            errors=errors or None,
        )

        return response.dict()

  {% endif %}
  {%- if model.graphql.upsert %}
    @mutation.field("upsert{{ model.graphql_type_name }}")
    def resolve_upsert{{ model.graphql_type_name }}(
        response,
        info,
    {%- for field in model.fields %}
        {{ field.graphql_field_name }}: {{ field.python_type_hint }}{% if field.name != model.primary_key %} = ...{% endif -%},
    {%- endfor %}
    ):
        errors = []
        success = False

        # TODO validation goes here
        obj = app.session.query(models.{{ model.database_model_name }}).get({{ model.graphql_identifier }})

        if not obj:
            errors.append('{{ model.graphql_type_name }} not found')

        if not errors:
    {%- for field in model.fields %}
        {%- if field.name != model.primary_key %}
            if {{ field.graphql_field_name }} is not Ellipsis:
                obj.{{ field.database_field_name }} = {{ field.graphql_field_name }}
        {% endif %}
    {%- endfor %}

            app.session.commit()

            success = True

            # TODO handle hierarchy

        response = MutationResponse(
            success=success,
            errors=errors or None,
        )

        return response.dict()

  {% endif %}
  {%- if model.graphql.create %}
    @mutation.field("delete{{ model.graphql_type_name }}")
    def resolve_delete{{ model.graphql_type_name }}(
        response,
        info,
    {%- for field in model.fields %}
        {%- if field.name == model.primary_key %}
        {{ field.graphql_field_name }}: {{ field.python_type_hint }},
        {%- endif %}
    {%- endfor %}
    ):
        errors = []
        success = False

        # TODO validation goes here
        obj = app.session.query(models.{{ model.database_model_name }}).get({{ model.graphql_identifier }})

        if not obj:
            errors.append('{{ model.graphql_type_name }} not found')

        if not errors:
            app.session.delete(obj)
            app.session.commit()

            success = True

            # TODO handle hierarchy

        response = MutationResponse(
            success=success,
            errors=errors or None,
        )

        return response.dict()

  {% endif %}
{% endfor %}

    return [mutation]