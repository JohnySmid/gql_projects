import pytest

from tests.tests_gt_definitions.gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)


test_reference_projectcategories = createResolveReferenceTest(tableName='projectcategories', gqltype='ProjectCategoryGQLModel', attributeNames=["id", "name", "lastchange"])

test_query_form_project_by_id = createByIdTest(tableName="projectcategories", queryEndpoint="projectCategoryById")
test_query_form_project_page = createPageTest(tableName="projectcategories", queryEndpoint="projectCategoryPage")

test_insert_project_category = createFrontendQuery(
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

test_update_project_category = createUpdateQuery(
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