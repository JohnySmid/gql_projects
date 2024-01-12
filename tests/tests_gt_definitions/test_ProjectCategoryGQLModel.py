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

test_reference_projectcategories = create_resolve_reference_test(table_name='projectcategories', gqltype='ProjectCategoryGQLModel',
                                                                 attribute_names=["id", "name", "name_en", "lastchange"])

test_query_form_project_by_id = create_by_id_test(table_name="projectcategories", query_endpoint="projectCategoryById")
test_query_form_project_page = create_page_test(table_name="projectcategories", query_endpoint="projectCategoryPage")

test_insert_project_category = create_frontend_query(
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

test_update_project_category = create_update_query(
    query="""mutation ($id: UUID!, $name: String, $name_en: String, $lastchange: DateTime!) {
        result: projectCategoryUpdate(project: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
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
    variables={
        "id": "fc7f95b5-410c-4a26-a4e9-6b0b2a841645",
        "name": "nova kategorie1",
        "name_en": "new category1",
    },
    table_name="projectcategories"
)