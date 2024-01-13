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
test_reference_financetypes = create_resolve_reference_test(table_name='projectfinancetypes', gqltype='FinanceTypeGQLModel',
                                                            attribute_names=["id", "name"])

test_query_finance_type_by_id = create_by_id_test(table_name="projectfinancetypes", query_endpoint="financeTypeById")
test_query_finance_type_page = create_page_test(table_name="projectfinancetypes", query_endpoint="financeTypePage")

test_insert_finance_type = create_frontend_query(query="""
   mutation ($id: UUID!, $name: String!, $name_en: String) {
        result: financeTypeInsert(finance: {id: $id, name: $name, nameEn: $name_en}) {
            id
            msg
            finance {
                id 
                name 
                nameEn 
                lastchange
                finances {
                    project {
                        id 
                        name
                    }
                }
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


test_update_finance_type = create_update_query(
    query="""
    mutation ($id: UUID!, $name: String, $name_en: String, $lastchange: DateTime!) {
        result: financeTypeUpdate(finance: {id: $id, name: $name, nameEn: $name_en, lastchange: $lastchange}) {
            id
            msg
            finance{
                id 
                name 
                nameEn 
                lastchange
                finances{
                    project {
                        id 
                        name
                    }
                }
            }   
        }
    }
    """,
    variables={
        "id": "9e37059c-de2c-4112-9009-559c8b0396f1", 
        "name": "nove finance1", 
        "name_en": "new en Finance1"
        },
    table_name="projectfinancetypes"
)
