import strawberry as strawberryA
import datetime
import uuid
from typing import List, Annotated, Optional, Union
from .BaseGQLModel import BaseGQLModel

import strawberry
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

from gql_projects.GraphPermissions import RoleBasedPermission, OnlyForAuthentized

from gql_projects.GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_user_id,
    resolve_accesslevel,
    resolve_amount,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    createRootResolver_by_page,
    resolve_rbacobject
)

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance"""
)
class FinanceCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).financecategory
    
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject

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
class FinanceCategoryWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of projects""", permission_classes=[OnlyForAuthentized()])
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

finance_category_by_id = createRootResolver_by_id(FinanceCategoryGQLModel, description="Returns finance category by its id")

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
    rbacobject: strawberry.Private[uuid.UUID] = None 

@strawberryA.input(description="Definition of a project used for update")
class FinanceCategoryUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    name_en: Optional[str] = strawberryA.field(description="", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Input structure - D operation")
class FinanceCategoryDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")


@strawberryA.type(description="Result of a mutation over Project")
class FinanceCategoryResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project", permission_classes=[OnlyForAuthentized()])
    async def project(self, info: strawberryA.types.Info) -> Union[FinanceCategoryGQLModel, None]:
        result = await FinanceCategoryGQLModel.resolve_reference(info, self.id)
        return result


@strawberryA.mutation(description="Adds a new project.", permission_classes=[OnlyForAuthentized()])
async def finance_category_insert(self, info: strawberryA.types.Info, finance: FinanceCategoryInsertGQLModel) -> FinanceCategoryResultGQLModel:
    # user = getUserFromInfo(info)
    # project.createdby = uuid.UUID(user["id"])

    loader = getLoadersFromInfo(info).financecategory
    row = await loader.insert(finance)
    result = FinanceCategoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project.", permission_classes=[OnlyForAuthentized()])
async def finance_category_update(self, info: strawberryA.types.Info, finance: FinanceCategoryUpdateGQLModel) -> FinanceCategoryResultGQLModel:
    # user = getUserFromInfo(info)
    # project.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).financecategory
    row = await loader.update(finance)
    result = FinanceCategoryResultGQLModel()
    #result.msg = "ok" if (row not None) else result.msg = "fail"
    result.msg = "ok" if (row is not None) else "fail"
    result.id = finance.id
    # if row is None:
    #     result.msg = "fail"
    return result


# @strawberry.mutation(description="Delete the authorization user")
# async def finance_category_delete(
#         self, info: strawberry.types.Info, finance: FinanceCategoryDeleteGQLModel
# ) -> FinanceCategoryResultGQLModel:
#     finance_category_id_to_delete = finance.id
#     loader = getLoadersFromInfo(info).financecategory
#     row = await loader.delete(finance_category_id_to_delete)
#     result = FinanceCategoryResultGQLModel(id=finance_category_id_to_delete, msg="fail, user not found") if not row else FinanceCategoryResultGQLModel(id=finance_category_id_to_delete, msg="ok")
#     return result


# @strawberry.mutation(description="""Deletes already existing preference settings 
#                      rrequires ID and lastchange""", permission_classes=[OnlyForAuthentized()] )
# async def finance_category_delete(self, info: strawberry.types.Info, finance: FinanceCategoryDeleteGQLModel) -> FinanceCategoryResultGQLModel:

#     loader = getLoadersFromInfo(info).financecategory

#     rows = await loader.filter_by(id=finance.id)
#     row = next(rows, None)
#     if row is None:     
#         return FinanceCategoryResultGQLModel(id=finance.id, msg="Fail bad ID")

#     rows = await loader.filter_by(lastchange=finance.lastchange)
#     row = next(rows, None)
#     if row is None:     
#         return FinanceCategoryResultGQLModel(id=finance.id, msg="Fail (bad lastchange?)")
    
#     await loader.delete(finance.id)
#     return FinanceCategoryResultGQLModel(id=finance.id, msg="OK, deleted")