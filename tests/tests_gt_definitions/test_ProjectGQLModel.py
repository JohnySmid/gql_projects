import pytest

from tests.tests_gt_definitions.gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_project = createResolveReferenceTest(
    tableName='projects', gqltype='ProjectGQLModel', 
    attributeNames=["id", "name", "startdate", "enddate", "projecttype_id", "projecttype", "group_id", "created {id}", "lastchange", "createdby {id}", "changedby {id}", "updatedby {id}"])
test_query_project_by_id = createByIdTest(tableName="projects", queryEndpoint="projectById")
test_query_project_page = createPageTest(tableName="projects", queryEndpoint="projectPage")

test_project_insert = createFrontendQuery(query="""
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

test_project_update = createUpdateQuery(
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

test_hello_project = createFrontendQuery(query="""
    query($id: UUID!){ sayHelloProjects(id: $id) }""", 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3"},
    asserts=[]
)