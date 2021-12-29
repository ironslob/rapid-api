# -*- coding: utf-8 -*-

def snake_to_title_case(string):
    return string.replace("_", " ").title().replace(" ", "")

def snake_to_camel_case(string):
    snake = snake_to_title_case(string)

    return snake[0].lower() + snake[1:]

def database_model_name(model):
    return snake_to_title_case(model["table"])

def database_data_type(string):
    types = dict(
        string = "sqlalchemy.Text",
        integer = "sqlalchemy.Integer",
        bigint = "sqlalchemy.BigInteger",
        smallint = "sqlalchemy.SmallInteger",
        datetime = "sqlalchemy.DateTime",
        date = "sqlalchemy.Date",
        decimal = "sqlalchemy.Numeric(asdecimal=True)",
        numeric = "sqlalchemy.Numeric()",
    )

    return types[string]

def graphql_data_type(string):
    types = dict(
        string = "String",
        integer = "Int",
        bigint = "Int",
        smallint = "Int",
        datetime = "DateTime",
        date = "Date",
        decimal = "Float",
        numeric = "Float",
    )

    return types[string]
