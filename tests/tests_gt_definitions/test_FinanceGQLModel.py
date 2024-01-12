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

test_reference_finances = create_resolve_reference_test(table_name='projectfinances', gqltype='FinanceGQLModel',
                                                        attribute_names=["id", "name", "lastchange", "financetypeId", "projectId"])

#test_query_finance_by_id = create_by_id_test(table_name="projectfinances", query_endpoint="financeById")
test_query_finance_page = create_page_test(table_name="projectfinances", query_endpoint="financePage")

test_finance_insert = create_frontend_query(query="""
    mutation($id: UUID!, $name: String!, $financetype_id: UUID!, $project_id: UUID!) { 
        result: FinanceInsert(finance: {id: $id, name: $name, financetypeId: $financetype_id, projectId: $project_id}) { 
            id
            msg
            finance {
                id
                name
                financeType { id }
            }
        }
    }
    """, 
    variables={"id": "ee40b3bf-ac51-4dbb-8f73-d5da30bf8017", "name": "new finance", "financetype_id": "9e37059c-de2c-4112-9009-559c8b0396f1", "project_id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"},
    asserts=[]
)


test_finance_update = create_update_query(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!,) {
            FinanceUpdate(finance: {id: $id, name: $name, lastchange: $lastchange, value: $value}) {
                id
                msg
                finance {
                    id
                    name
                    value
                    lastchange
                }
            }
        }

    """,
    variables={"id": "f911230f-7e1f-4e9b-90a9-b921996ceb87", "name": "new name", "value": "other value"},
    table_name="projectfinances"
)
