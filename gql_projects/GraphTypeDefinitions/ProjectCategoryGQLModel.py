from typing import List, Union, Annotated, Optional
import strawberry as strawberryA
import datetime
import typing
import uuid
import strawberry
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

# from gql_projects.GraphResolvers import (
#     resolveProjectAll,
#     resolveProjectById,
#     resolveProjectsForGroup,
#     resolveFinancesForProject
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

@strawberryA.federation.type(
    keys=["id"], 
    description="""Entity representing a project"""
)

class ProjectCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).projectcategories
    # async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
    #     loader = getLoadersFromInfo(info).projectcategories
    #     result = await loader.load(id)
    #     if result is not None:
    #         result._type_definition = cls._type_definition  # little hack :)
    #     return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""Name of the project""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name en""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

###########################################################################################################################
#
# Query 
#
###########################################################################################################################

from contextlib import asynccontextmanager

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
class ProjectCategoryWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of projects""")
async def project_category_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[ProjectCategoryWhereFilter] = None
) -> List[ProjectCategoryGQLModel]:
    # otazka: musi tady byt async? 
    # async with withInfo(info) as session:
    loader = getLoadersFromInfo(info).projectcategories
    wf = None if where is None else strawberry.asdict(where)
    #result = await resolveProjectAll(session, skip, limit)
    result = await loader.page(skip, limit, where = wf)
    return result

project_category_by_id = createRootResolver_by_id(ProjectCategoryGQLModel, description="Returns project category by its id")

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################
from typing import Optional

@strawberryA.input(description="Definition of a project used for creation")
class ProjectCategoryInsertGQLModel:
    name: str = strawberryA.field(description="Name/label of the project")
    
    name_en: str = strawberryA.field(description="", default=None)
    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key (UUID), could be client-generated", default=None)
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberryA.input(description="Definition of a project used for update")
class ProjectCategoryUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    name_en: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Input structure - D operation")
class ProjectCategoryDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    # name: str = strawberryA.field(description="Name/label of the project")
    # lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

@strawberryA.type(description="Result of a mutation over Project")
class ProjectCategoryResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project")
    async def project(self, info: strawberryA.types.Info) -> Union[ProjectCategoryGQLModel, None]:
        result = await ProjectCategoryGQLModel.resolve_reference(info, self.id)
        return result


@strawberryA.mutation(description="Adds a new project.")
async def project_category_insert(self, info: strawberryA.types.Info, project: ProjectCategoryInsertGQLModel) -> ProjectCategoryResultGQLModel:
    # user = getUserFromInfo(info)
    # project.createdby = uuid.UUID(user["id"])

    loader = getLoadersFromInfo(info).projectcategories
    row = await loader.insert(project)
    result = ProjectCategoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project.")
async def project_category_update(self, info: strawberryA.types.Info, project: ProjectCategoryUpdateGQLModel) -> ProjectCategoryResultGQLModel:
    # user = getUserFromInfo(info)
    # project.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projectcategories
    row = await loader.update(project)
    result = ProjectCategoryResultGQLModel()
    result.msg = "ok"
    result.id = project.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"
    return result

@strawberry.mutation(description="Delete the authorization user")
async def project_category_delete(
        self, info: strawberry.types.Info, project: ProjectCategoryDeleteGQLModel
) -> ProjectCategoryResultGQLModel:
    project_category_id_to_delete = project.id
    loader = getLoadersFromInfo(info).projectcategories
    row = await loader.delete(project_category_id_to_delete)
    result = ProjectCategoryResultGQLModel(id=project_category_id_to_delete, msg="fail, user not found") if not row else ProjectCategoryResultGQLModel(id=project_category_id_to_delete, msg="ok")
    return result