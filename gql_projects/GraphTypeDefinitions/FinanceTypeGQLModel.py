import strawberry as strawberryA
import uuid
from typing import List, Annotated, Optional, Union
from gql_projects.GraphResolversOLD import resolveFinancesForFinanceType, resolveFinanceTypeAll
from contextlib import asynccontextmanager
import datetime

from .BaseGQLModel import BaseGQLModel
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
import strawberry
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

# @asynccontextmanager
# async def withInfo(info):
#     asyncSessionMaker = info.context["asyncSessionMaker"]
#     async with asyncSessionMaker() as session:
#         try:
#             yield session
#         finally:
#             pass

FinanceGQLModel = Annotated ["FinanceGQLModel",strawberryA.lazy(".FinanceGQLModel")]



@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance type"""
)
class FinanceTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).financetypes
    # async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
    #     loader = getLoadersFromInfo(info).financetypes
    #     result = await loader.load(id)
    #     if result is not None:
    #         result._type_definition = cls._type_definition  # little hack :)
    #     return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name en""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""List of finances, related to finance type""")
    async def finances(
        self, info: strawberryA.types.Info
    ) -> List["FinanceGQLModel"]:
        loader = getLoadersFromInfo(info).financetypes
        result = await loader.filter_by(id = self.id)
        return result
        # async with withInfo(info) as session:
        #     result = await resolveFinancesForFinanceType(session, self.id)
        #     return result
###########################################################################################################################
#
# Query 
#
###########################################################################################################################

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class FinanceTypeWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of finance types""")
async def finance_type_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[FinanceTypeWhereFilter] = None
) -> List[FinanceTypeGQLModel]:
    # async with withInfo(info) as session:
    #     result = await resolveFinanceTypeAll(session, skip, limit)
    #     return result
    loader = getLoadersFromInfo(info).financetypes
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

finance_type_by_id = createRootResolver_by_id(FinanceTypeGQLModel, description="Returns finance type by its id")

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

@strawberryA.input(description="Definition of a project used for creation")
class FinanceTypeInsertGQLModel:
    name: str = strawberryA.field(description="")

    name_en: Optional[str] = strawberryA.field(description="The name of the financial data (optional)",default=None)
    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key (UUID), could be client-generated", default=None)
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberryA.input(description="Definition of financial data used for update")
class FinanceTypeUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the financial data")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberryA.field(description="The name of the financial data (optional)",default=None)
    name_en: Optional[str] = strawberryA.field(description="The name of the financial data (optional)",default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Input structure - D operation")
class FinanceTypeDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")

@strawberryA.type(description="Result of a mutation over Project")
class FinanceTypeResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project")
    async def finance(self, info: strawberryA.types.Info) -> Union[FinanceTypeGQLModel, None]:
        result = await FinanceTypeGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.mutation(description="Adds a new project.")
async def finance_type_insert(self, info: strawberryA.types.Info, finance: FinanceTypeInsertGQLModel) -> FinanceTypeResultGQLModel:
    loader = getLoadersFromInfo(info).financetypes
    row = await loader.insert(finance)
    result = FinanceTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the finance record.")
async def finance_type_update(self, info: strawberryA.types.Info, finance: FinanceTypeUpdateGQLModel) -> FinanceTypeResultGQLModel:
    loader = getLoadersFromInfo(info).financetypes
    row = await loader.update(finance)
    result = FinanceTypeResultGQLModel()
    result.msg = "ok"
    result.id = finance.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"  
    return result

@strawberry.mutation(description="Delete the authorization user")
async def finance_type_delete(
        self, info: strawberry.types.Info, finance: FinanceTypeDeleteGQLModel
) -> FinanceTypeResultGQLModel:
    finance_type_id_to_delete = finance.id
    loader = getLoadersFromInfo(info).financetypes
    row = await loader.delete(finance_type_id_to_delete)
    result = FinanceTypeResultGQLModel(id=finance_type_id_to_delete, msg="fail, user not found") if not row else FinanceTypeResultGQLModel(id=finance_type_id_to_delete, msg="ok")
    return result