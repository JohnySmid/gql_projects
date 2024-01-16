from typing import List, Union, Annotated, Optional
import strawberry as strawberryA
import datetime
import typing
import uuid
import strawberry
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

from gql_projects.GraphTypeDefinitions.GraphResolvers import (
    resolve_id,
    resolve_user_id,
    resolve_accesslevel,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    resolve_rbacobject,
    createRootResolver_by_page,
)

from gql_projects.GraphPermissions import RoleBasedPermission, OnlyForAuthentized

ProjectTypeGQLModel = Annotated ["ProjectTypeGQLModel", strawberryA.lazy(".ProjectTypeGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]
ContentGQLModel = Annotated["ContentGQLModel", strawberry.lazy(".externals")]
MilestoneGQLModel = Annotated ["MilestoneGQLModel",strawberryA.lazy(".MilestoneGQLModel")]
FinanceGQLModel = Annotated ["FinanceGQLModel",strawberryA.lazy(".FinanceGQLModel")]

# def AsyncSessionFromInfo(info):
#     print(
#         "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
#     )
#     return info.context["session"]





@strawberryA.federation.type(
    keys=["id"], 
    description="""Entity representing a project"""
)
class ProjectGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).projects

    id = resolve_id
    accesslevel = resolve_accesslevel
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject

    @strawberry.field(
        description="""Form's validity""",
        permission_classes=[OnlyForAuthentized()])
    def valid(self) -> bool: return self.valid

    # def valid(self) -> bool:
    #     return self.valid

    @strawberry.field(
        description="""Form's status""",
        permission_classes=[OnlyForAuthentized()])
    def status(self) -> typing.Optional[str]: return self.status

    # def status(self) -> typing.Optional[str]:
    #     return self.status

    # async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
    #     loader = getLoadersFromInfo(info).projects
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

    @strawberryA.field(description="""Start date""")
    def startdate(self) -> datetime.date:
        return self.startdate

    @strawberryA.field(description="""End date""")
    def enddate(self) -> datetime.date:
        return self.enddate

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Project type of project""")
    async def project_type(self, info: strawberryA.types.Info) -> Optional ["ProjectTypeGQLModel"]:
        from .ProjectTypeGQLModel import ProjectTypeGQLModel  # Import here to avoid circular dependency
        result = await ProjectTypeGQLModel.resolve_reference(info, self.projecttype_id)
        return result

    @strawberryA.field(description="""List of finances, related to finance type""")
    async def finances(
        self, info: strawberryA.types.Info
    ) -> List["FinanceGQLModel"]:
        loader = getLoadersFromInfo(info).finances
        result = await loader.filter_by(project_id=self.id)
        return result
        # async with withInfo(info) as session:
        #     result = await resolveFinancesForProject(session, self.id)
        #     return result

    @strawberryA.field(description="""List of milestones, related to a project""")
    async def milestones(
        self, info: strawberryA.types.Info
    ) -> List["MilestoneGQLModel"]:
        loader = getLoadersFromInfo(info).milestones
        result = await loader.filter_by(project_id=self.id)
        return result

    # @strawberryA.field(description="""Group, related to a project""")
    # async def group(self, info: strawberryA.types.Info) -> Optional ["GroupGQLModel"]:
    #     loader = getLoadersFromInfo(info).projects
    #     result = await loader.filter_by(id=self.group_id)
    #     return result

    @strawberry.field(description="""Group, related to a project""")
    def group(self) -> Optional["GroupGQLModel"]:
        from .externals import GroupGQLModel
        return GroupGQLModel(id=self.group_id)
    
     # @strawberryA.field(description="""Team related to the project""")
    # async def team(self) -> Union["GroupGQLModel", None]:
    #     result = await GroupGQLModel.resolve_reference(self.group_id)
    #     return result
    
    @strawberry.field(description="""Team, related to a project""")
    def team(self) -> Union["GroupGQLModel", None]:
        from .externals import GroupGQLModel
        return GroupGQLModel(id=self.group_id)
    

    @strawberry.field(description="""Content, related to a project""")
    def content(self) -> Optional["ContentGQLModel"]:
        from .externals import ContentGQLModel
        return ContentGQLModel(id=self.content_id)
    
    # @strawberryA.field(description="""Finance type of finance""")
    # async def content(
    #     self, info: strawberryA.types.Info
    # ) -> List["ContentGQLModel"]:
    #     from .externals import ContentGQLModel
    #     result = ContentGQLModel(id = self.content_id)
    #     return result
    
###########################################################################################################################
#
# Query 
#
###########################################################################################################################

from contextlib import asynccontextmanager

# @asynccontextmanager
# async def withInfo(info):
#      asyncSessionMaker = info.context["asyncSessionMaker"]
#      async with asyncSessionMaker() as session:
#         try:
#             yield session
#         finally:
#             pass

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class ProjectWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str


@strawberryA.field(description="""Returns a list of projects""",
                   permission_classes=[OnlyForAuthentized()])
async def project_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[ProjectWhereFilter] = None
) -> List[ProjectGQLModel]:
    # otazka: musi tady byt async? 
    # async with withInfo(info) as session:
    loader = getLoadersFromInfo(info).projects
    wf = None if where is None else strawberry.asdict(where)
    #result = await resolveProjectAll(session, skip, limit)
    result = await loader.page(skip, limit, where = wf)
    return result
    
    
# @strawberryA.field(description="""Returns project by its id""")
# async def project_by_id(
#     self, info: strawberryA.types.Info, id: uuid.UUID
# ) -> Union[ProjectGQLModel, None]:
#     print(id)
#     async with withInfo(info) as session:
#         result = await resolveProjectById(session, id)
#         return result


project_by_id = createRootResolver_by_id(ProjectGQLModel, description="Returns project by its id")
#project_by_id = createRootResolver_by_id(ProjectGQLModel, description="Returns project by its id", permission_classes=[OnlyForAuthentized()])
    

# @strawberryA.field(description="""Returns a list of projects for group""")
# async def project_by_group(
#     self, info: strawberryA.types.Info, id: uuid.UUID
# ) -> List[ProjectGQLModel]:
#     async with withInfo(info) as session:
#         result = await resolveProjectsForGroup(session, id)
#         return result

# @strawberryA.field(description="""Random publications""")
# async def randomProject(
#     self, info: strawberryA.types.Info
# ) -> Union[ProjectGQLModel, None]:
#     async with withInfo(info) as session:
#         result = await randomDataStructure(AsyncSessionFromInfo(info))
#         return result

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################
from typing import Optional
# viz. forms - formMOdel
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
    # name: str = strawberryA.field(description="Name/label of the project")
    # lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

@strawberryA.type(description="Result of a mutation over Project")
class ProjectResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project")
    async def project(self, info: strawberryA.types.Info) -> Union[ProjectGQLModel, None]:
        result = await ProjectGQLModel.resolve_reference(info, self.id)
        return result

# changeby? createby?....

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
    user = getUserFromInfo(info)
    project.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).projects
    row = await loader.update(project)
    result = ProjectResultGQLModel()
    result.msg = "ok"
    result.id = project.id
    result.msg = "ok" if (row is not None) else "fail"
    # if row is None:
    #     result.msg = "fail"
    return result

@strawberry.mutation(description="Delete the authorization user")
async def project_delete(
        self, info: strawberry.types.Info, project: ProjectDeleteGQLModel
) -> ProjectResultGQLModel:
    project_id_to_delete = project.id
    loader = getLoadersFromInfo(info).projects
    row = await loader.delete(project_id_to_delete)
    result = ProjectResultGQLModel(id=project_id_to_delete, msg="fail, user not found") if not row else ProjectResultGQLModel(id=project_id_to_delete, msg="ok")
    return result