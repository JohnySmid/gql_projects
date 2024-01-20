from typing import List, Union, Annotated, Optional
import strawberry as strawberryA
import datetime
import typing
import uuid
import strawberry
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

from gql_projects.GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_startdate,
    resolve_enddate,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    resolve_rbacobject
)

from gql_projects.GraphPermissions import RoleBasedPermission, OnlyForAuthentized

ProjectTypeGQLModel = Annotated ["ProjectTypeGQLModel", strawberryA.lazy(".ProjectTypeGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
MilestoneGQLModel = Annotated ["MilestoneGQLModel",strawberryA.lazy(".MilestoneGQLModel")]
FinanceGQLModel = Annotated ["FinanceGQLModel",strawberryA.lazy(".FinanceGQLModel")]


@strawberryA.federation.type(
    keys=["id"], 
    description="""Entity representing a project"""
)
class ProjectGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).projects

    id = resolve_id
    name = resolve_name
    startdate = resolve_startdate
    enddate = resolve_enddate
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject

    # name_en = resolve_name_en
    # accesslevel = resolve_accesslevel
    # @strawberry.field(
    #     description="""Project's validity""",
    #     permission_classes=[OnlyForAuthentized()])
    # def valid(self) -> bool: return self.valid

    # def valid(self) -> bool:
    #     return self.valid

    # @strawberry.field(
    #     description="""Project's status""",
    #     permission_classes=[OnlyForAuthentized()])
    # def status(self) -> typing.Optional[str]: return self.status


    @strawberryA.field(description="""Project type of project""", permission_classes=[OnlyForAuthentized()])
    async def project_type(self, info: strawberryA.types.Info) -> Optional ["ProjectTypeGQLModel"]:
        from .ProjectTypeGQLModel import ProjectTypeGQLModel  # Import here to avoid circular dependency
        result = await ProjectTypeGQLModel.resolve_reference(info, self.projecttype_id)
        return result

    @strawberryA.field(description="""List of finances, related to finance type""", permission_classes=[OnlyForAuthentized()])
    async def finances(
        self, info: strawberryA.types.Info
    ) -> List["FinanceGQLModel"]:
        loader = getLoadersFromInfo(info).finances
        result = await loader.filter_by(project_id=self.id)
        return result

    @strawberryA.field(description="""List of milestones, related to a project""", permission_classes=[OnlyForAuthentized()])
    async def milestones(
        self, info: strawberryA.types.Info
    ) -> List["MilestoneGQLModel"]:
        loader = getLoadersFromInfo(info).milestones
        result = await loader.filter_by(project_id=self.id)
        return result

    @strawberry.field(description="""Group, related to a project""", permission_classes=[OnlyForAuthentized()])
    def group(self) -> Optional["GroupGQLModel"]:
        from .externals import GroupGQLModel
        return GroupGQLModel(id=self.group_id)
    
    
    @strawberry.field(description="""Team, related to a project""", permission_classes=[OnlyForAuthentized()])
    def team(self) -> Union["GroupGQLModel", None]:
        from .externals import GroupGQLModel
        return GroupGQLModel(id=self.group_id)
    
    
    
###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################

from contextlib import asynccontextmanager

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class ProjectWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str
    createdby: uuid.UUID


@strawberryA.field(description="""Returns a list of projects""",
                   permission_classes=[OnlyForAuthentized()])
async def project_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[ProjectWhereFilter] = None
) -> List[ProjectGQLModel]:
    loader = getLoadersFromInfo(info).projects
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result


project_by_id = createRootResolver_by_id(ProjectGQLModel, description="Returns project by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

from typing import Optional

@strawberryA.input(description="Definition of a project used for creation")
class ProjectInsertGQLModel:
    projecttype_id: uuid.UUID = strawberryA.field(description="The ID of the project type")
    name: str = strawberryA.field(description="Name/label of the project")
    
    
    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key (UUID), could be client-generated", default=None)
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Moment when the project starts (optional)", default_factory=lambda: datetime.datetime.now())
    enddate: Optional[datetime.datetime] = strawberryA.field(description="Moment when the project ends (optional)", default_factory=lambda: datetime.datetime.now())
    group_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the group associated with the project (optional)", default=None)
    content_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the content associated with the project (optional)", default=None)
    createdby: strawberry.Private[uuid.UUID] = None
    rbacobject: strawberry.Private[uuid.UUID] = None 
    
@strawberryA.input(description="Definition of a project used for update")
class ProjectUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    projecttype_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the project type (optional)",default=None)
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Moment when the project starts (optional)", default_factory=lambda: datetime.datetime.now())
    enddate: Optional[datetime.datetime] = strawberryA.field(description="Moment when the project ends (optional)", default_factory=lambda: datetime.datetime.now())
    group_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the group associated with the project (optional)", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Input structure - D operation")
class ProjectDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")

@strawberryA.type(description="Result of a mutation over Project")
class ProjectResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project")
    async def project(self, info: strawberryA.types.Info) -> Union[ProjectGQLModel, None]:
        result = await ProjectGQLModel.resolve_reference(info, self.id)
        return result


###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new project.",
                      permission_classes=[OnlyForAuthentized()])
async def project_insert(self, info: strawberryA.types.Info, project: ProjectInsertGQLModel) -> ProjectResultGQLModel:
    # user = getUserFromInfo(info)
    # project.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projects
    row = await loader.insert(project)
    result = ProjectResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project.",
                      permission_classes=[OnlyForAuthentized()])
async def project_update(self, info: strawberryA.types.Info, project: ProjectUpdateGQLModel) -> ProjectResultGQLModel:
    # user = getUserFromInfo(info)
    # project.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projects
    row = await loader.update(project)
    result = ProjectResultGQLModel()
    result.msg = "ok"
    result.id = project.id
    result.msg = "ok" if (row is not None) else "fail"
    return result
