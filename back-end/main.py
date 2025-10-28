"""
Ontology Parse API - FastAPI 应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ontology_router
from app.core.config import API_TITLE, API_VERSION, API_DESCRIPTION, API_V1_PREFIX

# 创建 FastAPI 应用实例
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(ontology_router.router, prefix=API_V1_PREFIX)


@app.get("/", tags=["Root"])
async def root():
    """根路径，返回API信息"""
    return {
        "message": "Welcome to Ontology Parse API",
        "version": API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "ontology-parse-api"}
