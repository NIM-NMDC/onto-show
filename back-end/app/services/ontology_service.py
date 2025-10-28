"""
本体服务层
"""
from typing import List, Optional, Dict, Any
from app.utils.ontology_parser import parse_ontology, save_nodes_to_json
from app.models.schema import TreeNode, StatisticsResponse
import os
from pathlib import Path


class OntologyService:
    """本体服务类"""
    
    def __init__(self, owl_file_path: str):
        """
        初始化本体服务
        
        Args:
            owl_file_path: OWL 文件路径
        """
        self.owl_file_path = owl_file_path
        self._cache = None
        self._cache_timestamp = None
    
    def _get_parsed_data(self) -> Dict[str, TreeNode]:
        """获取解析后的数据（带缓存）"""
        import time
        current_time = time.time()
        
        # 检查缓存是否有效（1小时）
        if (self._cache is None or 
            self._cache_timestamp is None or 
            current_time - self._cache_timestamp > 3600):
            
            self._cache = parse_ontology(self.owl_file_path)
            self._cache_timestamp = current_time
        
        return self._cache
    
    def get_all_terms(self) -> List[TreeNode]:
        """
        获取所有本体术语
        
        Returns:
            List[TreeNode]: 本体术语列表
        """
        data = self._get_parsed_data()
        return list(data.values())
    
    def get_term_by_id(self, term_id: str) -> Optional[TreeNode]:
        """
        根据ID获取本体术语
        
        Args:
            term_id: 术语ID
            
        Returns:
            Optional[TreeNode]: 本体术语，如果不存在则返回None
        """
        data = self._get_parsed_data()
        return data.get(term_id)
    
    def search_terms(self, query: str) -> List[TreeNode]:
        """
        搜索本体术语
        
        Args:
            query: 搜索关键词
            
        Returns:
            List[TreeNode]: 匹配的术语列表
        """
        data = self._get_parsed_data()
        query_lower = query.lower()
        results = []
        
        for term in data.values():
            # 搜索英文标签
            if term.label and query_lower in term.label.lower():
                results.append(term)
                continue
            
            # 搜索中文标签
            if term.label_zh and query_lower in term.label_zh.lower():
                results.append(term)
                continue
            
            # 搜索英文定义
            if term.definition and query_lower in term.definition.lower():
                results.append(term)
                continue
            
            # 搜索中文定义
            if term.definition_zh and query_lower in term.definition_zh.lower():
                results.append(term)
                continue
        
        return results
    
    def export_to_json(self, output_file: Optional[str] = None) -> str:
        """
        导出本体数据为JSON文件
        
        Args:
            output_file: 输出文件路径，如果为None则自动生成
            
        Returns:
            str: 输出文件路径
        """
        data = self._get_parsed_data()
        return save_nodes_to_json(data, output_file)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取本体统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        data = self._get_parsed_data()
        terms = list(data.values())
        
        # 计算关系统计
        subClassOf_relations = 0
        partOf_relations = 0
        leaf_nodes = 0
        max_depth = 0
        
        for term in terms:
            # 统计关系
            for parent in term.parents:
                if parent.relationType == "subClassOf":
                    subClassOf_relations += 1
                elif parent.relationType == "partOf":
                    partOf_relations += 1
            
            # 统计叶子节点
            if term.isLeaf:
                leaf_nodes += 1
            
            # 计算深度（简单实现）
            depth = len(term.parents)
            max_depth = max(max_depth, depth)
        
        return {
            "total_terms": len(terms),
            "total_classes": len(terms),  # 所有节点都是类
            "total_relations": subClassOf_relations + partOf_relations,
            "subClassOf_relations": subClassOf_relations,
            "partOf_relations": partOf_relations,
            "leaf_nodes": leaf_nodes,
            "max_depth": max_depth
        }
    
    def clear_cache(self):
        """清除缓存"""
        self._cache = None
        self._cache_timestamp = None