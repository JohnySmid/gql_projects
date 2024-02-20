# import re
# import json
# import pytest

# @pytest.fixture
# def QueriesFile(request):
#     file_path = "gql_projects/queries.json"
#     file = open(file_path, "w+", encoding="utf-8")
    
#     def writequery(query=None, mutation=None, variables={}, asserts=[]):
#         queries_data = {}  # Create a separate dictionary for each test
        
#         if (query is not None) and ("mutation" in query):
#             jsonData = {
#                 "query": None,
#                 "mutation": query,
#                 "variables": variables,
#                 "asserts": asserts
#             }
#         else:
#             jsonData = {
#                 "query": query,
#                 "mutation": mutation,
#                 "variables": variables,
#                 "asserts": asserts
#             }
        
#         rpattern = r"((?:[a-zA-Z]+Insert)|(?:[a-zA-Z]+Update)|(?:[a-zA-Z]+ById)|(?:[a-zA-Z]+Page))"
#         qstring = query if query else mutation
#         querynames = re.findall(rpattern, qstring)
#         print(querynames)
#         queryname = querynames[0] if querynames else "query_" + qstring
#         queryname = queryname.replace("query", "mutation") if jsonData.get("query", None) is None else queryname
#         queryname = queryname + f"_{hash(queryname)}"
#         queryname = queryname.replace("-", "")
        
#         queries_data[queryname] = jsonData  # Add query data to the dictionary
        
#         def save_to_file():
#             nonlocal file, queries_data
#             json.dump(queries_data, file, indent=2)
        
#         # Register the finalization function to be called after each test
#         request.addfinalizer(save_to_file)
    
#     try:
#         yield writequery
#     finally:
#         file.close()

# Example of how to use the fixture
# def test_queries_file(QueriesFile):
#     query = """
#     query($id: UUID!) {
#         projectById(id: $id)
#     }"""
    
#     variables = {"id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bb"}
    
#     # Assuming you have some asserts to check the results, you can add them to the `asserts` list
    
#     # Call the QueriesFile fixture with your query, variables, and asserts
#     QueriesFile(query=query, variables=variables)
