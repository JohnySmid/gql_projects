import strawberry as strawberryA
import uuid
from typing import List, Annotated, Optional, Union
from gql_projects.GraphResolvers import resolveFinancesForFinanceType, resolveFinanceTypeAll
from contextlib import asynccontextmanager
import datetime

import strawberry
from gql_projects.utils.DBFeeder import randomDataStructure
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

FinanceGQLModel = Annotated ["FinanceGQLModel",strawberryA.lazy(".FinanceGQLModel")]



@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance type"""
)
class FinanceTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        loader = getLoadersFromInfo(info).financetypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

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
        async with withInfo(info) as session:
            result = await resolveFinancesForFinanceType(session, self.id)
            return result
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

    name_en: Optional[str] = strawberryA.field(description="The name of the financial data (optional)")
    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key (UUID), could be client-generated", default=None)
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberryA.input(description="Definition of financial data used for update")
class FinanceTypeUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the financial data")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberryA.field(description="The name of the financial data (optional)")
    name_en: Optional[str] = strawberryA.field(description="The name of the financial data (optional)")
    changedby: strawberry.Private[uuid.UUID] = None

@strawberryA.type(description="Result of a mutation over Project")
class FinanceTypeResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project")
    async def finance(self, info: strawberryA.types.Info) -> Union[FinanceTypeGQLModel, None]:
        result = await FinanceTypeGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.mutation(description="Adds a new project.")
async def financeType_insert(self, info: strawberryA.types.Info, finance: FinanceTypeInsertGQLModel) -> FinanceTypeResultGQLModel:
    loader = getLoadersFromInfo(info).financetypes
    row = await loader.insert(finance)
    result = FinanceTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the finance record.")
async def financeType_update(self, info: strawberryA.types.Info, finance: FinanceTypeUpdateGQLModel) -> FinanceTypeResultGQLModel:
    loader = getLoadersFromInfo(info).financetypes
    row = await loader.update(finance)
    result = FinanceTypeResultGQLModel()
    result.msg = "ok"
    result.id = finance.id
    if row is None:
        result.msg = "fail"  
    return result