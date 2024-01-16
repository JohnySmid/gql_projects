# from typing import List
# import typing

# import asyncio

# from fastapi import FastAPI
# import strawberry
# from strawberry.fastapi import GraphQLRouter

# ## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
# ## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)
# # from .gql_projects.GraphTypeDefinitions import Query

# ## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
# ## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
# ## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select
# from gql_projects.DBDefinitions import startEngine, ComposeConnectionString

# ## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# # from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes

# connectionString = ComposeConnectionString()


# def singleCall(asyncFunc):
#     """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
#     Dekorovana funkce je asynchronni.
#     """
#     resultCache = {}

#     async def result():
#         if resultCache.get("result", None) is None:
#             resultCache["result"] = await asyncFunc()
#         return resultCache["result"]

#     return result

# from gql_projects.utils.DBFeeder import initDB

# @singleCall
# async def RunOnceAndReturnSessionMaker():
#     """Provadi inicializaci asynchronniho db engine, inicializaci databaze a vraci asynchronni SessionMaker.
#     Protoze je dekorovana, volani teto funkce se provede jen jednou a vystup se zapamatuje a vraci se pri dalsich volanich.
#     """
#     print(f'starting engine for "{connectionString}"')

#     import os
#     #makedrop musel byt na tvrdo
#     makeDrop = os.environ.get("DEMO", "") == "true"
#     makeDrop = True
#     result = await startEngine(
#         connectionstring=connectionString, makeDrop=makeDrop, makeUp=True
#     )

#     print(f"initializing system structures")

#     ###########################################################################################################################
#     #
#     # zde definujte do funkce asyncio.gather
#     # vlozte asynchronni funkce, ktere maji data uvest do prvotniho konzistentniho stavu
#     await initDB(result)
#     # await asyncio.gather( # concurency running :)
#     # sem lze dat vsechny funkce, ktere maji nejak inicializovat databazi
#     # musi byt asynchronniho typu (async def ...)
#     # createSystemDataStructureRoleTypes(result),
#     # createSystemDataStructureGroupTypes(result)
#     # )

#     ###########################################################################################################################
#     print(f"all done")
#     return result


# from strawberry.asgi import GraphQL

# from gql_projects.utils.Dataloaders import createLoaders
# class MyGraphQL(GraphQL):
#     """Rozsirena trida zabezpecujici praci se session"""

#     async def __call__(self, scope, receive, send):
#         asyncSessionMaker = await RunOnceAndReturnSessionMaker()
#         async with asyncSessionMaker() as session:
#             self._session = session
#             self._user = {"id": "?"}
#             return await GraphQL.__call__(self, scope, receive, send)

#     async def get_context(self, request, response):
#         parentResult = await GraphQL.get_context(self, request, response)
#         asyncSessionMaker = await RunOnceAndReturnSessionMaker()
#         return {
#             **parentResult,
#             "session": self._session,
#             "asyncSessionMaker": asyncSessionMaker,
#             "user": self._user,
#             "loaders": createLoaders(asyncSessionMaker)
#         }


# from gql_projects.GraphTypeDefinitions import schema

# ## ASGI app, kterou "moutneme"
# graphql_app = MyGraphQL(schema, graphiql=True, allow_queries_via_get=True)

# app = FastAPI()
# app.mount("/gql", graphql_app)


# @app.on_event("startup")
# async def startup_event():
#     initizalizedEngine = await RunOnceAndReturnSessionMaker()
#     return None


# print("All initialization is done")

# # @app.get('/hello')
# # def hello():
# #    return {'hello': 'world'}

# ###########################################################################################################################
# #
# # pokud jste pripraveni testovat GQL funkcionalitu, rozsirte apollo/server.js
# #
# ###########################################################################################################################

from typing import Any, List
import logging
import os
from pydantic import BaseModel

from dotenv import load_dotenv


import logging
import logging.handlers
import socket
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
    datefmt='%Y-%m-%dT%I:%M:%S')
SYSLOGHOST = os.getenv("SYSLOGHOST", None)
if SYSLOGHOST is not None:
    [address, strport, *_] = SYSLOGHOST.split(':')
    assert len(_) == 0, f"SYSLOGHOST {SYSLOGHOST} has unexpected structure, try `localhost:514` or similar (514 is UDP port)"
    port = int(strport)
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address=(address, port), socktype=socket.SOCK_DGRAM)
    #handler = logging.handlers.SocketHandler('10.10.11.11', 611)
    my_logger.addHandler(handler)



from fastapi import FastAPI, Request, Depends
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from gql_projects.DBDefinitions import ComposeConnectionString, startEngine
from gql_projects.utils.DBFeeder import initDB

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes

connectionString = ComposeConnectionString()

appcontext = {}
@asynccontextmanager
async def initEngine(app: FastAPI):

    connectionstring = ComposeConnectionString()
    makeDrop = os.getenv("DEMO", None) == "True"
    print("MAKEDROP:", makeDrop)
    asyncSessionMaker = await startEngine(
        connectionstring=connectionstring,
        makeDrop=makeDrop,
        makeUp=True
    )

    appcontext["asyncSessionMaker"] = asyncSessionMaker

    logging.info("engine started")

    await initDB(asyncSessionMaker)

    logging.info("data (if any) imported")
    yield


from gql_projects.GraphTypeDefinitions import schema
from gql_projects.utils.Dataloaders import createLoadersContext, createUgConnectionContext 
from gql_projects.utils.sentinel import sentinel

async def get_context(request: Request):
    asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
    if asyncSessionMaker is None:
        async with initEngine(app) as cntx:
            pass
        
    context = createLoadersContext(appcontext["asyncSessionMaker"])
    i = Item(query = "")
    # i.query = ""
    # i.variables = {}
    logging.info(f"before sentinel current user is {request.scope.get('user', None)}")
    await sentinel(request, i)
    logging.info(f"after sentinel current user is {request.scope.get('user', None)}")
    connectionContext = createUgConnectionContext(request=request)
    result = {**context, **connectionContext}
    result["request"] = request
    result["user"] = request.scope.get("user", None)
    logging.info(f"context created {result}")
    return result

app = FastAPI(lifespan=initEngine)

""" from doc import attachVoyager
attachVoyager(app, path="/gql/doc") """

print("All initialization is done")
@app.get('/hello')
def hello(request: Request):
    headers = request.headers
    auth = request.auth
    user = request.scope["user"]
    return {'hello': 'world', 'headers': {**headers}, 'auth': f"{auth}", 'user': user}


graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

class Item(BaseModel):
    query: str
    variables: dict = {}
    operationName: str = None

app.include_router(graphql_app, prefix="/gql2")

@app.get("/gql")
async def graphiql(request: Request):
    return await graphql_app.render_graphql_ide(request)



@app.post("/gql")
async def apollo_gql(request: Request, item: Item):
    DEMOE = os.getenv("DEMO", None)
    # logging.info(f"apollo_gql DEMO {DEMOE} {type(DEMOE)}, {DEMO}")
    logging.info(f"asking sentinel for advice (is user authenticated?)")
    sentinelResult = await sentinel(request, item)
    if DEMOE == "False":
        if sentinelResult:
            return sentinelResult
        logging.info(f"sentinel test passed for user {request.scope['user']}")
    else:
        request.scope["user"] = {"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        logging.info(f"sentinel skippend because of DEMO mode")
    try:
        context = await get_context(request)
        logging.info(f"executing \n {item.query} \n with \n {item.variables}")
        schemaresult = await schema.execute(query=item.query, variable_values=item.variables, operation_name=item.operationName, context_value=context)
        # schemaresult = await schema.execute(query=item.query, variable_values=item.variables, context_value=context)
        # assert 1 == 0, ":)"
    except Exception as e:
        logging.info(f"error during schema execute {e}")
        return {"data": None, "errors": [f"{type(e).__name__}: {e}"]}
    
    logging.info(f"schema execute result \n{schemaresult}")
    result = {"data": schemaresult.data}
    if schemaresult.errors:
        result["errors"] = [f"{error}" for error in schemaresult.errors]
    return result

# from uoishelpers.authenticationMiddleware import BasicAuthenticationMiddleware302, BasicAuthBackend
# app.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(
#         JWTPUBLICKEY = JWTPUBLICKEY,
#         JWTRESOLVEUSERPATH = JWTRESOLVEUSERPATH
# ))

load_dotenv("environment.env")

DEMO = os.getenv('DEMO', None)
assert DEMO is not None, "DEMO environment variable must be explicitly defined"
assert (DEMO == "True") or (DEMO == "False"), "DEMO environment variable can have only `True` or `False` values"
DEMO = DEMO == "True"

if DEMO:
    print("####################################################")
    print("#                                                  #")
    print("# RUNNING IN DEMO                                  #")
    print("#                                                  #")
    print("####################################################")

    logging.info("####################################################")
    logging.info("#                                                  #")
    logging.info("# RUNNING IN DEMO                                  #")
    logging.info("#                                                  #")
    logging.info("####################################################")

if not DEMO:
    GQLUG_ENDPOINT_URL = os.getenv("GQLUG_ENDPOINT_URL", None)
    assert GQLUG_ENDPOINT_URL is not None, "GQLUG_ENDPOINT_URL environment variable must be explicitly defined"
    JWTPUBLICKEYURL = os.getenv("JWTPUBLICKEYURL", None)
    assert JWTPUBLICKEYURL is not None, "JWTPUBLICKEYURL environment variable must be explicitly defined"
    JWTRESOLVEUSERPATHURL = os.getenv("JWTRESOLVEUSERPATHURL", None)
    assert JWTRESOLVEUSERPATHURL is not None, "JWTRESOLVEUSERPATHURL environment variable must be explicitly defined"