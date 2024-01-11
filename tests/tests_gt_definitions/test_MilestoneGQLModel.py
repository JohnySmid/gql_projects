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

test_reference_milestones = create_resolve_reference_test(table_name='projectmilestones', gqltype='MilestoneGQLModel')

test_insert_milestone = create_frontend_query(
    query="""mutation ($id: UUID!, $name: String!, $project_id: UUID!) {
        result: MilestoneInsert(link: {id: $id, name: $name, project_id: $project_id}) {
            id
            msg
            history {
                id
                name
            }
        }
    }""",
    variables={
        "id": "4d8fdcb1-bde1-47da-80bb-a67917e1914a", 
        "name": "new name",
        "project_id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb",
    }
)

test_update_history = create_update_query(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: MilestoneUpdate(link: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            history {
                id
                name
            }
        }
    }""",
    variables={"id": "d7266936-17c1-4810-88d2-079ebb864d2e", "name": "new name"},
    table_name="projectmilestones"
)