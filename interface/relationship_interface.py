#encoding=utf-8
from flask import Flask
from flask_restful import reqparse, Api, Resource ,request
import time,json,datetime
# Flask相关变量声明
app = Flask(__name__)
api = Api(app)
from flask_cors import CORS
CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}})
from py2neo import Graph,Node,Relationship

# 修改连接方式
graph = Graph("http://localhost:7474", auth=("neo4j", "12345678"))

class BaikeData(Resource):
    @app.route('/', methods=["POST"])
    def post(self):
        data = request.get_json()
        if 'keyword' in data.keys():
            # 节点名称
            node_name = data['keyword']
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
            links = result_dict['links']
            json_result = {}
            lista = []
            listb = []
            id = 1
            set_id = set()
            set_target_id = set()
            for link_json in links:
                print(json.dumps(link_json))
                id = link_json['source_id']
                origin_json = {}
                if link_json['source_id'] not in set_id:
                    origin_json['id'] = str(link_json['source_id'])
                    origin_json['text'] = link_json['source_name']
                    origin_json['color'] = '#43a2f1'
                    origin_json['fontColor'] = 'yellow'
                    lista.append(origin_json)
                    set_id.add(link_json['source_id'])
                target_json = {}
                if link_json['target_id'] not in set_id:
                    target_json['id'] = str(link_json['target_id'])
                    target_json['text'] = link_json['target_name']
                    target_json['color'] = '#43a2f1'
                    target_json['fontColor'] = 'yellow'
                    lista.append(target_json)
                    set_id.add(link_json['target_id'])
                target_id = str(link_json['source_id']) + ':' + str(link_json['target_id'])
                if target_id not in set_target_id:
                    to_json = {}
                    to_json['from'] = str(link_json['source_id'])
                    to_json['to'] = str(link_json['target_id'])
                    to_json['text'] = link_json['type']
                    to_json['color'] = '#43a2f1'
                    listb.append(to_json)
                    set_target_id.add(target_id)
            json_result['rootId'] = str(id)
            json_result['nodes'] = lista
            json_result['lines'] = listb
            print(json.dumps(json_result,ensure_ascii=False))
            response_json = {"status":200,"respon":json_result}
            return response_json

# 设置路由，即路由地址为http://127.0.0.1:5000/baike
api.add_resource(BaikeData, "/relationship")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True,port=5001)