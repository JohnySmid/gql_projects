import pytest
from tests.tests_gt_definitions.gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_finances = createResolveReferenceTest(tableName='projectfinances', gqltype='FinanceItemGQLModel', attributeNames=["id", "name", "lastchange", "financetype_id", "project_id"])

test_query_finance_by_id = createByIdTest(tableName="projectfinances", queryEndpoint="financeById")
test_query_finance_page = createPageTest(tableName="projectfinances", queryEndpoint="financePage")

test_finance_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!, $financetype_id: UUID!, $project_id: UUID!) { 
        result: FinanceInsert(finance: {id: $id, name: $name, financetypeId: $financetype_id, projectId: $project_id}) { 
            id
            msg
            finance {
                id
                name
                financetype { id }
            }
        }
    }
    """, 
    variables={"id": "ee40b3bf-ac51-4dbb-8f73-d5da30bf8017", "name": "new finance", "financetype_id": "9e37059c-de2c-4112-9009-559c8b0396f1", "project_id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"},
    asserts=[]
)


test_finance_update = createUpdateQuery(
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
    tableName="projectfinances"
)
