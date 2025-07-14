import json
from py2neo import Graph

# 创建图数据库连接
#根据py2neo版本采用不同的连接方式
graph = Graph("http://localhost:7687",  username="neo4j", password='12345678')
#graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
if __name__=="__main__":
    file = open('../baike_crawl/baike_data.txt', encoding='utf-8')
    file = open('../baike_crawl/baike_append_data.txt', encoding='utf-8')
    people_relation_list = []
    for line in file:
        name = json.loads(line)['name']
        bkid = json.loads(line)['bkid']
        people_relations = json.loads(line)['peoplerelations']
        for people_relation in people_relations:
            relation = people_relation.split('#')[1]
            target_bkid = people_relation.split('#')[3].split('?')[0].split('/')[-1]
            people_relation_list.append(bkid+'\01'+relation+'\01'+ str(target_bkid))
    # 记录关系数量
    # print(people_relation_list)
    for people_relation in people_relation_list:
        print(people_relation)
        a_id = people_relation.split('\01')[0].strip()
        b_id = people_relation.split('\01')[-1].strip()
        rel_type = people_relation.split('\01')[1].strip()
        # 关系query
        query = '''MATCH (a:Celebrity),(b:Celebrity) WHERE a.id = $a_id AND b.id = $b_id CREATE (a)-[r:`{}`]->(b) RETURN r '''.format(rel_type)
        # 运行query
        result = graph.run(query, a_id=a_id, b_id=b_id)
        print(result)




