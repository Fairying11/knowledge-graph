#encoding=utf-8
import json,py2neo
from py2neo import Graph,Node,Relationship


if __name__=="__main__":
    # 第一次采集的实体数据
    file = open('../baike_crawl/baike_data.txt', encoding='utf-8')
    # 增加百科图谱实体数据，第二次采集的人物实体数据
    file = open('../baike_crawl/baike_append_data.txt', encoding='utf-8')
    triple_list = []
    for line in file:
        if 'bkid' in json.loads(line).keys():
            bkid = json.loads(line)['bkid']
            name = json.loads(line)['ename']
            summary = json.loads(line)['summary']
            properties_json = {}
            properties_json['name'] = name
            properties_json['summary'] = summary
            basicinfo = json.loads(line)['basicinfo']
            for key,value in basicinfo.items():
                key = key.strip().replace(' ','')
                value = value.strip()
                properties_json[key] = value
            json_basic_info = {"id": bkid, "properties": properties_json}
            triple_list.append(json_basic_info)
    #打印数量
    print(len(triple_list))
    # 根据py2neo版本采用不同的连接方式
    graph = Graph("http://localhost:7687",  username="neo4j", password='12345678')
    # graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
    # 更新query
    #cypher_query = """MERGE (p:Person {id: $id}) ON CREATE SET p += $properties ON MATCH SET p += $new_properties RETURN p"""
    # 创建merge query
    cypher_query = """MERGE (p:Celebrity {id: $id}) ON CREATE SET p += $properties RETURN p"""
    number = 0
    for parameters in triple_list:
        # 运行query
        try:
            result = graph.run(cypher_query, parameters)
            # Print the results
            for record in result:
                number += 1
                #记录数量
                # print(number)
        except:
            #记录异常
            print(record)
