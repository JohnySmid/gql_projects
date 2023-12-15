import uuid
import strawberry as strawberryA
from typing import List, Annotated, Optional, Union
from contextlib import asynccontextmanager

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

from gql_projects.GraphResolvers import (
    resolveProjectsForProjectType,
    resolveProjectTypeAll
)

ProjectGQLModel = Annotated["ProjectGQLModel",strawberryA.lazy(".ProjectGQLModel")]


def getLoaders(info):
    return info.context['all']



@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a project types"""
)
class ProjectTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        loader = getLoaders(info).projecttypes
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

    @strawberryA.field(description="""List of projects, related to project type""")
    async def projects(self, info: strawberryA.types.Info) -> List["ProjectGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveProjectsForProjectType(session, self.id)
            return result
        
###########################################################################################################################
#
# Query 
#
###########################################################################################################################

@strawberryA.field(description="""Returns a list of project types""")
async def project_type_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
) -> List[ProjectTypeGQLModel]:
    async with withInfo(info) as session:
        result = await resolveProjectTypeAll(session, skip, limit)
        return result

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

@strawberryA.input(description="Definition of a project used for creation")
class ProjectTypeInsertGQLModel:
    projecttype_id: uuid.UUID = strawberryA.field(description="")
    name: str = strawberryA.field(description="")
    name_en: str = strawberryA.field(description="")

    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key (UUID), could be client-generated", default=None)
    

@strawberryA.input(description="Definition of a project used for update")
class ProjectTypeUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project")
    name: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)
    name_en: Optional[str] = strawberryA.field(description="The name of the project (optional)", default=None)

@strawberryA.type(description="Result of a mutation over Project")
class ProjectTypeResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project")
    async def project(self, info: strawberryA.types.Info) -> Union[ProjectTypeGQLModel, None]:
        result = await ProjectTypeGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.mutation(description="Adds a new project.")
async def projectType_insert(self, info: strawberryA.types.Info, project: ProjectTypeInsertGQLModel) -> ProjectTypeResultGQLModel:
    loader = getLoaders(info).projecttypes
    row = await loader.insert(project)
    result = ProjectTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project.")
async def projectType_update(self, info: strawberryA.types.Info, project: ProjectTypeUpdateGQLModel) -> ProjectTypeResultGQLModel:
    loader = getLoaders(info).projecttypes
    row = await loader.update(project)
    result = ProjectTypeResultGQLModel()
    result.msg = "ok"
    result.id = project.id
    if row is None:
        result.msg = "fail"
    return result