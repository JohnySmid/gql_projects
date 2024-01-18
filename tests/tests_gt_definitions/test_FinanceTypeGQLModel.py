import pytest

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_financetypes = createResolveReferenceTest(tableName='projectfinancetypes', gqltype='FinanceTypeGQLModel',
                                                            attributeNames=["id", "name"])

test_query_finance_type_by_id = createByIdTest(tableName="projectfinancetypes", queryEndpoint="financeTypeById")
test_query_finance_type_page = createPageTest(tableName="projectfinancetypes", queryEndpoint="financeTypePage")

test_insert_finance_type = createFrontendQuery(query="""
   mutation ($id: UUID!, $name: String!, $name_en: String, ) {
        result: financeTypeInsert(finance: {id: $id, name: $name, nameEn: $name_en}) {
            id
            msg
            finance {
                id 
                name 
                nameEn 
                lastchange
                finances{
                  id
                }
            category { id }
            }
            
        }
    }
    """, 
    variables={
        "id": "ee50b3bf-ac51-4dbb-8f73-d5da30bf8017", 
        "name": "nove finance", 
        "name_en": "new en Finance"
    },
    asserts=[]
)


test_update_finance_type = createUpdateQuery(
    query="""
    mutation ($id: UUID!, $name: String, $lastchange: DateTime!) {
        result: financeTypeUpdate(finance: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            finance{
                id 
                name 
                lastchange
            }   
        }
    }
    """,
    variables={
        "id": "9e37059c-de2c-4112-9009-559c8b0396f1", 
        "name": "nove finance1", 
        },
    tableName="projectfinancetypes"
)

# test_finance_type_delete = createUpdateQuery (
#     query="""
#         mutation($id: UUID!, $lastchange: DateTime!) {
#             financeTypeDelete(finance: {id: $id, lastchange: $lastchange}) {
#                 id
#                 msg
#                 finance {
#                 id 
#                 }
#             }
#         }
#     """,
#     variables={
#          "id": "9e37059c-de2c-4112-9009-559c8b0396f1",
#     },
#     tableName="projectfinancetypes"
# )