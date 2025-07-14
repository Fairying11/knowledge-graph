#encoding=utf-8
from flask import Flask
from flask_restful import reqparse, Api, Resource, request
import time, json, datetime
from neo4j import GraphDatabase

# Flask相关变量声明
app = Flask(__name__)
api = Api(app)

# 创建图数据库连接
uri = "bolt://localhost:7687"  # 根据实际情况修改
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))

data = {"keyword": "杨幂"}
if 'keyword' in data.keys():
    node_name = "刘德华"

    def get_relations(tx):
        query = """
        MATCH (a {name: $node_name})-[r]->(b)
        RETURN ID(r) AS id, a.name AS source_name, type(r) AS type, b.name AS target_name, ID(a) AS source_id, ID(b) AS target_id
        """
        result = tx.run(query, node_name=node_name)
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
        return result_dict

    with driver.session() as session:
        result_dict = session.read_transaction(get_relations)

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

    jsona['rootId'] = id
    jsona['nodes'] = lista
    jsona['lines'] = listb
    print(json.dumps(jsona, ensure_ascii=False))

    driver.close()
    exit()
