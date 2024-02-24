import requests
import pytest
import os

introspection_query = """
  query IntrospectionQuery {
    __schema {
      queryType { name }
      mutationType { name }
      subscriptionType { name }
      types {
        ...FullType
      }
      directives {
        name
        description
        args {
          ...InputValue
        }
      }
    }
  }

  fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
      name
      description
      args {
        ...InputValue
      }
      type {
        ...TypeRef
      }
      isDeprecated
      deprecationReason
    }
    inputFields {
      ...InputValue
    }
    interfaces {
      ...TypeRef
    }
    enumValues(includeDeprecated: true) {
      name
      description
      isDeprecated
      deprecationReason
    }
    possibleTypes {
      ...TypeRef
    }
  }

  fragment InputValue on __InputValue {
    name
    description
    type { ...TypeRef }
    defaultValue
  }

  fragment TypeRef on __Type {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
        }
      }
    }
  }
"""

def test_save_introspection_query():
    graphql_endpoint = 'http://localhost:8000/gql'
    filename = 'IntrospectionQuery.txt'
    
    # Make the GraphQL introspection query
    response = requests.post(graphql_endpoint, json={'query': introspection_query})

    # Check if the request was successful (status code 200) && check if the file exists
    assert response.status_code == 200, f"Failed to execute introspection query. Status code: {response.status_code}"
    assert os.path.isfile(filename), f"File {filename} is not accessible."
    # Save the introspection query result into a txt file
    with open('IntrospectionQuery.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)




# introspection_query = """
#   query IntrospectionQuery {
#     __schema {
#       types {
#         ...FullType
#       }
#     }
#   }

#   fragment FullType on __Type {
#     kind
#     name
#     description
#     fields(includeDeprecated: true) {
#       name
#       description
#       args {
#         ...InputValue
#       }
#       type {
#         ...TypeRef
#       }
#       isDeprecated
#       deprecationReason
#     }
#     inputFields {
#       ...InputValue
#     }
#     interfaces {
#       ...TypeRef
#     }
#     enumValues(includeDeprecated: true) {
#       name
#       description
#       isDeprecated
#       deprecationReason
#     }
#     possibleTypes {
#       ...TypeRef
#     }
#   }

#   fragment InputValue on __InputValue {
#     name
#     description
#     type { ...TypeRef }
#     defaultValue
#   }

#   fragment TypeRef on __Type {
#     kind
#     name
#     ofType {
#       kind
#       name
#       ofType {
#         kind
#         name
#         ofType {
#           kind
#           name
#         }
#       }
#     }
#   }
# """

# def generate_graphql_sdl(types):
#     sdl = ""
#     for graphql_type in types:
#         if graphql_type['kind'] == 'ENUM':
#             sdl += f"enum {graphql_type['name']} {{\n"
#             for enum_value in graphql_type.get('enumValues', []):
#                 sdl += f"  {enum_value['name']}\n"
#             sdl += "}\n\n"
#         elif graphql_type['kind'] == 'OBJECT':
#             sdl += f"type {graphql_type['name']} {{\n"
#             for field in graphql_type.get('fields', []):
#                 sdl += f"  {field['name']}: {get_type_string(field['type'])}\n"
#             sdl += "}\n\n"
#     return sdl

# def get_type_string(graphql_type):
#     if graphql_type['kind'] == 'NON_NULL':
#         return f"{get_type_string(graphql_type['ofType'])}!"
#     elif graphql_type['kind'] == 'LIST':
#         return f"[{get_type_string(graphql_type['ofType'])}]"
#     else:
#         type_name = graphql_type['name']
#         # Replace "UUID" with "ID"
#         # type_name = "ID" if type_name == "UUID" else type_name
#         # # Replace "DateTime" with "String" or the appropriate scalar type
#         # type_name = "String" if type_name == "DateTime" else type_name
#         # type_name = "String" if type_name == "Date" else type_name
#         return type_name

# def test_save_introspection_query():
#     graphql_endpoint = 'http://localhost:8000/gql'
#     filename = 'GraphQLSchema.graphql'  # Change the filename as needed

#     # Make the GraphQL introspection query
#     response = requests.post(graphql_endpoint, json={'query': introspection_query})

#     # Check if the request was successful (status code 200) && check if the file exists
#     assert response.status_code == 200, f"Failed to execute introspection query. Status code: {response.status_code}"

#     # Save the GraphQL SDL format into a separate file
#     with open(filename, 'w', encoding='utf-8') as file:
#         types = response.json()['data']['__schema']['types']
#         sdl = generate_graphql_sdl(types)
#         file.write(sdl)

#     assert os.path.isfile(filename), f"File {filename} is not accessible."