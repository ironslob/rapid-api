# -*- coding: utf-8 -*-

{% if config.backend.model_imports is defined %}
    {% for model_import in config.backend.model_imports %}
{{ model_import }}
    {% endfor %}
{% endif %}

from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class ParameterError(BaseModel):
    field: str
    error: str

class MutationResponse(BaseModel):
    success: bool
    errors: Optional[List[ParameterError]]
    data: Optional[object]

    class Config:
        arbitrary_types_allowed = True

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

    {%- if model.graphql.patch %}

class Patch{{ model.graphql_type_name }}(BaseModel):
        {%- for field in model.fields %}
            {%- if field.can_update %}
    {{ field.graphql_field_name }}: {{ field.python_type_hint }} = None
            {%- endif %}
        {%- endfor %}

class Patch{{ model.graphql_type_name }}Response(MutationResponse):
    pass
    {%- endif %}
{%- endfor %}
