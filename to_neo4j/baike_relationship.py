import json
from neo4j import GraphDatabase
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# 创建图数据库连接
uri = "bolt://localhost:7687"  # 根据实际情况修改
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))

def import_relations(tx):
    # 定义两个文件路径
    file_path_1 = '../baike_crawl/baike_data.txt'
    file_path_2 = '../baike_crawl/baike_append_data.txt'

    # 统计总关系数
    total_relations = 0

    # 处理第一个文件
    print(f"\n正在处理文件: {file_path_1}")
    processed, errors = process_file(file_path_1, tx)
    total_relations += processed
    print(f"文件 {file_path_1} 处理完成:")
    print(f"  成功导入: {processed} 个关系")
    print(f"  错误数量: {errors}")

    # 处理第二个文件
    print(f"\n正在处理文件: {file_path_2}")
    processed, errors = process_file(file_path_2, tx)
    total_relations += processed
    print(f"文件 {file_path_2} 处理完成:")
    print(f"  成功导入: {processed} 个关系")
    print(f"  错误数量: {errors}")

    print(f"\n总共成功导入: {total_relations} 个关系")

def process_file(file_path, tx):
    """处理单个文件并导入关系"""
    try:
        with open(file_path, encoding='utf-8') as file:
            lines = file.readlines()
            print(f"文件内容行数: {len(lines)}")

            # 解析关系数据
            relations, errors = parse_relations(lines)
            print(f"有效关系条目数: {len(relations)}")
            print(f"解析错误数: {errors}")

            if not relations:
                print("警告: 没有找到有效的关系数据")
                return 0, errors

            # 批量导入关系
            success_count = batch_import_relations(tx, relations)
            return success_count, errors

    except FileNotFoundError:
        print(f"错误: 文件未找到 - {file_path}")
        return 0, 0
    except Exception as e:
        print(f"处理文件时发生未知错误: {e}")
        return 0, 0

def parse_relations(lines):
    """解析JSON行并提取关系数据"""
    relations = []
    error_count = 0
    line_count = 0

    for line in lines:
        line_count += 1
        try:
            data = json.loads(line)
            # 跳过缺少必要字段的记录
            if 'bkid' not in data or 'peoplerelations' not in data:
                continue

            source_bkid = data['bkid']

            # 处理每个关系
            for rel_data in data['peoplerelations']:
                parts = rel_data.split('#')
                if len(parts) < 4:
                    print(f"格式错误 (行 {line_count}): 关系数据部分不足 - {rel_data}")
                    error_count += 1
                    continue

                rel_type = parts[1].strip()
                target_bkid = parts[3].split('?')[0].split('/')[-1].strip()

                # 过滤无效的关系类型或ID
                if not rel_type or not target_bkid:
                    error_count += 1
                    continue

                # 使用元组表示关系，便于后续去重
                relations.append((source_bkid, rel_type, target_bkid))

        except json.JSONDecodeError as e:
            error_count += 1
            print(f"JSON解析错误 (行 {line_count}): {e}")
        except Exception as e:
            error_count += 1
            print(f"处理行 {line_count} 时出错: {e}")

    # 去重处理 (如果两个节点间已存在相同类型的关系，则跳过)
    unique_relations = list(set(relations))
    if len(relations) != len(unique_relations):
        print(f"去重处理: 从 {len(relations)} 条减少到 {len(unique_relations)} 条唯一关系")

    return unique_relations, error_count

def batch_import_relations(tx, relations, batch_size=500):
    """批量导入关系数据，提高性能"""
    success_count = 0
    batch_count = 0

    # 使用进度条显示处理进度
    with tqdm(total=len(relations), desc="导入关系") as pbar:
        for i in range(0, len(relations), batch_size):
            batch = relations[i:i+batch_size]
            batch_count += 1

            # 构建批量导入的Cypher语句
            queries = []
            params_list = []

            for rel in batch:
                source_id, rel_type, target_id = rel
                # 转义关系类型中的特殊字符
                safe_rel_type = rel_type.replace('`', '\\`')

                # 使用 MERGE 避免创建重复关系
                query = f"""
                MERGE (a:Celebrity {{id: $source_id}})
                MERGE (b:Celebrity {{id: $target_id}})
                MERGE (a)-[r:`{safe_rel_type}`]->(b)
                RETURN COUNT(r) AS created
                """
                queries.append(query)
                params_list.append({"source_id": source_id, "target_id": target_id})

            # 执行批量查询
            try:
                for query, params in zip(queries, params_list):
                    result = tx.run(query, **params)
                    count = result.single()[0]
                    success_count += count

                pbar.update(len(batch))

            except Exception as e:
                print(f"批量 {batch_count} 执行失败: {e}")
                # 可以选择继续处理下一批，或根据需要终止整个操作

    return success_count

if __name__ == "__main__":
    with driver.session() as session:
        # 使用 execute_write 替换 write_transaction
        session.execute_write(import_relations)

    # 验证导入结果
    with driver.session() as session:
        node_count = session.run("MATCH (n) RETURN count(n) AS count").single()[0]
        rel_count = session.run("MATCH ()-[r]->() RETURN count(r) AS count").single()[0]

        print(f"\n数据库当前状态:")
        print(f"  节点总数: {node_count}")
        print(f"  关系总数: {rel_count}")

    driver.close()
