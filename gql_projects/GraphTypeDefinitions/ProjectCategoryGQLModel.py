from typing import List, Union, Annotated, Optional
import strawberry as strawberryA
import datetime
import typing
import uuid
import strawberry
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

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
    keys=["id"], 
    description="""Entity representing a project"""
)

class ProjectCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).projectcategories

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

from contextlib import asynccontextmanager
from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class ProjectCategoryWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of projects""", permission_classes=[OnlyForAuthentized()])
async def project_category_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[ProjectCategoryWhereFilter] = None
) -> List[ProjectCategoryGQLModel]:
    loader = getLoadersFromInfo(info).projectcategories
    wf = None if where is None else strawberry.asdict(where)
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
    rbacobject: strawberry.Private[uuid.UUID] = None 

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
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

@strawberryA.type(description="Result of a mutation over Project")
class ProjectCategoryResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project")
    async def project(self, info: strawberryA.types.Info) -> Union[ProjectCategoryGQLModel, None]:
        result = await ProjectCategoryGQLModel.resolve_reference(info, self.id)
        return result


@strawberryA.mutation(description="Adds a new project.", permission_classes=[OnlyForAuthentized()])
async def project_category_insert(self, info: strawberryA.types.Info, project: ProjectCategoryInsertGQLModel) -> ProjectCategoryResultGQLModel:
    # user = getUserFromInfo(info)
    # project.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projectcategories
    row = await loader.insert(project)
    result = ProjectCategoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project.", permission_classes=[OnlyForAuthentized()])
async def project_category_update(self, info: strawberryA.types.Info, project: ProjectCategoryUpdateGQLModel) -> ProjectCategoryResultGQLModel:
    # user = getUserFromInfo(info)
    # project.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projectcategories
    row = await loader.update(project)
    result = ProjectCategoryResultGQLModel()
    result.msg = "ok"
    result.id = project.id
    result.msg = "ok" if (row is not None) else "fail"
    return result
