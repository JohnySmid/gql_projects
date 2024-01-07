import strawberry as strawberryA
import datetime
import uuid
from typing import List, Annotated, Optional, Union

import strawberry
from gql_projects.utils.DBFeeder import randomDataStructure
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance"""
)
class FinanceCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        loader = getLoadersFromInfo(info).financecategory
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""Time stamp""")
    def lastchange(self) -> uuid.UUID:
        return self.lastchange

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""Name en""")
    def name_en(self) -> str:
        return self.name_en

###########################################################################################################################
#
# Query 
#
###########################################################################################################################

from contextlib import asynccontextmanager

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class FinanceCategoryWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of projects""")
async def finance_category_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[FinanceCategoryWhereFilter] = None
) -> List[FinanceCategoryGQLModel]:
    # otazka: musi tady byt async? 
    # async with withInfo(info) as session:
    loader = getLoadersFromInfo(info).financecategory
    wf = None if where is None else strawberry.asdict(where)
    #result = await resolveProjectAll(session, skip, limit)
    result = await loader.page(skip, limit, where = wf)
    return result

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################
from typing import Optional

@strawberryA.input(description="Definition of a project used for creation")
class FinanceCategoryInsertGQLModel:
    name: str = strawberryA.field(description="Name/label of the project")

    name_en: str = strawberryA.field(description="", default=None)
    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key (UUID), could be client-generated", default=None)
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberryA.input(description="Definition of a project used for update")
class FinanceCategoryUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    name_en: str = strawberryA.field(description="", default=None)
    changedby: strawberry.Private[uuid.UUID] = None


@strawberryA.type(description="Result of a mutation over Project")
class FinanceCategoryResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project")
    async def project(self, info: strawberryA.types.Info) -> Union[FinanceCategoryGQLModel, None]:
        result = await FinanceCategoryGQLModel.resolve_reference(info, self.id)
        return result


@strawberryA.mutation(description="Adds a new project.")
async def finance_category_insert(self, info: strawberryA.types.Info, finance: FinanceCategoryInsertGQLModel) -> FinanceCategoryResultGQLModel:
    # user = getUserFromInfo(info)
    # project.createdby = uuid.UUID(user["id"])

    loader = getLoadersFromInfo(info).financecategory
    row = await loader.insert(finance)
    result = FinanceCategoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project.")
async def finance_category_update(self, info: strawberryA.types.Info, finance: FinanceCategoryUpdateGQLModel) -> FinanceCategoryResultGQLModel:
    # user = getUserFromInfo(info)
    # project.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).financecategory
    row = await loader.update(finance)
    result = FinanceCategoryResultGQLModel()
    result.msg = "ok"
    result.id = finance.id
    if row is None:
        result.msg = "fail"
    return result