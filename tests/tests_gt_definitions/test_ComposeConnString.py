import os
from gql_projects.DBDefinitions import ComposeConnectionString, startEngine

def test_ComposeConnectionString():
    os.environ["POSTGRES_USER"] = "test_user"
    os.environ["POSTGRES_PASSWORD"] = "test_password"
    os.environ["POSTGRES_DB"] = "test_db"
    os.environ["POSTGRES_HOST"] = "test_host:5432"

    # Get connection string
    connection_string = ComposeConnectionString()

   
    expected_connection_string = "postgresql+asyncpg://test_user:test_password@test_host:5432/test_db"
    assert connection_string == expected_connection_string
    #delete variables
    del os.environ["POSTGRES_USER"]
    del os.environ["POSTGRES_PASSWORD"]
    del os.environ["POSTGRES_DB"]
    del os.environ["POSTGRES_HOST"]