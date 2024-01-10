import logging
import json


def create_gql_client():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import gql_projects.DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"

    gql_projects.DBDefinitions.ComposeConnectionString = ComposeCString

    import main

    client = TestClient(main.app, raise_server_exceptions=False)

    return client


def create_client_function():
    client = create_gql_client()

    async def result(query, variables={}):
        json = {
            "query": query,
            "variables": variables
        }
        headers = {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        logging.debug(f"query client for {query} with {variables}")

        response = client.post("/gql", headers=headers, json=json)
        return response.json()

    return result


def update_introspection_query():
    from introspection import query
    client = create_gql_client()
    inputjson = {"query": query, "variables": {}}
    response = client.post("/gql", headers={}, json=inputjson)
    try:
        response.raise_for_status()  # Check for HTTP errors
        response_content = response.json()  # Try parsing response as JSON
        # Log the response content
        logging.debug(f"Response content: {response_content}")
        # Rest of your code...
    except Exception as e:
        # Handle exceptions or errors
        logging.error(f"Error processing response: {e}")


update_introspection_query()