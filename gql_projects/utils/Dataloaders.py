# efektivní načítání dat z databáze, třída Loaders obsahuje vlastnosti pro načítací funkce pro jednotlivé modely, 
# a tyto načítací funkce jsou optimalizovány pro efektivní práci s databází a snižují počet dotazů na databázi.
import datetime
import logging
from sqlalchemy import select
from functools import cache


from gql_projects.DBDefinitions import ProjectCategoryModel, ProjectTypeModel, ProjectModel, MilestoneModel, MilestoneLinkModel, FinanceCategory, FinanceTypeModel, FinanceModel

from uoishelpers.dataloaders import createIdLoader

dbmodels = {
     "projectcategories": ProjectCategoryModel,
     "projecttypes": ProjectTypeModel,
     "projects": ProjectModel,
     "milestones": MilestoneModel,
     "milestonelinks": MilestoneLinkModel,
     "financecategory": FinanceCategory,
     "financetypes": FinanceTypeModel,
     "finances": FinanceModel
}

#gql_forms dataloaders
def prepareSelect(model, where: dict):   
    usedTables = [model.__tablename__]
    from sqlalchemy import select, and_, or_
    baseStatement = select(model)
    # stmt = select(GroupTypeModel).join(GroupTypeModel.groups.property.target).filter(GroupTypeModel.groups.property.target.c.name == "22-5KB")
    # type(GroupTypeModel.groups.property) sqlalchemy.orm.relationships.RelationshipProperty
    # GroupTypeModel.groups.property.entity.class_
    def limitDict(input):
        if isinstance(input, list):
            return [limitDict(item) for item in input]
        if not isinstance(input, dict):
            # print("limitDict", input)
            return input
        result = {key: limitDict(value) if isinstance(value, dict) else value for key, value in input.items() if value is not None}
        return result
    
    def convertAnd(model, name, listExpr):
        assert len(listExpr) > 0, "atleast one attribute in And expected"
        results = [convertAny(model, w) for w in listExpr]
        return and_(*results)

    def convertOr(model, name, listExpr):
        # print("enter convertOr", listExpr)
        assert len(listExpr) > 0, "atleast one attribute in Or expected"
        results = [convertAny(model, w) for w in listExpr]
        return or_(*results)

    def convertAttributeOp(model, name, op, value):
        # print("convertAttributeOp", type(model))
        # print("convertAttributeOp", model, name, op, value)
        column = getattr(model, name)
        assert column is not None, f"cannot map {name} to model {model.__tablename__}"
        opMethod = getattr(column, op)
        assert opMethod is not None, f"cannot map {op} to attribute {name} of model {model.__tablename__}"
        return opMethod(value)

    def convertRelationship(model, attributeName, where, opName, opValue):
        # print("convertRelationship", model, attributeName, where, opName, opValue)
        # GroupTypeModel.groups.property.entity.class_
        targetDBModel = getattr(model, attributeName).property.entity.class_
        # print("target", type(targetDBModel), targetDBModel)

        nonlocal baseStatement
        if targetDBModel.__tablename__ not in usedTables:
            baseStatement = baseStatement.join(targetDBModel)
            usedTables.append(targetDBModel.__tablename__)
        #return convertAttribute(targetDBModel, attributeName, opValue)
        return convertAny(targetDBModel, opValue)
        
        # stmt = select(GroupTypeModel).join(GroupTypeModel.groups.property.target).filter(GroupTypeModel.groups.property.target.c.name == "22-5KB")
        # type(GroupTypeModel.groups.property) sqlalchemy.orm.relationships.RelationshipProperty

    def convertAttribute(model, attributeName, where):
        woNone = limitDict(where)
        #print("convertAttribute", model, attributeName, woNone)
        keys = list(woNone.keys())
        assert len(keys) == 1, "convertAttribute: only one attribute in where expected"
        opName = keys[0]
        opValue = woNone[opName]

        ops = {
            "_eq": "__eq__",
            "_lt": "__lt__",
            "_le": "__le__",
            "_gt": "__gt__",
            "_ge": "__ge__",
            "_in": "in_",
            "_like": "like",
            "_ilike": "ilike",
            "_startswith": "startswith",
            "_endswith": "endswith",
        }

        opName = ops.get(opName, None)
        # if opName is None:
        #     print("op", attributeName, opName, opValue)
        #     result = convertRelationship(model, attributeName, woNone, opName, opValue)
        # else:
        result = convertAttributeOp(model, attributeName, opName, opValue)
        return result
        
    def convertAny(model, where):
        
        woNone = limitDict(where)
        # print("convertAny", woNone, flush=True)
        keys = list(woNone.keys())
        # print(keys, flush=True)
        # print(woNone, flush=True)
        assert len(keys) == 1, "convertAny: only one attribute in where expected"
        key = keys[0]
        value = woNone[key]
        
        convertors = {
            "_and": convertAnd,
            "_or": convertOr
        }
        #print("calling", key, "convertor", value, flush=True)
        #print("value is", value, flush=True)
        convertor = convertors.get(key, convertAttribute)
        convertor = convertors.get(key, None)
        modelAttribute = getattr(model, key, None)
        if (convertor is None) and (modelAttribute is None):
            assert False, f"cannot recognize {model}.{key} on {woNone}"
        if (modelAttribute is not None):
            property = getattr(modelAttribute, "property", None)
            target = getattr(property, "target", None)
            # print("modelAttribute", modelAttribute, target)
            if target is None:
                result = convertAttribute(model, key, value)
            else:
                result = convertRelationship(model, key, where, key, value)
        else:
            result = convertor(model, key, value)
        return result
    
    filterStatement = convertAny(model, limitDict(where))
    result = baseStatement.filter(filterStatement)
    return result

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
    mainstmt = select(DBModel)
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
        
        async def page(self, skip=0, limit=10, where=None, extendedfilter=None):
                    statement = mainstmt
                    if where is not None:
                        statement = prepareSelect(DBModel, where)
                    statement = statement.offset(skip).limit(limit)
                    if extendedfilter is not None:
                        statement = statement.filter_by(**extendedfilter)
                    logging.info(f"loader.page statement {statement}")
                    return await self.execute_select(statement)

    return Loader()

class Loaders:
    authorizations = None
    requests = None
    histories = None
    forms = None
    formtypes = None
    formcategories = None
    sections = None
    parts = None
    items = None
    itemtypes = None
    itemcategories = None
    pass

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

def getLoadersFromInfo(info) -> Loaders:
    context = info.context
    loaders = context["loaders"]
    return loaders

demouser = {
    "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
    "name": "John",
    "surname": "Newbie",
    "email": "john.newbie@world.com",
    "roles": [
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor"
            }
        },
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "name": "rektor"
            }
        }
    ]
}

def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    result = context.get("user", None)
    if result is None:
        authorization = context["request"].headers.get("Authorization", None)
        if authorization is not None:
            if 'Bearer ' in authorization:
                token = authorization.split(' ')[1]
                if token == "2d9dc5ca-a4a2-11ed-b9df-0242ac120003":
                    result = demouser
                    context["user"] = result
    logging.debug("getUserFromInfo", result)
    return result

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }


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




# async def createLoaders(asyncSessionMaker, models=dbmodels):
#     def createLambda(loaderName, DBModel):
#         return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
#     attrs = {}
#     for key, DBModel in models.items():
#         attrs[key] = property(cache(createLambda(key, DBModel)))
    
#     Loaders = type('Loaders', (), attrs)   
#     return Loaders()

# from functools import cache