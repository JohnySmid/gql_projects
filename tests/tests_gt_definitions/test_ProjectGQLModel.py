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
    create_update_query,
    create_delete_query
)

test_reference_project = create_resolve_reference_test(table_name='projects', gqltype='ProjectGQLModel', 
                                                       attribute_names=["id", "name"])
test_query_project_by_id = create_by_id_test(table_name="projects", query_endpoint="projectById")
test_query_project_page = create_page_test(table_name="projects", query_endpoint="projectPage")

test_project_insert = create_frontend_query(query="""
    mutation ($id: UUID!, $projecttype_id: UUID!, $name: String!, $group_id: UUID, $content_id: UUID) {
        result: projectInsert(project: {id: $id, projecttypeId: $projecttype_id, name: $name, groupId: $group_id, contentId: $content_id}) {
            id
            msg
            project {
            id
            name
            startdate
            enddate
            group { 
              id 
            }
            content{
              id
            }
            team {
              id
            }
            projectType {
                id
            }
            lastchange
            finances{
              id
              name
            }
            milestones{
                id
                name
            }
            }
        }
    }
    """, 
    variables={
        "id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3",
        "name": "new project", 
        "projecttype_id": "6abcd26b-4f9b-4b49-8a5d-8ec9880acf3e",
        "group_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
        "content_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120123"
},
    asserts=[]
)

test_project_update = create_update_query(
    query="""
        mutation($id: UUID!, $projecttype_id: UUID!, $name: String!, $lastchange: DateTime!) {
            projectUpdate(project: {id: $id, projecttypeId: $projecttype_id, name: $name, lastchange: $lastchange}) {
                id
                msg
                project {
                    id
                    name
                lastchange
                }
            }
        }
    """,
    variables={
         "id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb",
        "name": "new project1", 
        "projecttype_id": "6abcd26b-4f9b-4b49-8a5d-8ec9880acf3e",
    },
    table_name="projects"
)

test_project_delete = create_delete_query (
    query="""
        mutation($id: UUID!) {
            projectDelete(project: {id: $id}) {
                id
                msg
            }
        }
    """,
    variables={
         "id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb",
    },
    table_name="projects"
)


# test_hello_project = create_frontend_query(query="""
#     query($id: UUID!){ sayHelloProjects(id: $id) }""", 
#     variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3"},
#     asserts=[]
# )