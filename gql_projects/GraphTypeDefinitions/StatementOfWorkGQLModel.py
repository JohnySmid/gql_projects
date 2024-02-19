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
    resolve_startdate,
    resolve_enddate,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    resolve_rbacobject,
    resolve_valid
)

ProjectGQLModel = Annotated["ProjectGQLModel",strawberryA.lazy(".ProjectGQLModel")]
EventGQLModel = Annotated["EventGQLModel", strawberry.lazy(".externals")]

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a SOW"""
)
class StatementOfWorkGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).statementofwork

    id = resolve_id
    lastchange = resolve_lastchange
    startdate = resolve_startdate
    enddate = resolve_enddate
    #name = resolve_name

    created = resolve_created
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject
    valid = resolve_valid
    
   #project_id
    @strawberryA.field(description="""Project of milestone""", permission_classes=[OnlyForAuthentized()])
    async def project(self, info: strawberryA.types.Info) -> Optional ["ProjectGQLModel"]:
        loader = getLoadersFromInfo(info).projects
        result = await loader.load(self.project_id)
        return result
    
    #event_id
    @strawberry.field(description="""Team, related to a project""", permission_classes=[OnlyForAuthentized()])
    def event(self) -> Union["EventGQLModel", None]:
        from .externals import EventGQLModel
        return EventGQLModel(id=self.event_id)
    
###########################################################################################################################
#                                                                                                                         #
#                                                       Query                                                             #
#                                                                                                                         #
###########################################################################################################################

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass
class StatementOfWorkWhereFilter:
    #name: str
    id: uuid.UUID
    value: str
    valid: bool

@strawberryA.field(description="""Returns a list of project types""", permission_classes=[OnlyForAuthentized()])
async def statement_of_work_page(
    self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[StatementOfWorkWhereFilter] = None
) -> List[StatementOfWorkGQLModel]:
    loader = getLoadersFromInfo(info).statementofwork
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result

statement_of_work_by_id = createRootResolver_by_id(StatementOfWorkGQLModel, description="Returns SOW by its id")

###########################################################################################################################
#                                                                                                                         #
#                                                       Models                                                            #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.input(description="Definition of a project used for creation")
class StatementOfWorkInsertGQLModel:
    event_id: uuid.UUID = strawberryA.field(description="")
    project_id: uuid.UUID = strawberryA.field(description="")
    
    #name: Optional[str] = strawberryA.field(description="The name of the SOW (optional)", default=None)
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Start date of the milestone (optional)", default=datetime.datetime.now())
    enddate: Optional[datetime.datetime] = strawberryA.field(description="End date of the milestone (optional)", default=datetime.datetime.now() + datetime.timedelta(days=30))
    
    valid: Optional[bool] = True
    id: Optional[uuid.UUID] = strawberryA.field(description="Primary key (UUID), could be client-generated", default=None)
    createdby: strawberry.Private[uuid.UUID] = None 
    rbacobject: strawberry.Private[uuid.UUID] = None 

@strawberryA.input(description="Definition of a project used for update")
class StatementOfWorkUpdateGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    valid: Optional[bool] = None
    #name: Optional[str] = strawberryA.field(description="The name of the SOW (optional)", default=None)
    project_id: Optional[uuid.UUID] = strawberryA.field(description="The ID of the project type (optional)",default=None)
    startdate: Optional[datetime.datetime] = strawberryA.field(description="Start date of the milestone (optional)",default=None)
    enddate: Optional[datetime.datetime] = strawberryA.field(description="End date of the milestone (optional)",default=None)
    changedby: strawberry.Private[uuid.UUID] = None


@strawberry.input(description="Input structure - D operation")
class StatementOfWorkDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")


@strawberryA.type(description="Result of a mutation over Project")
class StatementOfWorkResultGQLModel:
    id: uuid.UUID = strawberryA.field(description="The ID of the project", default=None)
    msg: str = strawberryA.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberryA.field(description="Returns the project", permission_classes=[OnlyForAuthentized()])
    async def statementofwork(self, info: strawberryA.types.Info) -> Union[StatementOfWorkGQLModel, None]:
        result = await StatementOfWorkGQLModel.resolve_reference(info, self.id)
        return result

###########################################################################################################################
#                                                                                                                         #
#                                                       Mutations                                                         #
#                                                                                                                         #
###########################################################################################################################

@strawberryA.mutation(description="Adds a new project.", permission_classes=[OnlyForAuthentized()])
async def statement_of_work_insert(self, info: strawberryA.types.Info, statementofwork: StatementOfWorkInsertGQLModel) -> StatementOfWorkResultGQLModel:
    # user = getUserFromInfo(info)
    # statementofwork.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).statementofwork
    row = await loader.insert(statementofwork)
    result = StatementOfWorkResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberryA.mutation(description="Update the project.", permission_classes=[OnlyForAuthentized()])
async def statement_of_work_update(self, info: strawberryA.types.Info, statementofwork: StatementOfWorkUpdateGQLModel) -> StatementOfWorkResultGQLModel:
    # user = getUserFromInfo(info)
    # statementofwork.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).statementofwork
    row = await loader.update(statementofwork)
    result = StatementOfWorkResultGQLModel()
    result.msg = "ok"
    result.id = statementofwork.id
    result.msg = "ok" if (row is not None) else "fail"
    return result

