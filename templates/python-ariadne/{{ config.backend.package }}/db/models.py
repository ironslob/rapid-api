# -*- coding: utf-8 -*-

from sqlalchemy.orm import relationship
import sqlalchemy

from .session import Base

{% if config.backend.model_imports is defined %}
    {% for model_import in config.backend.model_imports %}
{{ model_import }}
    {% endfor %}
{% endif %}

{% for name, model in config.datamodel.items() %}
class {{ model.database_model_name }}(Base):
    __tablename__ = "{{ model.table }}"

    # fields
    {% for field in model.fields %}

    {{ field.name }} = Column(
        {{ field.database_field_type }}
        {% if field.foreign_key %}
        , ForeignKey("{{ field.foreign_key }}")
        {% endif %}
        {% if model.primary_key == field.name %}
        , primary_key=True
        {% endif %}
        , nullable={{ field.nullable }}
        {% if field.default %}
        , default={{ field.default }}
        {% endif %}
        {% if field.onupdate %}
        , onupdate={{ field.onupdate }}
        {% endif %}
    )

    {% endfor %}

    {% if model.indexes %}
    __table_args__ = (
        {% for name, index in model.indexes.items() %}
        sqlalchemy.Index("{{ name }}"{% for field in index.fields %}, "{{ field }}" {% endfor %}),
        {% endfor %}
    )
    {% endif %}

    {% if model.relationships %}
        {% for name, relationship in model.relationships.items() %}

    {{ name }} = relationship(
        {{ relationship.foreign_database_model_name }}
        {% if relationship.backref %}
        , backref="{{ relationship.backref }}"
        {% endif %}
    )

        {% endfor %}
    {% endif %}
{% endfor %}
