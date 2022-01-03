# -*- coding: utf-8 -*-

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from utils import snake_to_title_case, snake_to_camel_case, database_data_type, graphql_data_type, python_type_hint

class DataModelGraphQLRelation(BaseModel):
    relationship: str
    as_list: bool = Field(True)
    description: Optional[str]

class DataModelRelationship(BaseModel):
    # relation: str
    backref: str
    foreign_key: str

    @property
    def foreign_model(self):
        datamodel, _ = self.foreign_key.split('.', 1)
        return datamodel

    @property
    def foreign_database_model_name(self):
        return snake_to_title_case(self.foreign_model)

class DataModelField(BaseModel):
    name: str
    type: str
    default: Optional[str]
    onupdate: Optional[str]
    nullable: bool = Field(False)
    foreign_key: Optional[str]
    can_create: bool = Field(True)
    can_update: bool = Field(True)
    can_patch: bool = Field(True)
    description: Optional[str]

    @property
    def python_type_hint(self):
        return python_type_hint(self.type)

    @property
    def database_field_name(self):
        return self.name

    @property
    def database_field_type(self):
        return database_data_type(self.type)

    @property
    def graphql_field_name(self):
        return snake_to_camel_case(self.name)

    @property
    def graphql_type_name(self):
        return graphql_data_type(self.type)

class DataModelGraphQL(BaseModel):
    patch: bool = Field(True)
    create: bool = Field(True)
    delete: bool = Field(True)
    update: bool = Field(True)
    patchMutation: Optional[str] = None
    createMutation: Optional[str] = None
    deleteMutation: Optional[str] = None
    updateMutation: Optional[str] = None
    hierarchy: Dict[str, DataModelGraphQLRelation] = Field(None)
    identifier: Optional[str]

class DataModelIndex(BaseModel):
    fields: List[str]

class DataModel(BaseModel):
    table: str
    primary_key: str
    graphql: DataModelGraphQL = Field(DataModelGraphQL())
    fields: List[DataModelField]
    relationships: Optional[Dict[str, DataModelRelationship]]
    indexes: Optional[Dict[str, DataModelIndex]]
    description: Optional[str]

    @property
    def graphql_patch_mutation(self):
        return self.graphql.patchMutation or f"patch{self.graphql_type_name}"

    @property
    def graphql_create_mutation(self):
        return self.graphql.createMutation or f"create{self.graphql_type_name}"

    @property
    def graphql_delete_mutation(self):
        return self.graphql.deleteMutation or f"delete{self.graphql_type_name}"

    @property
    def graphql_update_mutation(self):
        return self.graphql.updateMutation or f"update{self.graphql_type_name}"

    @property
    def database_model_name(self):
        return snake_to_title_case(self.table)

    @property
    def graphql_identifier_type(self):
        return "Int"    # FIXME not necessarily

    @property
    def graphql_identifier(self):
        # return self.graphql.identifier or snake_to_camel_case(self.primary_key)
        return snake_to_camel_case(self.primary_key)

    @property
    def graphql_type_name(self):
        return snake_to_title_case(self.table)

class Backend(BaseModel):
    package: str = Field("internal")
    model_imports: Optional[List[str]]

class Config(BaseModel):
    backend: Backend
    datamodel: Dict[str, DataModel]
