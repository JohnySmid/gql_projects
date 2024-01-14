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

test_reference_finances = create_resolve_reference_test(table_name='projectfinances', gqltype='FinanceGQLModel', 
                                                         attribute_names=["id", "name"])

test_query_finance_by_id = create_by_id_test(table_name="projectfinances", query_endpoint="financeById", attribute_names=["id"])
test_query_finance_page = create_page_test(table_name="projectfinances", query_endpoint="financePage", attribute_names=["id"])

test_finance_insert = create_frontend_query(query="""
    mutation ($id: UUID, $name: String!, $amount: Float, $financetype_id: UUID!, $project_id: UUID!) {
         result: financeInsert(finance: {id: $id, name: $name, amount: $amount, financetypeId: $financetype_id, projectId: $project_id}) {
             id
             msg
             finance {
                 id
                 lastchange
                 name
                 amount
                 project {
                     id
                     name
                 }
                 financeType {
                     id
                     name
                 }
             }
         }
     }
     """, 
     variables={"id": "ee40b3bf-ac51-4dbb-8f73-d5da30bf8017", "name": "new finance", "financetype_id": "9e37059c-de2c-4112-9009-559c8b0396f1", "project_id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"},
     asserts=[]
 )


test_finance_update = create_update_query(
    query="""
        mutation ($id: UUID!, $name: String!, $amount: Float, $financetype_id: UUID, $lastchange: DateTime!) {
            result: financeUpdate(finance: {id: $id, name: $name, amount: $amount, financetypeId: $financetype_id, lastchange: $lastchange}) {
                id
                msg
                finance {
                    id
                    lastchange
                    name
                }
            }
        }
    """,
    variables={	
        "id": "f911230f-7e1f-4e9b-90a9-b921996ceb87", 
        "name": "new name",
        "financetype_id": "9e37059c-de2c-4112-9009-559c8b0396f1",
        "amount":  1,
        "lastchange": "2024-01-12T19:17:59.613945"},
    table_name="projectfinances"
)

test_finance_delete = create_delete_query (
    query="""
        mutation($id: UUID!) {
            financeDelete(finance: {id: $id}) {
                id
                msg
            }
        }
    """,
    variables={
         "id": "f911230f-7e1f-4e9b-90a9-b921996ceb87",
    },
    table_name="projectfinances"
)