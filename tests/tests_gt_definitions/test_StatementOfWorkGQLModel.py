import pytest

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_statementofwork = createResolveReferenceTest(tableName='projects_events', gqltype='StatementOfWorkGQLModel', 
                                                          attributeNames=["id"])

test_statementofwork_by_id = createByIdTest(tableName="projects_events", queryEndpoint="statementOfWorkById", attributeNames=["id"])
test_statementofwork_page = createPageTest(tableName="projects_events", queryEndpoint="statementOfWorkPage", attributeNames=["id"])

test_insert_statementofwork_type = createFrontendQuery(
    query="""mutation ($event_id: UUID!, $project_id: UUID!) {
        result: statementOfWorkInsert(statementofwork: {eventId: $event_id, projectId: $project_id}) {
                id
                msg
                statementofwork {
                    created
                    enddate
                    id
                    lastchange
                    startdate
                    project {
                        id
                    }
                    rbacobject {
                        id
                    }
                }
        }
    }""",
    variables={
              "event_id": "45b2df80-ae0f-11ed-9bd8-0242ac110002", 
              "project_id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"
               }
)


test_update_statementofwork_type = createUpdateQuery(
    query="""
        mutation ($id: UUID!, $lastchange: DateTime!, $project_id: UUID) {
            result: statementOfWorkUpdate(statementofwork: {id: $id, lastchange: $lastchange, projectId: $project_id}) {
                id
                msg
                statementofwork {
                    lastchange
                    id
                    event {
                        id
                    }
                }
            }
        }
    """,
    variables={
        "id": "72fa0f04-0a6c-44e0-99e0-15ec08a7443c", 
        "project_id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"
        },
    tableName="projects_events"
)