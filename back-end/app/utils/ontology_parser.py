from rdflib import Graph, RDFS, RDF, Namespace, URIRef, Literal, OWL
from typing import Dict
import json
import os
from datetime import datetime
from app.models.schema import TreeNode, ParentRelation, ChildRelation

OBO = Namespace("http://purl.obolibrary.org/obo/")
OBOINOWL = Namespace("http://www.geneontology.org/formats/oboInOwl#")
PART_OF = OBO["BFO_0000050"]


def _get_literal(graph: Graph, subject: URIRef, predicate: URIRef, lang=None):
    """获取指定语言的Literal文本"""
    for obj in graph.objects(subject, predicate):
        if isinstance(obj, Literal):
            if lang is None or obj.language == lang:
                return str(obj)
    return None


def parse_ontology(file_path: str) -> Dict[str, TreeNode]:
    """
    解析 OWL 文件，返回以 ID 为键的 TreeNode 字典。
    - 子类→父类：rdfs:subClassOf
    - 部分关系：obo:BFO_0000050 (part_of)
    """
    g = Graph()
    g.parse(file_path, format="xml")

    nodes: Dict[str, TreeNode] = {}

    # === Step 1: 构建所有节点（只处理 owl:Class） ===
    for s in g.subjects(RDF.type, OWL.Class):
        iri = str(s)
        node_id = _get_literal(g, s, OBOINOWL.id) or iri.split("/")[-1]
        label = _get_literal(g, s, RDFS.label)
        label_zh = _get_literal(g, s, RDFS.label, lang="zh")
        definition = _get_literal(g, s, OBO["IAO_0000115"])
        definition_zh = _get_literal(g, s, OBO["IAO_0000115"], lang="zh")

        nodes[node_id] = TreeNode(
            id=node_id,
            label=label,
            label_zh=label_zh,
            definition=definition,
            definition_zh=definition_zh,
            iri=iri,
        )

    # === Step 2: 建立 subClassOf 父子关系 ===
    for s, _, o in g.triples((None, RDFS.subClassOf, None)):
        # 跳过指向 owl:Restriction 的关系，这些会在 Step 3 中处理
        if (o, RDF.type, OWL.Restriction) in g:
            continue
            
        child_id = _get_literal(g, s, OBOINOWL.id) or str(s).split("/")[-1]
        parent_id = _get_literal(g, o, OBOINOWL.id) or str(o).split("/")[-1]

        # 创建节点（若还不存在）
        if child_id not in nodes:
            nodes[child_id] = TreeNode(id=child_id)
        if parent_id not in nodes:
            nodes[parent_id] = TreeNode(id=parent_id)

        nodes[child_id].parents.append(
            ParentRelation(parentId=parent_id, relationType="subClassOf")
        )
        nodes[parent_id].children.append(
            ChildRelation(childId=child_id, relationType="subClassOf")
        )
        nodes[parent_id].isLeaf = False

    # === Step 3: 建立 part_of 父子关系 ===
    # part_of 关系通过 owl:Restriction 定义，需要特殊处理
    for s, _, restriction in g.triples((None, RDFS.subClassOf, None)):
        # 检查是否指向 owl:Restriction
        if (restriction, RDF.type, OWL.Restriction) in g:
            # 检查 owl:onProperty 是否为 part_of
            for _, _, property_uri in g.triples((restriction, OWL.onProperty, None)):
                if str(property_uri) == str(PART_OF):
                    # 获取 owl:someValuesFrom 指向的父类
                    for _, _, parent_uri in g.triples((restriction, OWL.someValuesFrom, None)):
                        child_id = _get_literal(g, s, OBOINOWL.id) or str(s).split("/")[-1]
                        parent_id = _get_literal(g, parent_uri, OBOINOWL.id) or str(parent_uri).split("/")[-1]

                        # 创建节点（若还不存在）
                        if child_id not in nodes:
                            nodes[child_id] = TreeNode(id=child_id)
                        if parent_id not in nodes:
                            nodes[parent_id] = TreeNode(id=parent_id)

                        nodes[child_id].parents.append(
                            ParentRelation(parentId=parent_id, relationType="partOf")
                        )
                        nodes[parent_id].children.append(
                            ChildRelation(childId=child_id, relationType="partOf")
                        )
                        nodes[parent_id].isLeaf = False

    # === Step 4: 统计子节点数量 ===
    for node in nodes.values():
        node.count = len(node.children)

    return nodes


def save_nodes_to_json(nodes: Dict[str, TreeNode], output_file: str = None) -> str:
    """
    将解析的节点数据保存为 JSON 文件
    
    Args:
        nodes: 解析后的节点字典
        output_file: 输出文件路径，如果为 None 则自动生成
    
    Returns:
        str: 保存的文件路径
    """
    if output_file is None:
        # 自动生成文件名，包含时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"ontology_nodes_{timestamp}.json"
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file) if os.path.dirname(output_file) else "."
    os.makedirs(output_dir, exist_ok=True)
    
    # 将 TreeNode 对象转换为字典
    nodes_data = {}
    for node_id, node in nodes.items():
        nodes_data[node_id] = node.dict()
    
    # 创建包含元数据的完整数据结构
    output_data = {
        "metadata": {
            "total_nodes": len(nodes),
            "generated_at": datetime.now().isoformat(),
            "description": "Parsed ontology nodes from OWL file"
        },
        "nodes": nodes_data
    }
    
    # 保存为 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 节点数据已保存到: {output_file}")
    print(f"📊 共保存 {len(nodes)} 个节点")
    
    return output_file


# === 测试入口 ===
if __name__ == "__main__":
    test_file = "./psi-ms-zh.owl"
    print("🧩 正在解析 OWL 文件...")
    nodes = parse_ontology(test_file)
    print(f"✅ 共解析 {len(nodes)} 个节点")
    
    # 保存为 JSON 文件
    output_file = save_nodes_to_json(nodes)
    
    # 显示前3个节点的示例
    print("\n📋 前3个节点示例:")
    sample = list(nodes.values())[:3]
    for i, node in enumerate(sample, 1):
        print(f"\n节点 {i}:")
        print(f"  ID: {node.id}")
        print(f"  标签: {node.label}")
        print(f"  中文标签: {node.label_zh}")
        print(f"  定义: {node.definition[:100]}..." if node.definition and len(node.definition) > 100 else f"  定义: {node.definition}")
        print(f"  子节点数量: {node.count}")
        print(f"  子节点: {[f'{child.childId}({child.relationType})' for child in node.children[:3]]}")
        print(f"  父节点: {[f'{parent.parentId}({parent.relationType})' for parent in node.parents[:3]]}")
