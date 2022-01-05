# -*- coding: utf-8 -*-

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from utils import snake_to_title_case, snake_to_camel_case, database_data_type, graphql_data_type, python_type_hint

class DataModelGraphQLRelation(BaseModel):
    relationship: str
    as_list: bool = True
    description: Optional[str]
    eager_load: bool = False

class DataModelRelationship(BaseModel):
    backref: str
    foreign_model: str
    foreign_model_field: str

    @property
    def foreign_database_model_name(self):
        return snake_to_title_case(self.foreign_model)

class DataModelFieldFilter(BaseModel):
    equal: bool = False

class DataModelField(BaseModel):
    name: str
    type: str
    default: Optional[str]
    onupdate: Optional[str]
    nullable: bool = Field(False)
    foreign_model: Optional[str]
    foreign_model_field: Optional[str]
    can_create: bool = Field(True)
    can_update: bool = Field(True)
    can_patch: bool = Field(True)
    description: Optional[str]
    filters: Optional[DataModelFieldFilter] = DataModelFieldFilter()

    def foreign_key(self, config):
        key = None

        if self.foreign_model and self.foreign_model_field:
            key = f"{config.datamodel[self.foreign_model].table}.{self.foreign_model_field}"

        return key

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

    backrefs: Dict[str, DataModelRelationship] = None

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

    backrefs_populated: bool = False

    def _populate_datamodelbackrefs(self):
        if not self.backrefs_populated:
            self.backrefs_populated = True

            for datamodel_name, datamodel in self.datamodel.items():
                if datamodel.relationships:
                    for rel_name, relationship in datamodel.relationships.items():
                        if relationship.backref:
                            foreign_model = self.datamodel[relationship.foreign_model]
                            if foreign_model.backrefs is None:
                                foreign_model.backrefs = {}

                            foreign_model.backrefs[relationship.backref] = DataModelRelationship(
                                backref=rel_name,
                                foreign_model=datamodel_name,
                                foreign_model_field=relationship.foreign_model_field,
                            )

    def graphql_relation_foreign_model(
        self,
        datamodel: DataModel,
        relation: DataModelGraphQLRelation,
    ) -> DataModel:

        self._populate_datamodelbackrefs()

        if datamodel.relationships and relation.relationship in datamodel.relationships:
            relationship = datamodel.relationships[relation.relationship]

        elif datamodel.backrefs and relation.relationship in datamodel.backrefs:
            relationship = datamodel.backrefs[relation.relationship]

        foreign_model = self.datamodel[relationship.foreign_model]

        return foreign_model
