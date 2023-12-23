import strawberry as strawberryA
import strawberry
from .GroupGQLModel import GroupGQLModel


@strawberry.type(description="""Type for query root""")
class Query:
    @strawberry.field(
        description="""Returns hello world"""
        )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"

    from .ProjectGQLModel import project_page
    project_page = project_page

    from .ProjectGQLModel import project_by_id
    project_by_id = project_by_id

    from .ProjectGQLModel import project_by_group
    project_by_group = project_by_group

    from .ProjectGQLModel import randomProject
    randomProject = randomProject

    from .ProjectTypeGQLModel import project_type_page
    project_type_page = project_type_page

    from .FinanceGQLModel import finance_page
    finance_page = finance_page

    from .FinanceTypeGQLModel import finance_type_page
    finance_type_page = finance_type_page

    from .MilestoneGQLModel import milestone_page
    milestone_page = milestone_page

    from .ProjectCategoryGQLModel import project_category_page
    project_category_page= project_category_page

    from .FinanceCategoryGQLModel import finance_category_page
    finance_category_page = finance_category_page


@strawberry.type(description="""Type for mutation root""")
class Mutation:
    from .ProjectGQLModel import project_insert
    project_insert = project_insert

    from .ProjectGQLModel import project_update
    project_update = project_update

    from .FinanceGQLModel import finance_insert
    finance_insert = finance_insert

    from .FinanceGQLModel import finance_update
    finance_update = finance_update

    from .MilestoneGQLModel import milestone_insert
    milestone_insert = milestone_insert

    from .MilestoneGQLModel import milestone_update
    milestone_update = milestone_update

    from .MilestoneGQLModel import milestone_delete
    milestone_delete = milestone_delete

    from .MilestoneGQLModel import milestones_link_remove
    milestones_link_remove = milestones_link_remove

    from .MilestoneGQLModel import milestones_link_add
    milestones_link_add = milestones_link_add

    from .ProjectTypeGQLModel import projectType_insert
    projectType_insert = projectType_insert

    from .FinanceTypeGQLModel import financeType_insert
    financeType_insert = financeType_insert

    from .FinanceTypeGQLModel import financeType_update
    financeType_update = financeType_update

    from .ProjectTypeGQLModel import projectType_update
    projectType_update = projectType_update

    from .ProjectCategoryGQLModel import project_category_insert
    project_category_insert = project_category_insert

    from .ProjectCategoryGQLModel import project_category_update
    project_category_update = project_category_update

    from .FinanceCategoryGQLModel import finance_category_insert
    finance_category_insert = finance_category_insert

    from .FinanceCategoryGQLModel import finance_category_update
    finance_category_update = finance_category_update


schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation
)

# schema = strawberryA.federation.Schema(Query, types=(GroupGQLModel,), mutation=Mutation)