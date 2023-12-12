# efektivní načítání dat z databáze, třída Loaders obsahuje vlastnosti pro načítací funkce pro jednotlivé modely, 
# a tyto načítací funkce jsou optimalizovány pro efektivní práci s databází a snižují počet dotazů na databázi.
import datetime
from sqlalchemy import select
from functools import cache


from gql_projects.DBDefinitions import ProjectCategoryModel, ProjectTypeModel, ProjectModel, MilestoneModel, MilestoneLinkModel, FinanceCategory, FinanceTypeModel, FinanceModel

from uoishelpers.dataloaders import createIdLoader

def update(destination, source=None, extraValues={}):
    """Updates destination's attributes with source's attributes.
    Attributes with value None are not updated."""
    if source is not None:
        for name in dir(source):
            if name.startswith("_"):
                continue
            value = getattr(source, name)
            if value is not None:
                setattr(destination, name, value)

    for name, value in extraValues.items():
        setattr(destination, name, value)

    return destination


def createLoader(asyncSessionMaker, DBModel):
    baseStatement = select(DBModel)
    print(str(baseStatement)+"test")
    class Loader:
        async def load(self, id):
            async with asyncSessionMaker() as session:
                statement = baseStatement.filter_by(id=id)
                rows = await session.execute(statement)
                rows = rows.scalars()
                row = next(rows, None)
                return row
        
        async def filter_by(self, **kwargs):
            async with asyncSessionMaker() as session:
                statement = baseStatement.filter_by(**kwargs)
                rows = await session.execute(statement)
                rows = rows.scalars()
                return rows

        async def insert(self, entity, extra={}):
            newdbrow = DBModel()
            newdbrow = update(newdbrow, entity, extra)
            async with asyncSessionMaker() as session:
                session.add(newdbrow)
                await session.commit()
            return newdbrow
            
        async def update(self, entity, extraValues={}):
            async with asyncSessionMaker() as session:
                statement = baseStatement.filter_by(id=entity.id)
                rows = await session.execute(statement)
                rows = rows.scalars()
                rowToUpdate = next(rows, None)

                if rowToUpdate is None:
                    return None

                dochecks = hasattr(rowToUpdate, 'lastchange')             
                checkpassed = True  
                # if (dochecks):
                #     if (entity.lastchange != rowToUpdate.lastchange):
                #         result = None
                #         checkpassed = False                        
                #     else:
                #         entity.lastchange = datetime.datetime.now()
                if checkpassed:
                    rowToUpdate = update(rowToUpdate, entity, extraValues=extraValues)
                    await session.commit()
                    result = rowToUpdate               
            return result


    return Loader()


def createLoaders(asyncSessionMaker):
    class Loaders:
        
        @property
        @cache
        def projects(self):
            return createLoader(asyncSessionMaker, ProjectModel)
        
        @property
        @cache
        def finances(self):
            return createLoader(asyncSessionMaker, FinanceModel)
        
        @property
        @cache
        def financetypes(self):
            return createLoader(asyncSessionMaker, FinanceTypeModel)
        
        @property
        @cache
        def milestones(self):
            return createLoader(asyncSessionMaker, MilestoneModel)
        
        @property
        @cache
        def projecttypes(self):
            return createLoader(asyncSessionMaker, ProjectTypeModel)
        
        @property
        @cache
        def financecategory(self):
            return createLoader(asyncSessionMaker, FinanceCategory)
        
        @property
        @cache
        def projectcategories(self):
            return createLoader(asyncSessionMaker, ProjectCategoryModel)
        
        @property
        @cache
        def milestonelinks(self):
            return createLoader(asyncSessionMaker, MilestoneLinkModel)

    return Loaders()


def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }

def getLoadersFromInfo(info):
    return info.context['all']


# from uoishelpers.dataloaders import createIdLoader, createFkeyLoader

# from gql_projects.DBDefinitions import (
#     ProjectCategoryModel,
#     ProjectTypeModel,
#     ProjectModel,
#     MilestoneModel,
#     MilestoneLinkModel,
#     FinanceCategory,
#     FinanceTypeModel,
#     FinanceModel
# )


# dbmodels = {
#     "projectcategories": ProjectCategoryModel,
#     "projecttypes": ProjectTypeModel,
#     "projects": ProjectModel,
#     "milestones": MilestoneModel,
#     "milestonelinks": MilestoneLinkModel,
#     "financecategory": FinanceCategory,
#     "financetypes": FinanceTypeModel,
#     "finances": FinanceModel
# }

# async def createLoaders(asyncSessionMaker, models=dbmodels):
#     def createLambda(loaderName, DBModel):
#         return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
#     attrs = {}
#     for key, DBModel in models.items():
#         attrs[key] = property(cache(createLambda(key, DBModel)))
    
#     Loaders = type('Loaders', (), attrs)   
#     return Loaders()

# from functools import cache