import asyncio
import strawberry as strawberryA
from typing import List, Annotated, Optional, Union
import datetime
import uuid
# from gql_projects.GraphResolvers import (
#     resolveProjectById,
#     resolveMilestoneAll
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
from contextlib import asynccontextmanager
from .ProjectGQLModel import ProjectResultGQLModel
from .BaseGQLModel import BaseGQLModel

import strawberry
from gql_projects.utils.DBFeeder import randomDataStructure
from gql_projects.utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

# @asynccontextmanager
# async def withInfo(info):
#     asyncSessionMaker = info.context["asyncSessionMaker"]
#     async with asyncSessionMaker() as session:
#         try:
#             yield session
#         finally:
#             pass

ProjectGQLModel = Annotated["ProjectGQLModel",strawberryA.lazy(".ProjectGQLModel")]




@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a milestone"""
)
class MilestoneGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).milestones
    
    # async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
    #     loader = getLoadersFromInfo(info).milestones
    #     result = await loader.load(id)
    #     if result is not None:
    #         result._type_definition = cls._type_definition  # little hack :)
    #     return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="""Time stamp""")
    def lastchange(self) -> uuid.UUID:
        return self.lastchange

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Start date""")
    def startdate(self) -> datetime.date:
        return self.startdate

    @strawberryA.field(description="""End date""")
    def enddate(self) -> datetime.date:
        return self.enddate

    @strawberryA.field(description="""Last change""")
    def lastChange(self) -> datetime.datetime:
        return self.lastChange

    @strawberryA.field(description="""Project of milestone""")
    async def project(self, info: strawberryA.types.Info) -> Optional ["ProjectGQLModel"]:
        loader = getLoadersFromInfo(info).projects
        result = await loader.load(self.project_id)
        return result
        # async with withInfo(info) as session:
        #     result = await resolveProjectById(session, self.project_id)
        #     return result

    @strawberryA.field(description="""Milestones which has this one as follower""")
    async def previous(self, info: strawberryA.types.Info) -> List["MilestoneGQLModel"]:
        # async with withInfo(info) as session:
        #     result = await resolveProjectById(session, self.project_id)
        #     return result
        loader = getLoadersFromInfo(info).milestonelinks
        rows = await loader.filter_by(next_id=self.id)
        awaitable = (MilestoneGQLModel.resolve_reference(info, row.previous_id) for row in rows)
        return await asyncio.gather(*awaitable)

    @strawberryA.field(description="""Milestone which follow this milestone""")
    async def nexts(self, info: strawberryA.types.Info) -> List["MilestoneGQLModel"]:
        # async with withInfo(info) as session:
        #     result = await resolveProjectById(session, self.project_id)
        #     return result
        loader = getLoadersFromInfo(info).milestonelinks
        rows = await loader.filter_by(previous_id=self.id)
        awaitable = (MilestoneGQLModel.resolve_reference(info, row.next_id) for row in rows)
        return await asyncio.gather(*awaitable)
    
###########################################################################################################################
#
# Query 
#
###########################################################################################################################

from dataclasses import dataclass
from .utils import createInputs
@createInputs
@dataclass
class MilestoneWhereFilter:
    name: str
    type_id: uuid.UUID
    value: str

@strawberryA.field(description="""Returns a list of milestones""")
async def milestone_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[MilestoneWhereFilter] = None
) -> List[MilestoneGQLModel]:
    # async with withInfo(info) as session:
    #     result = await resolveMilestoneAll(session, skip, limit)
    #     return result
    loader = getLoadersFromInfo(info).milestones
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

milestone_by_id = createRootResolver_by_id(MilestoneGQLModel, description="Returns milestone by its id")

###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

@strawberryA.input(description="Definition of a milestone used for insertion")
class MilestoneInsertGQLModel:
    name: str = strawberryA.field(description="Name of the milestone")
    project_id: uuid.UUID = strawberryA.field(description="The ID of the associated project")
    
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Start date of the milestone (optional)", default=datetime.datetime.now())
    enddate: Optional[datetime.datetime] = strawberryA.field(description="End date of the milestone (optional)", default=datetime.datetime.now() + datetime.timedelta(days=30))
    id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the milestone (optional)",default=None)

@strawberryA.input(description="Definition of a milestone used for update")
class MilestoneUpdateGQLModel:
    lastchange: datetime.datetime = strawberryA.field(description="Timestamp of the last change")
    id: uuid.UUID = strawberryA.field(description="The ID of the milestone")
    name: Optional[str] = strawberryA.field(description="The name of the milestone (optional)",default=None)
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Start date of the milestone (optional)",default=None)
    enddate: Optional[datetime.datetime] = strawberryA.field(description="End date of the milestone (optional)",default=None)
    
@strawberryA.type(description="Result of a user operation on a milestone")
class MilestoneResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the milestone", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the milestone")
    async def milestone(self, info: strawberryA.types.Info) -> Union[MilestoneGQLModel, None]:
        result = await MilestoneGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input(description="Definition of milestone link used for addition")
class MilestoneLinkAddGQLModel:
    previous_id: uuid.UUID = strawberryA.field(description="The ID of the previous milestone")
    next_id: uuid.UUID = strawberryA.field(description="The ID of the next milestone")

@strawberryA.mutation(description="Adds a new milestones link.")
async def milestones_link_add(self, info: strawberryA.types.Info, link: MilestoneLinkAddGQLModel) -> MilestoneResultGQLModel:
    loader = getLoadersFromInfo(info).milestonelinks
    rows = await loader.filter_by(previous_id=link.previous_id, next_id=link.next_id)
    row = next(rows, None)
    result = MilestoneResultGQLModel()
    if row is None:
        row = await loader.insert(link)
        result.msg = "ok"
    else:
        result.msg = "exists"
    result.id = link.previous_id
    return result

@strawberryA.mutation(description="Removes the milestones link.")
async def milestones_link_remove(self, info: strawberryA.types.Info, link: MilestoneLinkAddGQLModel) -> MilestoneResultGQLModel:
    loader = getLoadersFromInfo(info).milestonelinks
    rows = await loader.filter_by(previous_id=link.previous_id, next_id=link.next_id)
    row = next(rows, None)
    result = MilestoneResultGQLModel()
    if row is None:
        result.msg = "fail"
    else:
        await loader.delete(row.id)
        result.msg = "ok"
    result.id = link.previous_id
    return result

@strawberryA.mutation(description="Adds a new milestone.")
async def milestone_insert(self, info: strawberryA.types.Info, milestone: MilestoneInsertGQLModel) -> MilestoneResultGQLModel:
    loader = getLoadersFromInfo(info).milestones
    row = await loader.insert(milestone)
    result = MilestoneResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the milestone.")
async def milestone_update(self, info: strawberryA.types.Info, milestone: MilestoneUpdateGQLModel) -> MilestoneResultGQLModel:
    loader = getLoadersFromInfo(info).milestones
    row = await loader.update(milestone)
    result = MilestoneResultGQLModel()
    result.msg = "ok"
    result.id = milestone.id
    if row is None:
        result.msg = "fail"  
    return result

@strawberryA.mutation(description="Delete the milestone.")
async def milestone_delete(self, info: strawberryA.types.Info, id: uuid.UUID) -> ProjectResultGQLModel:
    loader = getLoadersFromInfo(info).milestonelinks
    rows = await loader.filter_by(previous_id=id)
    linksids = [row.id for row in rows]
    rows = await loader.filter_by(next_id=id)
    linksids.extend([row.id for row in rows])
    for id in linksids:
        await loader.delete(id)

    loader = getLoadersFromInfo(info).milestones
    row = await loader.load(id)
    result = ProjectResultGQLModel()
    result.id = row.project_id
    await loader.delete(id)       
    result.msg = "ok"
    return result