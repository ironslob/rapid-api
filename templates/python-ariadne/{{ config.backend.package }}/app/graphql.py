# -*- coding: utf-8 -*-

from datetime import datetime
from ariadne import (
    ScalarType,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)

from .query import queries
from .mutation import mutations
from .resolver import resolvers

type_defs = load_schema_from_path("schema.graphql")

date_scalar = ScalarType("Date")
datetime_scalar = ScalarType("DateTime")

@date_scalar.serializer
def serialize_date(timevalue):
    obj = timevalue

    if isinstance(obj, datetime):
        obj = timevalue.date()

    return obj.isoformat()

@datetime_scalar.serializer
def serialize_datetime(timevalue):
    return timevalue.isoformat()

schema = make_executable_schema(
    type_defs,
    *resolvers(),
    *queries(),
    *mutations(),
    date_scalar,
    datetime_scalar,
)

snake_case_fallback_resolvers.bind_to_schema(schema)
