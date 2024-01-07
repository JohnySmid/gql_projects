import pytest
from tests.tests_gt_definitions.gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_financecategory = createResolveReferenceTest(tableName='projectfinancecategories', gqltype='FinanceCategoryItemGQLModel', attributeNames=["id", "name", "lastchange", "name_en"])

test_query_finance_category_by_id = createByIdTest(tableName="projectfinancecategories", queryEndpoint="financeCategoryeById")
test_query_finance_category_page = createPageTest(tableName="projectfinancecategories", queryEndpoint="financeCategoryPage")

test_insert_finance_category = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!, $name_en: String!) { 
        result: FinanceCategoryInsert(finance: {id: $id, name: $name, nameEn: $name_en}) { 
            id
            msg
            finance {
                id
                name
                nameEn
            }
        }
    }
    """, 
    variables={"id": "53365ad1-acce-4c29-b0b9-c51c67af4033", "name": "new financeC", "name_en": "new en FinanceC"},
    asserts=[]
)


test_update_finance_category = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!,) {
            FinanceCategoryUpdate(finance: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                finance {
                    id
                    name
                    lastchange
                }
            }
        }

    """,
    variables={"id": "5a15450e-67e6-42a8-923a-aa7ed555b008", "name": "new name"},
    tableName="projectfinancecategories"
)
