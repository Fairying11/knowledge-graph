#encoding=utf-8
import json
from neo4j import GraphDatabase

# 创建图数据库连接
uri = "bolt://localhost:7687"  # 根据实际情况修改
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))

def import_attributes(tx):
    # 定义两个文件路径
    file_path_1 = '../baike_crawl/baike_data.txt'
    file_path_2 = '../baike_crawl/baike_append_data.txt'

    # 处理第一个文件
    try:
        with open(file_path_1, encoding='utf-8') as file_1:
            lines_1 = file_1.readlines()
            print(f"{file_path_1} 文件内容行数: {len(lines_1)}")
            process_file(lines_1, tx)
    except FileNotFoundError:
        print(f"错误: 文件未找到 - {file_path_1}")
    except Exception as e:
        print(f"处理 {file_path_1} 时发生未知错误: {e}")

    # 处理第二个文件
    try:
        with open(file_path_2, encoding='utf-8') as file_2:
            lines_2 = file_2.readlines()
            print(f"{file_path_2} 文件内容行数: {len(lines_2)}")
            process_file(lines_2, tx)
    except FileNotFoundError:
        print(f"错误: 文件未找到 - {file_path_2}")
    except Exception as e:
        print(f"处理 {file_path_2} 时发生未知错误: {e}")

def process_file(lines, tx):
    triple_list = []
    for line in lines:
        try:
            data = json.loads(line)
            if 'bkid' in data:
                bkid = data['bkid']
                name = data.get('ename', '')
                summary = data.get('summary', '')
                properties_json = {'name': name, 'summary': summary}

                basicinfo = data.get('basicinfo', {})
                for key, value in basicinfo.items():
                    clean_key = key.strip().replace(' ', '')
                    clean_value = value.strip()
                    properties_json[clean_key] = clean_value

                json_basic_info = {"id": bkid, "properties": properties_json}
                triple_list.append(json_basic_info)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}, 行内容: {line[:50]}...")
        except Exception as e:
            print(f"处理行时出错: {e}, 行内容: {line[:50]}...")

    print(f"有效数据条目数: {len(triple_list)}")

    if not triple_list:
        print("警告: 没有找到有效的数据条目，可能是文件格式问题或路径错误")
        return

    cypher_query = "MERGE (p:Celebrity {id: $id}) ON CREATE SET p += $properties RETURN p"
    number = 0
    for parameters in triple_list:
        try:
            result = tx.run(cypher_query, parameters)
            for record in result:
                number += 1
        except Exception as e:
            print(f"执行Cypher时出错: {e}, 参数: {parameters.get('id')}")

    print(f"成功导入 {number} 个节点")

if __name__ == "__main__":
    with driver.session() as session:
        session.execute_write(import_attributes)
    driver.close()
