import uuid
from typing import Union

import strawberry

from .FinanceCategoryGQLModel import FinanceCategoryGQLModel
from .FinanceGQLModel import FinanceGQLModel
from .FinanceTypeGQLModel import FinanceTypeGQLModel

from .MilestoneGQLModel import MilestoneGQLModel

from .ProjectCategoryGQLModel import ProjectCategoryGQLModel
from .ProjectGQLModel import ProjectGQLModel
from .ProjectTypeGQLModel import ProjectTypeGQLModel

from gql_projects.GraphPermissions import RoleBasedPermission

from .externals import UserGQLModel

# @strawberry.type(description="""Type for query root""")
# class Query:
#     @strawberry.field(
#         description="""Returns hello world"""
#         )
#     async def hello(
#         self,
#         info: strawberry.types.Info,
#     ) -> str:
#         return "hello world"

#     from .ProjectGQLModel import project_page
#     project_page = project_page

#     from .ProjectGQLModel import project_by_id
#     project_by_id = project_by_id

#     from .ProjectGQLModel import project_by_group
#     project_by_group = project_by_group

#     from .ProjectGQLModel import randomProject
#     randomProject = randomProject

#     from .ProjectTypeGQLModel import project_type_page
#     project_type_page = project_type_page

#     from .FinanceGQLModel import finance_page
#     finance_page = finance_page

#     from .FinanceTypeGQLModel import finance_type_page
#     finance_type_page = finance_type_page

#     from .MilestoneGQLModel import milestone_page
#     milestone_page = milestone_page

#     from .ProjectCategoryGQLModel import project_category_page
#     project_category_page= project_category_page

#     from .FinanceCategoryGQLModel import finance_category_page
#     finance_category_page = finance_category_page

@strawberry.type(description="""Type for query root""")
class Query:
    from .FinanceCategoryGQLModel import (
       finance_category_by_id,
       finance_category_page
    )
    finance_category_by_id = finance_category_by_id
    finance_category_page = finance_category_page
    
    from .FinanceGQLModel import (
        finance_by_id,
        finance_page
    )
    finance_by_id = finance_by_id
    finance_page = finance_page

    from .FinanceTypeGQLModel import (
        finance_type_by_id,
        finance_type_page
    )
    finance_type_by_id = finance_type_by_id  
    finance_type_page = finance_type_page

    from .MilestoneGQLModel import (
        milestone_by_id,
        milestone_page
    )
    milestone_by_id = milestone_by_id
    milestone_page = milestone_page

    from .ProjectCategoryGQLModel import (
        project_category_by_id,
        project_category_page
    )
    project_category_by_id = project_category_by_id
    project_category_page = project_category_page

    from .ProjectGQLModel import (
        project_by_id,
        project_page
    )
    project_by_id = project_by_id
    project_page = project_page

    from .ProjectTypeGQLModel import (
        project_type_by_id,
        project_type_page
    )
    project_type_by_id = project_type_by_id
    project_type_page = project_type_page

######################################################################################################################
#
#
# Mutations
#
#
######################################################################################################################

@strawberry.type(description="""Type for mutation root""")
class Mutation:
    from .FinanceCategoryGQLModel import (
        finance_category_insert,
        finance_category_update,
        finance_category_delete
    )
    finance_category_insert = finance_category_insert
    finance_category_update = finance_category_update
    finance_category_delete = finance_category_delete

    from .FinanceGQLModel import (
        finance_insert,
        finance_update,
        finance_delete
    )
    finance_insert = finance_insert
    finance_update = finance_update
    finance_delete = finance_delete

    from .FinanceTypeGQLModel import (
        finance_type_insert,
        finance_type_update,
        finance_type_delete
    )
    finance_type_insert = finance_type_insert
    finance_type_update = finance_type_update

    from .MilestoneGQLModel import (
        milestone_insert,
        milestone_update,
        milestone_delete,
        milestones_link_add
    )
    milestone_insert = milestone_insert
    milestone_update = milestone_update
    milestone_delete = milestone_delete

    from .ProjectCategoryGQLModel import (
        project_category_insert,
        project_category_update,
        project_category_delete
    )
    project_category_insert = project_category_insert
    project_category_update = project_category_update
    project_category_delete = project_category_delete

    from .ProjectGQLModel import (
        project_insert,
        project_update,
        #project_delete,
    )
    project_insert = project_insert
    project_update = project_update
   # project_delete = project_delete

    from .ProjectTypeGQLModel import (
        project_type_insert,
        project_type_update,
        project_type_delete
    )
    project_type_insert = project_type_insert
    project_type_update = project_type_update
    project_type_delete = project_type_delete

# @strawberry.type(description="""Type for mutation root""")
# class Mutation:
#     from .ProjectGQLModel import project_insert
#     project_insert = project_insert

#     from .ProjectGQLModel import project_update
#     project_update = project_update

#     from .FinanceGQLModel import finance_insert
#     finance_insert = finance_insert

#     from .FinanceGQLModel import finance_update
#     finance_update = finance_update

#     from .MilestoneGQLModel import milestone_insert
#     milestone_insert = milestone_insert

#     from .MilestoneGQLModel import milestone_update
#     milestone_update = milestone_update

#     from .MilestoneGQLModel import milestone_delete
#     milestone_delete = milestone_delete

#     from .MilestoneGQLModel import milestones_link_remove
#     milestones_link_remove = milestones_link_remove

#     from .MilestoneGQLModel import milestones_link_add
#     milestones_link_add = milestones_link_add

#     from .ProjectTypeGQLModel import projectType_insert
#     projectType_insert = projectType_insert

#     from .FinanceTypeGQLModel import financeType_insert
#     financeType_insert = financeType_insert

#     from .FinanceTypeGQLModel import financeType_update
#     financeType_update = financeType_update

#     from .ProjectTypeGQLModel import projectType_update
#     projectType_update = projectType_update

#     from .ProjectCategoryGQLModel import project_category_insert
#     project_category_insert = project_category_insert

#     from .ProjectCategoryGQLModel import project_category_update
#     project_category_update = project_category_update

#     from .FinanceCategoryGQLModel import finance_category_insert
#     finance_category_insert = finance_category_insert

#     from .FinanceCategoryGQLModel import finance_category_update
#     finance_category_update = finance_category_update


# schema = strawberry.federation.Schema(
#     query=Query,
#     mutation=Mutation
# )
schema = strawberry.federation.Schema(Query, types=(UserGQLModel, ),
                                      mutation=Mutation)
# schema = strawberryA.federation.Schema(Query, types=(ProjectGQLModel,), mutation=Mutation)