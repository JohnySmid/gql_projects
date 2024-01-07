import pytest

from tests.tests_gt_definitions.gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_projecttypes = createResolveReferenceTest(tableName='projecttypes', gqltype='ProjectTypeGQLModel', attributeNames=["id", "name", "lastchange", "category_id"])

test_query_project_type_by_id = createByIdTest(tableName="projecttypes", queryEndpoint="projectTypeById")
test_query_project_type_page = createPageTest(tableName="projecttypes", queryEndpoint="projectTypePage")

test_insert_project_type = createFrontendQuery(
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

test_update_project_type = createUpdateQuery(
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