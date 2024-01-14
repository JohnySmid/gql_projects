#import pytest
# from tests.shared import (
#     prepare_demodata,
#     prepare_in_memory_sqllite,
#     get_demodata,
#     create_context,
# )
 
from tests.gqlshared import (
    create_by_id_test,
    create_page_test,
    create_resolve_reference_test,
    create_frontend_query,
    create_update_query,
    create_delete_query
)

test_reference_financecategory = create_resolve_reference_test(table_name='projectfinancecategories', gqltype='FinanceCategoryGQLModel', 
                                                               attribute_names=["id", "name"])

test_query_finance_category_by_id = create_by_id_test(table_name="projectfinancecategories", query_endpoint="financeCategoryById")
test_query_finance_category_page = create_page_test(table_name="projectfinancecategories", query_endpoint="financeCategoryPage")

test_insert_finance_category = create_frontend_query(query="""
    mutation($id: UUID!, $name: String!, $name_en: String!) { 
        result: financeCategoryInsert(finance: {id: $id, name: $name, nameEn: $name_en}) { 
            id
            msg
            project {
                id
                name
                nameEn
            }
        }
    }
    """, 
    variables={
        "id": "53365ad1-acce-4c29-b0b9-c51c67af4033", 
        "name": "new financeC", 
        "name_en": "new en FinanceC"
        },
    asserts=[]
)


test_update_finance_category = create_update_query(
    query="""
        mutation ($id: UUID!, $name: String, $lastchange: DateTime!) {
            result: financeCategoryUpdate(finance: {id: $id, name: $name, lastchange: $lastchange}) {
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
        "id": "5a15450e-67e6-42a8-923a-aa7ed555b008", 
        "name": "new financeC",
        },
    table_name="projectfinancecategories"
)

test_finance_delete = create_delete_query (
    query="""
        mutation($id: UUID!) {
            financeCategoryDelete(finance: {id: $id}) {
                id
                msg
            }
        }
    """,
    variables={
         "id": "5a15450e-67e6-42a8-923a-aa7ed555b008",
    },
    table_name="projectfinancecategories"
)