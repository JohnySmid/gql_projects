import pytest

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createDeleteQuery
)
test_reference_projectcategories = createResolveReferenceTest(tableName='projectcategories', gqltype='ProjectCategoryGQLModel',
                                                                 attributeNames=["id", "name", "nameEn", "lastchange"])

test_query_form_project_by_id = createByIdTest(tableName="projectcategories", queryEndpoint="projectCategoryById")
test_query_form_project_page = createPageTest(tableName="projectcategories", queryEndpoint="projectCategoryPage")

test_insert_project_category = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $name_en: String!) {
        result: projectCategoryInsert(project: {id: $id, name: $name, nameEn: $name_en}) {
            id
            msg
            project {
                id
                name
                nameEn
                lastchange
            }
        }
    }""",
    variables=
    {
        "id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3",
        "name": "nova kategorie", 
        "name_en": "new category"
    }
)

test_update_project_category = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String, $lastchange: DateTime!) {
        result: projectCategoryUpdate(project: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            project {
                id
                name
                lastchange
            }
        }
    }""",
    variables={
        "id": "5c8c4c5a-df3b-44a9-ab90-396bdc84542b",
        "name": "nova kategorie1",
    },
    tableName="projectcategories"
)

test_delete_project_category = createDeleteQuery(tableName="projectcategories", 
        queryBase="projectCategory", id="5c8c4c5a-df3b-44a9-ab90-396bdc84542b")

# test_project_category_delete = createUpdateQuery (
#     query="""
#         mutation($id: UUID!, $lastchange: DateTime!) {
#             projectCategoryDelete(project: {id: $id, lastchange: $lastchange}) {
#                 id
#                 msg
#                 project {
#                 id
#                 }
#             }
#         }
#     """,
#     variables={
#          "id": "5c8c4c5a-df3b-44a9-ab90-396bdc84542b",
#     },
#     tableName="projectcategories"
# )