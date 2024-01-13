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

test_reference_milestones = create_resolve_reference_test(table_name='projectmilestones', gqltype='MilestoneGQLModel', 
                                                          attribute_names=["id", "name"])

test_milestone_by_id = create_by_id_test(table_name="projectmilestones", query_endpoint="milestoneById")
test_milestone_page = create_page_test(table_name="projectmilestones", query_endpoint="milestonePage")

test_insert_milestone = create_frontend_query(
    query="""
    mutation ($id: UUID, $name: String!, $project_id: UUID!, $start_date: DateTime, $end_date: DateTime) {
        result: milestoneInsert(milestone: {id: $id, name: $name, projectId: $project_id, startdate: $start_date, enddate: $end_date}) {
            id
            msg
            milestone
            {
                id
                name
                startdate
                enddate
                lastchange
                previous{
                    id
                    name
                }
                nexts{
                    id
                    name
                }
            }
        }
    }
    """,
    variables={
         "id": "4d8fdcb1-bde1-47da-80bb-a67917e1914a", 
        "name": "new milestone",
        "project_id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"
    }
)

test_update_milestone = create_update_query(
    query="""
    mutation ($id: UUID!, $name: String, $lastchange: DateTime!, $start_date: DateTime, $end_date: DateTime) {
        result: milestoneUpdate(milestone: {id: $id, name: $name, lastchange: $lastchange, startdate: $start_date, enddate: $end_date}) {
            id
            msg
            milestone {
                id
                name
                lastchange
            }
        }
    }
    """,
    variables={
        "id": "d7266936-17c1-4810-88d2-079ebb864d2e", 
        "name": "newMilestone1"
        },
    table_name="projectmilestones"
)