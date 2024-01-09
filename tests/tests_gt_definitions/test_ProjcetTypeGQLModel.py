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

test_reference_projecttypes = create_resolve_reference_test(tableName='projecttypes', gqltype='ProjectTypeGQLModel', attributeNames=["id", "name", "lastchange", "category_id"])

test_query_project_type_by_id = create_by_id_test(tableName="projecttypes", queryEndpoint="projectTypeById")
test_query_project_type_page = create_page_test(tableName="projecttypes", queryEndpoint="projectTypePage")

test_insert_project_type = create_frontend_query(
    query="""mutation ($id: UUID!, $name: String!, $category_id: UUID!) {
        result: ProjectTypeInsert(project: {id: $id, name: $name, categoryId: $category_id}) {
            id
            msg
            project {
                id
                name
                projects { id }
            }
        }
    }""",
    variables={"id": "f6f79926-ac0e-4833-9a38-4272cae33fa6", "name": "new name", "category_id": "5c8c4c5a-df3b-44a9-ab90-396bdc84542b"}
)

test_update_project_type = create_update_query(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: ProjectTypeUpdate(project: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            project {
                id
                name
            }
        }
    }""",
    variables={"id": "2e1140f4-afb0-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="projecttypes"
)