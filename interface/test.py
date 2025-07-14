#encoding=utf-8
from flask import Flask
from flask_restful import reqparse, Api, Resource ,request
import time,json,datetime
# Flask相关变量声明
app = Flask(__name__)
api = Api(app)
from py2neo import Graph,Node,Relationship

graph = Graph("http://localhost:7474",  username="neo4j", password='12345678')
data = {"keyword":"杨幂"}
if 'keyword' in data.keys():


    # # 运行cypher查询
    # query = """
    # MATCH (a)-[r]->(b)
    # RETURN a.name AS source, type(r) AS type, b.name AS target
    # """
    # result = graph.run(query)
    # 节点名称
    node_name = "刘德华"

    # 运行cypher查询
    query = """
    MATCH (a {name: $node_name})-[r]->(b)
    RETURN ID(r) AS id, a.name AS source_name, type(r) AS type, b.name AS target_name, ID(a) AS source_id, ID(b) AS target_id
    """
    result = graph.run(query, node_name=node_name)

    # 将结果转换为字典
    result_dict = {"links": []}
    for record in result:
        result_dict["links"].append({
            "id": record["id"],
            "source_name": record["source_name"],
            "type": record["type"],
            "target_name": record["target_name"],
            "source_id": record["source_id"],
            "target_id": record["target_id"]
        })

    print(result_dict)
    links = result_dict['links']
    jsona = {}
    lista = []
    listb = []
    listc = []

    id = 1
    set_id = set()
    for link_json in links:
        print(json.dumps(link_json))
        id = link_json['source_id']
        origin_json = {}
        origin_json['id'] = link_json['source_id']
        origin_json['text'] = link_json['source_name']
        origin_json['color'] = '#43a2f1'
        origin_json['fontColor'] = 'yellow'
        if origin_json['id'] not in set_id:
            set_id.add(link_json['source_id'])
            lista.append(origin_json)
        target_json = {}
        target_json['id'] = link_json['target_id']
        target_json['text'] = link_json['target_name']
        target_json['color'] = '#43a2f1'
        target_json['fontColor'] = 'yellow'
        lista.append(target_json)
        to_json = {}
        to_json['from'] = link_json['source_id']
        to_json['to'] = link_json['target_id']
        to_json['text'] = link_json['type']
        to_json['color'] = '#43a2f1'
        listb.append(to_json)
        # print(link_json['source_id'])
        # print(link_json['target_id'])
    jsona['rootId'] = id
    jsona['nodes'] = lista
    jsona['lines'] = listb
    print(json.dumps(jsona,ensure_ascii=False))
    exit()


    # 将字典转换为JSON格式
    json_data = json.dumps(result_dict)

    # 打印JSON数据
    print(json_data)

    exit()

    #查询与人物相关的实体和关系
    query = "MATCH p=(n:Star)-[r]-(m) WHERE n.name = '" + data['keyword'] + "'RETURN p, n, r, m"
    result = graph.run(query).data()
    print(json.dumps(result,ensure_ascii=False))

    for record in result:

        # print(json.dumps(record.data()))
        path = record['p']
        person = record['n']
        relation = record['r']
        entity = record['m']
        print(path)
        print(person)
        print(relation)
        print(entity)
        exit()

    # query = "MATCH (n { name: '" +  data['keyword'] + "'})--(r) RETURN  r"
    # print(graph.run(query))
    # for record in graph.run(query):
    #     # print(record)
    #     pass
    # result = graph.run(query).data()
    # print(json.dumps(result,ensure_ascii=False))
    response_json = {"status":200,"respon":result}
    print(response_json)
# return json.dumps(data,ensure_ascii=False)

