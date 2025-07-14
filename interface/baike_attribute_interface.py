#encoding=utf-8
from flask import Flask, make_response, request  # 仅保留flask核心库的导入
from flask_restful import reqparse, Api, Resource  # 从flask-restful导入reqparse等组件
import time, json, datetime
from neo4j import GraphDatabase

# Flask相关变量声明
app = Flask(__name__)
api = Api(app)

# 创建图数据库连接
uri = "bolt://localhost:7687"  # 根据实际情况修改
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))

class BaikeData(Resource):
    def post(self):  # 注意：这里移除了重复的@app.route装饰器，避免与api.add_resource冲突
        data = request.get_json()
        if 'keyword' in data.keys():
            def get_star(tx):
                # 推荐使用参数化查询，避免SQL注入风险
                query = 'match (star: Celebrity {name: $keyword}) return star'
                result = tx.run(query, keyword=data["keyword"])
                return result.data()

            with driver.session() as session:
                result = session.read_transaction(get_star)

            # 增加空结果判断，避免索引错误
            if not result:
                return {"status": 404, "message": "未找到该明星数据"}

            result_json = {}
            summary = result[0]['star']['summary']
            name = result[0]['star']['name']
            jsona = result[0]['star']
            jsona.pop('name')
            jsona.pop('summary')
            result_json['summary'] = summary
            result_json['name'] = name
            result_json['basicInfo'] = jsona
            response_json = {"status": 200, "respon": result_json}

            print(json.dumps(response_json))
            return response_json
        else:
            return {"message": "error"}


# 设置路由：http://127.0.0.1:5001/star/attribute
api.add_resource(BaikeData, "/star/attribute")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)
    driver.close()
