# -*- coding: utf-8 -*-

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from utils import snake_to_title_case, snake_to_camel_case, database_data_type, graphql_data_type, python_type_hint

class DataModelGraphQLRelation(BaseModel):
    # name of the datamodel relationship that the relation operates via, see DataModel.relationships
    relationship: str

    # if this is a many-to-one or one-to-many relationship - FIXME many-to-many not supported yet
    as_list: bool = True

    # description for documention
    description: Optional[str]

    # whether this relation should be eager loaded by default when pulling data - FIXME this should eagerload when needed
    eager_load: bool = False

class DataModelRelationship(BaseModel):
    # sqlalchemy backref option, to specify that the relationship can be reversed
    backref: str

    # the name of the config model (not database model) that this relationship refers to
    foreign_model: str

    # the field that this model should join on - must be a foreign key
    foreign_model_field: str

    @property
    def foreign_database_model_name(self):
        return snake_to_title_case(self.foreign_model)

class DataModelFieldFilter(BaseModel):
    # whether this field can be specified and used as "equals"
    equal: bool = False

class DataModelField(BaseModel):
    # field name in the model, e.g. username
    name: str

    # field type, e.g. string, integer, bigint, smallint, datetime, date, decimal, numeric, 
    type: str

    # default value, if not specified, callable (e.g. datetime.utcnow) or value with quotes (e.g. "foo")
    default: Optional[str]

    # sqlalchemy onupdate value, callable, e.g. datatime.utcnow
    onupdate: Optional[str]

    # whether this field is nullable, defaults to false
    nullable: bool = Field(False)

    # whether this field is a foreign key or not, this specifies the name of the config model NOT the table name
    foreign_model: Optional[str]

    # and this is the field name within that model
    foreign_model_field: Optional[str]

    # can this field be specified within a create api method?
    can_create: bool = Field(True)

    # can this field be specified within an update api method?
    can_update: bool = Field(True)

    # can this field be specified within a patch api method?
    can_patch: bool = Field(True)
    
    # field description to be included in docs
    description: Optional[str]

    # filter information that can be specified when retrieving via the api
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
    # should we generate a patch api method?
    patch: bool = Field(True)

    # should we generate a create api method?
    create: bool = Field(True)

    # should we generate a delete api method?
    delete: bool = Field(True)

    # should we generate an update api method?
    update: bool = Field(True)

    # specify name for patch mutation
    patchMutation: Optional[str] = None

    # specify name for create mutation
    createMutation: Optional[str] = None

    # specify name for delete mutation
    deleteMutation: Optional[str] = None

    # specify name for update mutation
    updateMutation: Optional[str] = None

    # extra properties that should be exposed via relationships
    hierarchy: Dict[str, DataModelGraphQLRelation] = Field(None)

    # name of the identifier that should be used in graphql
    # identifier: Optional[str]

class DataModelIndex(BaseModel):
    # list of fields to be included in this index
    fields: List[str]

class DataModel(BaseModel):
    # name of the table to be created in the database for this model
    table: str

    # name of the primary key field (FIXME could be handled in model fields)
    primary_key: str

    graphql: DataModelGraphQL = Field(DataModelGraphQL())
    fields: List[DataModelField]

    # mapping of internal relationship name to relationship config
    relationships: Optional[Dict[str, DataModelRelationship]]

    # mapping of index name to index config
    indexes: Optional[Dict[str, DataModelIndex]]

    # description of this model to be added to the schema
    description: Optional[str]

    # private
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
    # package name for templates - TODO remove this in the future
    package: str = Field("internal")

    # list of import statements that should be added to the generated model files
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
