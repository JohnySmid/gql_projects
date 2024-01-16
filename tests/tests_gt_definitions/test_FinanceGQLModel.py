# import pytest

# from gt_utils import (
#     createByIdTest, 
#     createPageTest, 
#     createResolveReferenceTest, 
#     createFrontendQuery, 
#     createUpdateQuery
# )
# test_reference_finances = createResolveReferenceTest(tableName='projectfinances', gqltype='FinanceGQLModel', 
#                                                          attributeNames=["id", "name"])

# test_query_finance_by_id = createByIdTest(tableName="projectfinances", queryEndpoint="financeById", attributeNames=["id"])
# test_query_finance_page = createPageTest(tableName="projectfinances", queryEndpoint="financePage", attributeNames=["id"])

# test_finance_insert = createFrontendQuery(query="""
#     mutation ($id: UUID, $name: String!, $amount: Float, $financetype_id: UUID!, $project_id: UUID!) {
#          result: financeInsert(finance: {id: $id, name: $name, amount: $amount, financetypeId: $financetype_id, projectId: $project_id}) {
#              id
#              msg
#              finance {
#                  id
#                  lastchange
#                  name
#                  amount
#                  project {
#                      id
#                      name
#                  }
#                  financeType {
#                      id
#                      name
#                  }
#              }
#          }
#      }
#      """, 
#      variables={"id": "ee40b3bf-ac51-4dbb-8f73-d5da30bf8017", "name": "new finance", "financetype_id": "9e37059c-de2c-4112-9009-559c8b0396f1", "project_id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"},
#      asserts=[]
#  )


# test_finance_update = createUpdateQuery(
#     query="""
#         mutation ($id: UUID!, $name: String!, $amount: Float, $financetype_id: UUID, $lastchange: DateTime!) {
#             result: financeUpdate(finance: {id: $id, name: $name, amount: $amount, financetypeId: $financetype_id, lastchange: $lastchange}) {
#                 id
#                 msg
#                 finance {
#                     id
#                     lastchange
#                     name
#                 }
#             }
#         }
#     """,
#     variables={	
#         "id": "f911230f-7e1f-4e9b-90a9-b921996ceb87", 
#         "name": "new name",
#         "financetype_id": "9e37059c-de2c-4112-9009-559c8b0396f1",
#         "amount":  1,
#         "lastchange": "2024-01-12T19:17:59.613945"},
#     tableName="projectfinances"
# )

# test_finance_delete = createUpdateQuery (
#     query="""
#         mutation($id: UUID!, $lastchange: DateTime!) {
#             financeDelete(finance: {id: $id, lastchange: $lastchange}) {
#                 id
#                 msg
#                 finance {
#                     id
#                     }
#             }
#         }
#     """,
#     variables={
#          "id": "f911230f-7e1f-4e9b-90a9-b921996ceb87",
#     },
#     tableName="projectfinances"
# )