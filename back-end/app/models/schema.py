"""
数据模型定义
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ParentRelation(BaseModel):
    """父节点关系"""
    parentId: str = Field(..., description="父节点ID")
    relationType: str = Field(..., description="关系类型: partOf | subClassOf")


class ChildRelation(BaseModel):
    """子节点关系"""
    childId: str = Field(..., description="子节点ID")
    relationType: str = Field(..., description="关系类型: partOf | subClassOf")


class TreeNode(BaseModel):
    """本体术语节点"""
    id: str = Field(..., description="术语ID")
    label: Optional[str] = Field(None, description="英文标签")
    label_zh: Optional[str] = Field(None, description="中文标签")
    definition: Optional[str] = Field(None, description="英文定义")
    definition_zh: Optional[str] = Field(None, description="中文定义")
    iri: Optional[str] = Field(None, description="国际资源标识符")
    isLeaf: bool = Field(True, description="是否为叶子节点")
    count: Optional[int] = Field(0, description="子节点数量")
    children: List[ChildRelation] = Field(default_factory=list, description="子节点列表")
    parents: List[ParentRelation] = Field(default_factory=list, description="父节点列表")


class ExportResponse(BaseModel):
    """导出响应模型"""
    message: str = Field(..., description="响应消息")
    file_path: str = Field(..., description="导出文件路径")
    status: str = Field(..., description="操作状态")


class SearchResponse(BaseModel):
    """搜索响应模型"""
    terms: List[TreeNode] = Field(..., description="匹配的术语列表")
    total: int = Field(..., description="总数量")
    query: str = Field(..., description="搜索关键词")


class StatisticsResponse(BaseModel):
    """统计信息响应模型"""
    total_terms: int = Field(..., description="总术语数量")
    total_classes: int = Field(..., description="类数量")
    total_relations: int = Field(..., description="关系数量")
    subClassOf_relations: int = Field(..., description="子类关系数量")
    partOf_relations: int = Field(..., description="部分关系数量")
    leaf_nodes: int = Field(..., description="叶子节点数量")
    max_depth: int = Field(..., description="最大深度")
