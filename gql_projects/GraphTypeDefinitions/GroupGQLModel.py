from gql_projects.GraphResolversOLD import resolveProjectsForGroup
import strawberry as strawberryA
import uuid
from typing import Annotated, List
from contextlib import asynccontextmanager

from .BaseGQLModel import BaseGQLModel

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

ProjectGQLModel = Annotated["ProjectGQLModel",strawberryA.lazy(".ProjectGQLModel")]

@strawberryA.federation.type(
    extend=True, 
    keys=["id"], 
    description="""Entity representing a Group"""
    )

class GroupGQLModel(BaseGQLModel):
    id: uuid.UUID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""List of projects, related to group""")
    async def projects(
        self, info: strawberryA.types.Info
    ) -> List[ProjectGQLModel]:
        async with withInfo(info) as session:
            result = await resolveProjectsForGroup(session, self.id)
            return result
###########################################################################################################################
#
# Query 
#
###########################################################################################################################

