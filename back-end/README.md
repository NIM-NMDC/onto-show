# Ontology Parse API

一个基于 FastAPI 的本体解析服务，专门用于解析 OWL 文件并提供 RESTful API 接口。

## 🚀 功能特性

- **OWL 文件解析**：支持解析 OWL 本体文件，提取类和关系信息
- **RESTful API**：提供标准的 REST API 接口
- **多语言支持**：支持中英文标签和定义
- **关系解析**：支持 `subClassOf` 和 `partOf` 关系
- **搜索功能**：支持根据关键词搜索本体术语
- **数据导出**：支持将解析结果导出为 JSON 文件
- **统计信息**：提供本体术语的统计信息
- **自动文档**：自动生成 API 文档

## 📁 项目结构

```
owlParseAPI/
├── app/                          # 应用核心代码
│   ├── core/                     # 核心配置
│   │   ├── __init__.py
│   │   └── config.py            # 应用配置
│   ├── models/                   # 数据模型
│   │   ├── __init__.py
│   │   └── schema.py            # Pydantic 模型
│   ├── routers/                  # 路由层
│   │   ├── __init__.py
│   │   └── ontology_router.py   # 本体相关路由
│   ├── services/                 # 业务逻辑层
│   │   ├── __init__.py
│   │   └── ontology_service.py  # 本体服务
│   ├── utils/                    # 工具层
│   │   ├── __init__.py
│   │   ├── ontology_parser.py   # OWL 解析器
│   │   └── xml_cleaner.py       # XML 清理工具
│   └── psi-ms-zh.owl            # 本体数据文件
├── main.py                      # FastAPI 应用入口
├── start.py                     # 启动脚本
├── requirements.txt             # Python 依赖
├── Dockerfile                   # Docker 配置
├── docker-compose.yml           # Docker Compose 配置
├── test_main.http               # API 测试文件
└── README.md                    # 项目说明
```

## 🛠️ 技术栈

- **Web 框架**：FastAPI
- **数据解析**：RDFLib
- **数据验证**：Pydantic
- **数据格式**：OWL (Web Ontology Language)
- **API 文档**：Swagger UI / ReDoc
- **容器化**：Docker

## 📦 安装和运行

### 方式一：直接运行

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd owlParseAPI
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动服务**
   ```bash
   python start.py
   ```

### 方式二：使用 Docker

1. **构建镜像**
   ```bash
   docker build -t ontology-api .
   ```

2. **运行容器**
   ```bash
   docker run -p 8000:8000 ontology-api
   ```

### 方式三：使用 Docker Compose

```bash
docker-compose up -d
```

## 🌐 API 接口

### 基础信息

- **Base URL**: `http://localhost:8000`
- **API 版本**: `v1`
- **API 前缀**: `/api/v1`

### 接口列表

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/` | 根路径，返回 API 信息 |
| GET | `/health` | 健康检查 |
| GET | `/api/v1/ontology/terms` | 获取所有本体术语 |
| GET | `/api/v1/ontology/terms/{term_id}` | 根据ID获取术语 |
| GET | `/api/v1/ontology/terms/search?q={query}` | 搜索术语 |
| GET | `/api/v1/ontology/stats` | 获取统计信息 |
| POST | `/api/v1/ontology/export` | 导出数据为JSON |

### 接口示例

#### 获取所有术语
```bash
curl -X GET "http://localhost:8000/api/v1/ontology/terms"
```

#### 根据ID获取术语
```bash
curl -X GET "http://localhost:8000/api/v1/ontology/terms/MS:0000001"
```

#### 搜索术语
```bash
curl -X GET "http://localhost:8000/api/v1/ontology/terms/search?q=mass"
```

#### 导出数据
```bash
curl -X POST "http://localhost:8000/api/v1/ontology/export"
```

## 📊 数据模型

### TreeNode（本体术语节点）

```json
{
  "id": "MS:0000001",
  "label": "sample number",
  "label_zh": "样本编号",
  "definition": "A reference number relevant to the sample under study.",
  "definition_zh": "与所研究样本相关的参考编号。",
  "iri": "http://purl.obolibrary.org/obo/MS_0000001",
  "isLeaf": false,
  "count": 5,
  "children": [
    {
      "childId": "MS:0000002",
      "relationType": "subClassOf"
    }
  ],
  "parents": [
    {
      "parentId": "MS:1000548",
      "relationType": "subClassOf"
    }
  ]
}
```

## 🔧 配置说明

### 环境变量

- `DEBUG`: 调试模式（默认：False）
- `OWL_FILE_PATH`: OWL 文件路径

### 配置文件

主要配置在 `app/core/config.py` 中：

```python
# API 配置
API_V1_PREFIX = "/api/v1"
API_TITLE = "Ontology Parse API"
API_VERSION = "1.0.0"

# 文件配置
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = [".owl", ".rdf", ".xml"]

# 缓存配置
CACHE_TTL = 3600  # 1 hour
```

## 📚 API 文档

启动服务后，可以通过以下地址访问 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🧪 测试

### 使用 HTTP 文件测试

项目包含 `test_main.http` 文件，可以在支持 HTTP 文件的 IDE 中直接运行测试。

### 使用 curl 测试

```bash
# 健康检查
curl http://localhost:8000/health

# 获取所有术语
curl http://localhost:8000/api/v1/ontology/terms

# 搜索术语
curl "http://localhost:8000/api/v1/ontology/terms/search?q=mass"
```

## 🚀 部署

### 生产环境部署

1. **设置环境变量**
   ```bash
   export DEBUG=False
   export OWL_FILE_PATH=/path/to/your/ontology.owl
   ```

2. **使用 Gunicorn 部署**
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **使用 Docker 部署**
   ```bash
   docker-compose up -d
   ```

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔍 开发指南

### 添加新的 API 端点

1. 在 `app/routers/ontology_router.py` 中添加路由
2. 在 `app/services/ontology_service.py` 中添加业务逻辑
3. 在 `app/models/schema.py` 中添加数据模型（如需要）

### 添加新的数据模型

1. 在 `app/models/schema.py` 中定义 Pydantic 模型
2. 使用 `Field` 添加字段描述和验证规则

### 代码规范

- 使用类型提示
- 添加详细的文档字符串
- 遵循 PEP 8 代码风格
- 使用异步函数处理 I/O 操作

## 📝 更新日志

### v1.0.0 (2025-10-28)

- 初始版本发布
- 支持 OWL 文件解析
- 提供 RESTful API 接口
- 支持中英文标签和定义
- 支持关系解析（subClassOf, partOf）
- 支持搜索和统计功能
- 支持数据导出
- 提供完整的 API 文档

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 创建 Issue
- 发送邮件
- 提交 Pull Request

## 🙏 致谢

感谢所有为本项目做出贡献的开发者和用户。