import uuid
import strawberry as strawberryA
from typing import List, Annotated, Optional, Union
from contextlib import asynccontextmanager
import datetime
from .BaseGQLModel import BaseGQLModel
import strawberry
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

from gql_projects.GraphPermissions import RoleBasedPermission, OnlyForAuthentized

from gql_projects.GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    resolve_rbacobject,
    resolve_valid
)

ProjectGQLModel = Annotated["ProjectGQLModel",strawberryA.lazy(".ProjectGQLModel")]
ProjectCategoryGQLModel = Annotated["ProjectCategoryGQLModel",strawberryA.lazy(".ProjectCategoryGQLModel")]



@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a project types"""
)
class ProjectTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).projecttypes

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject
    valid = resolve_valid
    
    @strawberryA.field(description="""List of projects, related to project type""", permission_classes=[OnlyForAuthentized()])
    async def projects(self, info: strawberryA.types.Info) -> List["ProjectGQLModel"]:
        loader = getLoadersFromInfo(info).projecttypes
        result = await loader.filter_by(id = self.id)
        return result
        
    @strawberryA.field(description="""Category ID of project, related to project""", permission_classes=[OnlyForAuthentized()])
    async def category(self, info: strawberryA.types.Info) -> Optional ["ProjectCategoryGQLModel"]:
        from .ProjectCategoryGQLModel import ProjectCategoryGQLModel  # Import here to avoid circular dependency
        result = await ProjectCategoryGQLModel.resolve_reference(info, self.category_id)
        return result

    # startdate = resolve_startdate
    # enddate = resolve_enddate
    # accesslevel = resolve_accesslevel

###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class ProjectTypeWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str
    valid: bool

@strawberryA.field(description="""Returns a list of project types""", permission_classes=[OnlyForAuthentized()])
async def project_type_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[ProjectTypeWhereFilter] = None
) -> List[ProjectTypeGQLModel]:
    loader = getLoadersFromInfo(info).projecttypes
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

project_type_by_id = createRootResolver_by_id(ProjectTypeGQLModel, description="Returns project type by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.input(description="Definition of a project used for creation")
class ProjectTypeInsertGQLModel:
    category_id: uuid.UUID = strawberryA.field(description="")
    name: str = strawberryA.field(description="")

    valid: Optional[bool] = True
    name_en: str = strawberryA.field(description="", default=None)
    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key (UUID), could be client-generated", default=None)
    createdby: strawberry.Private[uuid.UUID] = None 
    rbacobject: strawberry.Private[uuid.UUID] = None 

@strawberryA.input(description="Definition of a project used for update")
class ProjectTypeUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    valid: Optional[bool] = None
    name: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    name_en: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    changedby: strawberry.Private[uuid.UUID] = None


# @strawberry.input(description="Input structure - D operation")
# class ProjectTypeDeleteGQLModel:
#     id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
#     lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")


@strawberryA.type(description="Result of a mutation over Project")
class ProjectTypeResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project", permission_classes=[OnlyForAuthentized()])
    async def project(self, info: strawberryA.types.Info) -> Union[ProjectTypeGQLModel, None]:
        result = await ProjectTypeGQLModel.resolve_reference(info, self.id)
        return result

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new project.", permission_classes=[OnlyForAuthentized()])
async def project_type_insert(self, info: strawberryA.types.Info, project: ProjectTypeInsertGQLModel) -> ProjectTypeResultGQLModel:
    user = getUserFromInfo(info)
    project.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projecttypes
    row = await loader.insert(project)
    result = ProjectTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project.", permission_classes=[OnlyForAuthentized()])
async def project_type_update(self, info: strawberryA.types.Info, project: ProjectTypeUpdateGQLModel) -> ProjectTypeResultGQLModel:
    user = getUserFromInfo(info)
    project.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projecttypes
    row = await loader.update(project)
    result = ProjectTypeResultGQLModel()
    result.msg = "ok"
    result.id = project.id
    result.msg = "ok" if (row is not None) else "fail"
    return result


# @strawberry.mutation(description="""Deletes already existing preference settings 
#                      rrequires ID and lastchange""", permission_classes=[OnlyForAuthentized()])
# async def project_type_delete(self, info: strawberry.types.Info, project: ProjectTypeDeleteGQLModel) -> ProjectTypeResultGQLModel:
#     loader = getLoadersFromInfo(info).projecttypes
#     user = getUserFromInfo(info)
#     project.changedby = uuid.UUID(user["id"])
#     id_for_resposne = project.id
#     row = await loader.delete(id_for_resposne)
#     result = ProjectTypeResultGQLModel(id=id_for_resposne, msg="fail, user not found") if not row else ProjectTypeResultGQLModel(id=id_for_resposne, msg="ok")
#     return result