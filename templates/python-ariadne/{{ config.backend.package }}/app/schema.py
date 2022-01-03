# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class ParameterError(BaseModel):
    field: str
    error: str

class MutationResponse(BaseModel):
    success: bool
    errors: Optional[List[ParameterError]]
    data: Optional[object]

{%- for name, model in config.datamodel.items() %}
    {%- if model.graphql.create %}

class Create{{ model.graphql_type_name }}(BaseModel):
        {%- for field in model.fields %}
            {%- if field.can_create %}
    {{ field.graphql_field_name }}: {% if field.nullable %}Optional[{{ field.python_type_hint }}]{% else %}{{ field.python_type_hint }}{% endif %}
            {%- endif %}
        {%- endfor %}

class Create{{ model.graphql_type_name }}Response(MutationResponse):
    pass
    {%- endif %}

    {%- if model.graphql.update %}

class Update{{ model.graphql_type_name }}(BaseModel):
        {%- for field in model.fields %}
            {%- if field.can_update %}
    {{ field.graphql_field_name }}: {% if field.nullable %}Optional[{{ field.python_type_hint }}]{% else %}{{ field.python_type_hint }}{% endif %}
            {%- endif %}
        {%- endfor %}

class Update{{ model.graphql_type_name }}Response(MutationResponse):
    pass
    {%- endif %}

    {%- if model.graphql.upsert %}

class Upsert{{ model.graphql_type_name }}(BaseModel):
        {%- for field in model.fields %}
            {%- if field.can_update %}
    {{ field.graphql_field_name }}: {% if field.nullable %}Optional[{{ field.python_type_hint }}]{% else %}{{ field.python_type_hint }}{% endif %} = Field(Ellipsis)
            {%- endif %}
        {%- endfor %}

class Upsert{{ model.graphql_type_name }}Response(MutationResponse):
    pass
    {%- endif %}
{%- endfor %}
