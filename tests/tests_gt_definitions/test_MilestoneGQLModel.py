import pytest
from tests.tests_gt_definitions.gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_milestones = createResolveReferenceTest(tableName='projectmilestones', gqltype='MilestoneGQLModel')

test_insert_milestone = createFrontendQuery(
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

test_update_history = createUpdateQuery(
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
    tableName="projectmilestones"
)