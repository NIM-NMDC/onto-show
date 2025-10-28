"""
应用配置模块
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent.parent

# OWL 文件路径
OWL_FILE_PATH = BASE_DIR / "app" / "psi-ms-zh.owl"
OWL_FILE_CLEANED_PATH = BASE_DIR / "app" / "psi-ms-zh.owl"

# API 配置
API_V1_PREFIX = "/api/v1"
API_TITLE = "Ontology Parse API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "A FastAPI-based ontology parsing service for OWL files"

# 应用配置
APP_NAME = "Ontology Parse API"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# 文件配置
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = [".owl", ".rdf", ".xml"]

# 缓存配置
CACHE_TTL = 3600  # 1 hour
