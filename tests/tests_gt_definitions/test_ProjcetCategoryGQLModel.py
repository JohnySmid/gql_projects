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

test_reference_projectcategories = create_resolve_reference_test(tableName='projectcategories', gqltype='ProjectCategoryGQLModel', attributeNames=["id", "name", "lastchange"])

test_query_form_project_by_id = create_by_id_test(tableName="projectcategories", queryEndpoint="projectCategoryById")
test_query_form_project_page = create_page_test(tableName="projectcategories", queryEndpoint="projectCategoryPage")

test_insert_project_category = create_frontend_query(
    query="""mutation ($id: UUID!, $name: String!) {
        result: ProjectCategoryInsert(project: {id: $id, name: $name}) {
            id
            msg
            project {
                id
                name
            }
        }
    }""",
    variables={"id": "fc7f95b5-410c-4a26-a4e9-6b0b2a841645", "name": "new name"}
)

test_update_project_category = create_update_query(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: ProjectCategoryUpdate(project: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            project {
                id
                name
            }
        }
    }""",
    variables={"id": "5c8c4c5a-df3b-44a9-ab90-396bdc84542b", "name": "new name"},
    tableName="projectcategories"
)