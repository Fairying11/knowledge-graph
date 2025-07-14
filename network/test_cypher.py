
from py2neo import Graph
graph = Graph("http://localhost:7474",  username="neo4j", password='123456')
import json


query = """
        MATCH p=(n:Star)-[r]-(m) WHERE n.name = '刘德华' RETURN p, n, r, m
        """
# results = graph.run(query)
# json_results = []
# for record in results:
#
#     path = record['p']
#     person = record['n']
#     relation = record['r']
#     entity = record['m']
#     print(path.data())
#     print(person.data())
#     print(relation.data())
#     print(entity.data())
#     json_results.append({
#         'entity': {
#             'name': entity['name'],
#             'label': entity['label']
#         },
#         'relation': relation.type(),
#         'person': {
#             'name': person['name'],
#             'label': person['label']
#         },
#         'path': graph.cypher_escape(path)
#     })
#
# # 打印JSON格式的查询结果
# print(json.dumps(json_results))
results = graph.run(query).data()
for result in results:
    print(result)
    print(result['p'])
    print(result['n'])
    print(result['r'].properties)
    print(result['m'])
    exit()