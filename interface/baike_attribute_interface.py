#encoding=utf-8
from flask import Flask, make_response
from flask_restful import reqparse, Api, Resource ,request
import time,json,datetime
# Flask相关变量声明
app = Flask(__name__)
api = Api(app)
from flask_cors import CORS
CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}})
from py2neo import Graph,Node,Relationship

graph = Graph("http://localhost:7474",  username="neo4j", password='12345678')

class BaikeData(Resource):
    @app.route('/', methods=["POST"])
    def post(self):

        data = request.get_json()
        if 'keyword' in data.keys():
            query = 'match (star: Celebrity {name:"' + data['keyword'] +'"}) return star'
            result = graph.run(query).data()
            result_json = {}
            summary = result[0]['star']['summary']
            name = result[0]['star']['name']
            jsona = result[0]['star']
            jsona.pop('name')
            jsona.pop('summary')
            result_json['summary'] = summary
            result_json['name'] = name
            result_json['basicInfo'] = jsona
            # print(data)
            response_json = {"status":200,"respon":result_json}

            print(json.dumps(response_json))
            return response_json
        else:
            return {"message":"error"}


# 设置路由，即路由地址为http://127.0.0.1:5000/baike
api.add_resource(BaikeData, "/star/attribute")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True,port=5000)
