import pytest

from tests.shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    create_context,
)

from tests.gqlshared import (
    create_by_id_test,
    create_page_test,
    create_resolve_reference_test,
    create_frontend_query,
    create_update_query
)

test_reference_project = create_resolve_reference_test(
    tableName='projects', gqltype='ProjectGQLModel', 
    attributeNames=["id", "name", "startdate", "enddate", "projecttype_id", "projecttype", "group_id", "created {id}", "lastchange", "createdby {id}", "changedby {id}", "updatedby {id}"])
test_query_project_by_id = create_by_id_test(tableName="projects", queryEndpoint="projectById")
test_query_project_page = create_page_test(tableName="projects", queryEndpoint="projectPage")

test_project_insert = create_frontend_query(query="""
    mutation($id: UUID!,$projecttype_id: UUID!, $name: String!) { 
        result: ProjectInsert(project: {id: $id, projecttypeId: $projecttype_id, name: $name}) { 
            id
            msg
            project {
                id
                name
                projecttype { id }

                lastchange
                created
                changedby { id }              
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new project", "projecttype_id": "6abcd26b-4f9b-4b49-8a5d-8ec9880acf3e"},
    asserts=[]
)

test_project_update = create_update_query(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            ProjectUpdate(project: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                project {
                    id
                    name
                }
            }
        }
    """,
    variables={"id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb", "name": "new name"},
    tableName="projects"
)

test_hello_project = create_frontend_query(query="""
    query($id: UUID!){ sayHelloProjects(id: $id) }""", 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3"},
    asserts=[]
)