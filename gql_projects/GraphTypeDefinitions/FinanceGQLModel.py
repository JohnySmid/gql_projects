import strawberry as strawberryA
import datetime
import uuid
from typing import List, Annotated, Optional, Union
from .BaseGQLModel import BaseGQLModel

import strawberry
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

# from gql_projects.GraphResolvers import (
#     resolveFinanceTypeById,
#     resolveProjectById,
#     resolveFinanceAll
# )

from gql_projects.GraphTypeDefinitions.GraphResolvers import (
    resolve_id,
    resolve_authorization_id,
    resolve_user_id,
    resolve_accesslevel,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    createRootResolver_by_page,
)

ProjectGQLModel = Annotated["ProjectGQLModel",strawberryA.lazy(".ProjectGQLModel")]
FinanceTypeGQLModel = Annotated ["FinanceTypeGQLModel",strawberryA.lazy(".FinanceTypeGQLModel")]



@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance"""
)
class FinanceGQLModel(BaseGQLModel):
    @classmethod

    def getLoader(cls, info):
        return getLoadersFromInfo(info).finances
    # async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
    #     loader = getLoadersFromInfo(info).finances
    #     result = await loader.load(id)
    #     if result is not None:
    #         result._type_definition = cls._type_definition  # little hack :)
    #     return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""Time stamp""")
    def lastchange(self) -> uuid.UUID:
        return self.lastchange

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Amount""")
    def amount(self) -> float:
        return self.amount

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Project of finance""")
    async def project(self, info: strawberryA.types.Info) -> Optional ["ProjectGQLModel"]:
        loader = getLoadersFromInfo(info).projects
        result = await loader.load(self.project_id)
        return result
        # async with withInfo(info) as session:
        #     result = await resolveProjectById(session, self.project_id)
        #     return result

    @strawberryA.field(description="""Finance type of finance""")
    async def financeType(self, info: strawberryA.types.Info) -> Optional ["FinanceTypeGQLModel"]:
        loader = getLoadersFromInfo(info).finances
        result = await loader.load(self.financetype_id)
        return result
        # async with withInfo(info) as session:
        #     result = await resolveFinanceTypeById(session, self.financetype_id)
        #     return result
###########################################################################################################################
#
# Query 
#
###########################################################################################################################
#from contextlib import asynccontextmanager

# @asynccontextmanager
# async def withInfo(info):
#     asyncSessionMaker = info.context["asyncSessionMaker"]
#     async with asyncSessionMaker() as session:
#         try:
#             yield session
#         finally:
#             pass

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class FinanceWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of finances""")
async def finance_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[FinanceWhereFilter] = None
) -> List[FinanceGQLModel]:
    # async with withInfo(info) as session:
    #     result = await resolveFinanceAll(session, skip, limit)
    #     return result
    loader = getLoadersFromInfo(info).finances
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

finance_by_id = createRootResolver_by_id(FinanceGQLModel, description="Returns finance by its id")

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

@strawberryA.input(description="Definition of financial data used for insertion")
class FinanceInsertGQLModel:
    name: str = strawberryA.field(description="Name of the financial data")
    financetype_id: uuid.UUID = strawberryA.field(description="The ID of the financial data type")
    project_id: uuid.UUID = strawberryA.field(description="The ID of the associated project")

    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the financial data (optional)",default=None)
    amount: Optional[float] = strawberryA.field(description="The amount of financial data (optional)", default=0.0)
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberryA.input(description="Definition of financial data used for update")
class FinanceUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the financial data")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberryA.field(description="The name of the financial data (optional)",default=None)
    financetype_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the financial data type (optional)",default=None)
    amount: Optional[float] = strawberryA.field(description="The amount of financial data (optional)", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Input structure - D operation")
class FinanceDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")

@strawberryA.type(description="Result of a financial data operation")
class FinanceResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the financial data", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the financial data")
    async def finance(self, info: strawberryA.types.Info) -> Union[FinanceGQLModel, None]:
        result = await FinanceGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.mutation(description="Adds a new finance record.")
async def finance_insert(self, info: strawberryA.types.Info, finance: FinanceInsertGQLModel) -> FinanceResultGQLModel:
    user = getUserFromInfo(info)
    print(user)
    finance.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).finances
    row = await loader.insert(finance)
    result = FinanceResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the finance record.")
async def finance_update(self, info: strawberryA.types.Info, finance: FinanceUpdateGQLModel) -> FinanceResultGQLModel:
    user = getUserFromInfo(info)
    finance.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).finances
    row = await loader.update(finance)
    result = FinanceResultGQLModel()
    result.msg = "ok"
    result.id = finance.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"  
    return result

@strawberry.mutation(description="Delete the authorization user")
async def finance_delete(
        self, info: strawberry.types.Info, finance: FinanceDeleteGQLModel
) -> FinanceResultGQLModel:
    finance_id_to_delete = finance.id
    loader = getLoadersFromInfo(info).finances
    row = await loader.delete(finance_id_to_delete)
    if not row:
        return FinanceResultGQLModel(id=finance_id_to_delete, msg="fail, user not found")
    result = FinanceResultGQLModel(id=finance_id_to_delete, msg="ok")
    return result