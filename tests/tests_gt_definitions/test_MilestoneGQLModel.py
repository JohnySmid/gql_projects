import pytest

from gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_milestones = createResolveReferenceTest(tableName='projectmilestones', gqltype='MilestoneGQLModel', 
                                                          attributeNames=["id", "name"])

test_milestone_by_id = createByIdTest(tableName="projectmilestones", queryEndpoint="milestoneById")
test_milestone_page = createPageTest(tableName="projectmilestones", queryEndpoint="milestonePage")

test_insert_milestone = createFrontendQuery(
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
              	project{
                    id
                    }
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

test_update_milestone = createUpdateQuery(
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
    tableName="projectmilestones"
)

test_milestone_delete = createUpdateQuery (
    query="""
        mutation($id: UUID!, $lastchange: DateTime!) {
            milestoneDelete(milestone: {id: $id, lastchange: $lastchange}) {
                id
                msg
                milestone {
                id
                }
            }
        }
    """,
    variables={
         "id": "d7266936-17c1-4810-88d2-079ebb864d2e",
    },
    tableName="projectmilestones"
)


test_milestone_add_link=createFrontendQuery(
     query="""
          mutation($previous_id: UUID!, $next_id: UUID!) {
             milestonesLinkAdd(link: {previousId: $previous_id, nextId: $next_id}) {
                 id
                 msg
 }    
}
     """,
     variables={
          "previous_id": "512cf74f-3e8c-40cf-a815-7fd960a31a60",
          "next_id": "4ca54daf-38e1-4658-9a3f-f893548fb4aa",
     }
 )