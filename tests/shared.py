# import sqlalchemy
# import sys
# import asyncio
import logging
# import pytest

# from ..uoishelpers.uuid import UUIDColumn
from gql_projects.DBDefinitions.FinanceModel import FinanceModel
from gql_projects.DBDefinitions.BaseModel import BaseModel
from gql_projects.DBDefinitions.ProjectModel import ProjectModel
from gql_projects.DBDefinitions.ProjectTypeModel import ProjectTypeModel
from gql_projects.DBDefinitions.ProjectCategoryModel import ProjectCategoryModel
from gql_projects.DBDefinitions.FinanceTypeModel import FinanceTypeModel
from gql_projects.DBDefinitions.FinanceCategory import FinanceCategory
from gql_projects.DBDefinitions.MilestoneLinkModel import MilestoneLinkModel
from gql_projects.DBDefinitions.MilestoneModel import MilestoneModel

async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    async_engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker

from gql_projects.utils.DBFeeder import get_demodata


async def prepare_demodata(async_session_maker):
    data = get_demodata()

    print(data["awauthorizations"])
    print(type(data["awauthorizations"][0]["id"]))
    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [
            ProjectModel, ProjectTypeModel, ProjectCategoryModel,
            FinanceModel, FinanceTypeModel, FinanceCategory,
            MilestoneModel, MilestoneLinkModel
        ],
        data,
    )


from gql_projects.utils.Dataloaders import createLoadersContext

def create_context(async_session_maker, with_user=True):

    loaders_context = createLoadersContext(async_session_maker)
    user = {
        "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
        "name": "John",
        "surname": "Newbie",
        "email": "john.newbie@world.com"
    }
    if with_user:
        loaders_context["user"] = user

    return loaders_context


def create_info(async_session_maker, with_user=True):
    class Request():
        @property
        def headers(self):
            return {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}

    class Info():
        @property
        def context(self):
            context = create_context(async_session_maker, with_user=with_user)
            context["request"] = Request()
            return context

    return Info()


from gql_projects.GraphTypeDefinitions import schema


def create_schema_function():
    async def result(query: str, variables: dict = None) -> dict:
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)
        context_value = create_context(async_session_maker)
        logging.debug(f"query {query} with {variables}")
        print(f"query {query} with {variables}")
        response = await schema.execute(
            query=query,
            variable_values=variables,
            context_value=context_value
        )

        assert response.errors is None, response.errors
        response_data = response.data
        logging.debug(f"response data: {response_data}")

        return {"data": response_data, "errors": response.errors}

    return result