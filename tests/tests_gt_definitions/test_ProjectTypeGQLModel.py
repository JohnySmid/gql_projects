import pytest

from gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_projecttypes = createResolveReferenceTest(tableName='projecttypes', gqltype='ProjectTypeGQLModel',
                                                            attributeNames=["id", "name"])

test_query_project_type_by_id = createByIdTest(tableName="projecttypes", queryEndpoint="projectTypeById")
test_query_project_type_page = createPageTest(tableName="projecttypes", queryEndpoint="projectTypePage")

test_insert_project_type = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $name_en: String!, $category_id: UUID!) {
        result: projectTypeInsert(project: {id: $id, name: $name, nameEn: $name_en, categoryId: $category_id}) {
            id
            msg
            project {
                id
                name
                nameEn
                category { id }
                projects{
                  id
                }
            }
        }
    }""",
    variables={
               "id": "f6f79926-ac0e-4833-9a38-4272cae33fa6", 
               "name": "nove jmeno",
               "name_en": "new name", 
               "category_id": "5c8c4c5a-df3b-44a9-ab90-396bdc84542b"
               }
)


test_update_project_type = createUpdateQuery(
    query="""
        mutation ($id: UUID!, $name: String, $lastchange: DateTime!) {
            result: projectTypeUpdate(project: {id: $id, name: $name, lastchange: $lastchange}) {
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
        "id": "a825d8e1-2e60-4884-afdb-25642db581d8", 
        "name": "nove jmeno1"
        },
    tableName="projecttypes"
)

test_project_type_delete = createUpdateQuery (
    query="""
        mutation($id: UUID!, $lastchange: DateTime!) {
            projectTypeDelete(project: {id: $id, lastchange: $lastchange}) {
                id
                msg
                project {
                    	id
                        }
            }
        }
    """,
    variables={
         "id": "a825d8e1-2e60-4884-afdb-25642db581d8",
    },
    tableName="projecttypes"
)