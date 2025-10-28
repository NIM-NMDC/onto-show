"""
本体解析 API 路由
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.services.ontology_service import OntologyService
from app.models.schema import TreeNode, ExportResponse
from app.core.config import OWL_FILE_PATH

router = APIRouter(prefix="/ontology", tags=["Ontology"])


def get_ontology_service() -> OntologyService:
    """获取本体服务实例"""
    return OntologyService(str(OWL_FILE_PATH))


@router.get(
    "/terms",
    response_model=List[TreeNode],
    summary="获取所有本体术语",
    description="获取 OWL 文件中的所有本体术语列表"
)
async def get_all_terms(
    service: OntologyService = Depends(get_ontology_service)
) -> List[TreeNode]:
    """
    获取所有本体术语
    
    Returns:
        List[TreeNode]: 本体术语列表
    """
    return service.get_all_terms()


@router.get(
    "/terms/{term_id}",
    response_model=TreeNode,
    summary="根据ID获取本体术语",
    description="根据术语ID获取特定的本体术语信息"
)
async def get_term_by_id(
    term_id: str,
    service: OntologyService = Depends(get_ontology_service)
) -> TreeNode:
    """
    根据ID获取本体术语
    
    Args:
        term_id: 术语ID
        
    Returns:
        TreeNode: 本体术语信息
        
    Raises:
        HTTPException: 当术语不存在时返回404
    """
    term = service.get_term_by_id(term_id)
    if not term:
        raise HTTPException(
            status_code=404, 
            detail=f"Term with ID '{term_id}' not found"
        )
    return term


@router.get(
    "/terms/search",
    response_model=List[TreeNode],
    summary="搜索本体术语",
    description="根据标签或定义搜索本体术语"
)
async def search_terms(
    q: str = Query(..., description="搜索关键词"),
    service: OntologyService = Depends(get_ontology_service)
) -> List[TreeNode]:
    """
    搜索本体术语
    
    Args:
        q: 搜索关键词
        
    Returns:
        List[TreeNode]: 匹配的术语列表
    """
    return service.search_terms(q)


@router.post(
    "/export",
    response_model=ExportResponse,
    summary="导出本体数据",
    description="将本体数据导出为JSON文件"
)
async def export_ontology(
    service: OntologyService = Depends(get_ontology_service)
) -> ExportResponse:
    """
    导出本体数据为JSON文件
    
    Returns:
        ExportResponse: 导出结果信息
    """
    try:
        output_file = service.export_to_json()
        return ExportResponse(
            message="Ontology data exported successfully",
            file_path=output_file,
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Export failed: {str(e)}"
        )


@router.get(
    "/stats",
    summary="获取本体统计信息",
    description="获取本体术语的统计信息"
)
async def get_ontology_stats(
    service: OntologyService = Depends(get_ontology_service)
) -> dict:
    """
    获取本体统计信息
    
    Returns:
        dict: 统计信息
    """
    return service.get_statistics()
