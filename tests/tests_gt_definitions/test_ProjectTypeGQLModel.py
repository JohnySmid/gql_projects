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

test_reference_projecttypes = create_resolve_reference_test(table_name='projecttypes', gqltype='ProjectTypeGQLModel', attribute_names=["id", "name", "name_en", "lastchange", "category_id"])

test_query_project_type_by_id = create_by_id_test(table_name="projecttypes", query_endpoint="projectTypeById")
test_query_project_type_page = create_page_test(table_name="projecttypes", query_endpoint="projectTypePage")

test_insert_project_type = create_frontend_query(
    query="""mutation ($id: UUID!, $name: String!, $name_en: String!, $category_id: UUID!) {
        result: projectTypeInsert(project: {id: $id, name: $name, nameEn: $name_en, categoryId: $category_id}) {
            id
            msg
            project {
                id
                name
                nameEn
                projects { id }
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
#  FAILED tests/tests_gt_definitions/test_ProjectTypeGQLModel.py::test_update_project_type - TypeError: 'NoneType' object is not subscriptable
test_update_project_type = create_update_query(
    query="""
        mutation ($id: UUID!, $name: String, $name_en: String, $lastchange: DateTime!) {
            result: ProjectTypeUpdate(project: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
                id
                msg
                project {
                    	id
                        name
                        lastchange
                        nameEn
                }
            }
        }
    """,
    variables={"id": "2e1140f4-afb0-11ed-9bd8-0242ac110002", "name": "nove jmeno1", "name_en": "new name1",},
    table_name="projecttypes"
)