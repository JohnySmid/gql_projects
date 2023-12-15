from typing import List, Union, Annotated, Optional
import strawberry as strawberryA
import datetime
import typing
import uuid
from gql_projects.utils.DBFeeder import randomDataStructure

from gql_projects.GraphResolvers import (
    resolveProjectAll,
    resolveProjectById,
    resolveProjectsForGroup
)

ProjectTypeGQLModel = Annotated ["ProjectTypeGQLModel", strawberryA.lazy(".ProjectTypeGQLModel")]
GroupGQLModel = Annotated ["GroupGQLModel",strawberryA.lazy(".GroupGQLModel")]
MilestoneGQLModel = Annotated ["MilestoneGQLModel",strawberryA.lazy(".MilestoneGQLModel")]
FinanceGQLModel = Annotated ["FinanceGQLModel",strawberryA.lazy(".FinanceGQLModel")]

def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]


def getLoaders(info):
    return info.context['all']


@strawberryA.federation.type(
    keys=["id"], 
    description="""Entity representing a project"""
)
class ProjectGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        loader = getLoaders(info).projects
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

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

    @strawberryA.field(description="""Team related to the project""")
    async def team(self) -> Union["GroupGQLModel", None]:
        result = await GroupGQLModel.resolve_reference(self.group_id)
        return result

    @strawberryA.field(description="""Project type of project""")
    async def project_type(self, info: strawberryA.types.Info) -> Optional ["ProjectTypeGQLModel"]:
        from .ProjectTypeGQLModel import ProjectTypeGQLModel  # Import here to avoid circular dependency
        result = await ProjectTypeGQLModel.resolve_reference(info, self.projecttype_id)
        return result

    @strawberryA.field(description="""List of finances, related to a project""")
    async def finances(
        self, info: strawberryA.types.Info
    ) -> Optional["FinanceGQLModel"]:
        loader = getLoaders(info).finances
        result = await loader.filter_by(id=self.id)
        return result

    @strawberryA.field(description="""List of milestones, related to a project""")
    async def milestones(
        self, info: strawberryA.types.Info
    ) -> List["MilestoneGQLModel"]:
        loader = getLoaders(info).milestones
        result = await loader.filter_by(project_id=self.id)
        return result

    @strawberryA.field(description="""Group, related to a project""")
    async def group(self, info: strawberryA.types.Info) -> Optional ["GroupGQLModel"]:
        loader = getLoaders(info).projects
        result = await loader.filter_by(id=self.group_id)
        return result
    
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

@strawberryA.field(description="""Returns a list of projects""")
async def project_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
) -> List[ProjectGQLModel]:
    async with withInfo(info) as session:
        result = await resolveProjectAll(session, skip, limit)
        return result
    
    
@strawberryA.field(description="""Returns project by its id""")
async def project_by_id(
    self, info: strawberryA.types.Info, id: uuid.UUID
) -> Union[ProjectGQLModel, None]:
    print(id)
    async with withInfo(info) as session:
        result = await resolveProjectById(session, id)
        return result
@strawberryA.field(description="""Returns a list of projects for group""")
async def project_by_group(
    self, info: strawberryA.types.Info, id: uuid.UUID
) -> List[ProjectGQLModel]:
    async with withInfo(info) as session:
        result = await resolveProjectsForGroup(session, id)
        return result

@strawberryA.field(description="""Random publications""")
async def randomProject(
    self, info: strawberryA.types.Info
) -> Union[ProjectGQLModel, None]:
    async with withInfo(info) as session:
        result = await randomDataStructure(AsyncSessionFromInfo(info))
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
class ProjectInsertGQLModel:
    projecttype_id: uuid.UUID = strawberryA.field(description="The ID of the project type")
    name: str = strawberryA.field(description="Name/label of the project")

    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key (UUID), could be client-generated", default=None)
    name: Optional[str] = strawberryA.field(description="The name of the project (optional)", default="Project")
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Moment when the project starts (optional)", default_factory=lambda: datetime.datetime.now())
    enddate: Optional[datetime.datetime] = strawberryA.field(description="Moment when the project ends (optional)", default_factory=lambda: datetime.datetime.now())

    group_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the group associated with the project (optional)", default=None)

@strawberryA.input(description="Definition of a project used for update")
class ProjectUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project")
    name: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    projecttype_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the project type (optional)",default=None)
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Moment when the project starts (optional)", default_factory=lambda: datetime.datetime.now())
    enddate: Optional[datetime.datetime] = strawberryA.field(description="Moment when the project ends (optional)", default_factory=lambda: datetime.datetime.now())
    group_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the group associated with the project (optional)", default=None)

@strawberryA.type(description="Result of a mutation over Project")
class ProjectResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project")
    async def project(self, info: strawberryA.types.Info) -> Union[ProjectGQLModel, None]:
        result = await ProjectGQLModel.resolve_reference(info, self.id)
        return result



@strawberryA.mutation(description="Adds a new project.")
async def project_insert(self, info: strawberryA.types.Info, project: ProjectInsertGQLModel) -> ProjectResultGQLModel:
    loader = getLoaders(info).projects
    row = await loader.insert(project)
    result = ProjectResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project.")
async def project_update(self, info: strawberryA.types.Info, project: ProjectUpdateGQLModel) -> ProjectResultGQLModel:
    loader = getLoaders(info).projects
    row = await loader.update(project)
    result = ProjectResultGQLModel()
    result.msg = "ok"
    result.id = project.id
    if row is None:
        result.msg = "fail"
    return result