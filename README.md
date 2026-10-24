# 🚀 Enterprise RAG Knowledge Base (企业级 RAG 智能问答系统)

## 📖 项目简介
本项目是一个基于大模型（LLM）与 RAG（检索增强生成）架构的企业级私有知识库问答系统。不仅提供精准的文档检索回答，还重点解决了大模型在真实业务场景下的**“知识幻觉”**与**“多轮对话指代不明”**等工程痛点。

## ✨ 核心特性 (Key Features)
- **🧠 精准的 RAG 检索**：基于 LangChain 与 ChromaDB 实现文档切片、向量化与 Top-K 相似度召回，有效防止大模型幻觉。
- **🔄 Query Rewrite (问题重写)**：针对多轮对话中的指代词（如“它有什么缺点”），系统会自动结合上下文重写为完整 Query，大幅提升检索召回率。
- **💾 会话记忆持久化**：接入 MySQL 数据库，实现聊天记录的实时落盘，支持基于历史记录的多轮对话。
- **🛡️ 模块化工程架构**：遵循单一职责原则（SRP），将数据库层、RAG 引擎层与 API 路由层彻底解耦，具备极高的可维护性。
- **🐳 一键容器化部署**：基于 Docker 容器化交付，解决环境依赖问题，实现快速部署上线。

## 🏗️ 系统架构图 (Architecture)
用户提问 -> FastAPI (接口层) -> MySQL (拉取历史) -> LLM (Query 重写)
                                                       ↓
用户回答 <- LLM (生成最终回答) <- 向量检索 (ChromaDB 检索资料) 

*(注：此处后续可替换为你自己画的精美架构图)*

## 🛠️ 技术栈 (Tech Stack)
- **核心语言**: Python 3.10
- **大模型 API**: 通义千问 (Qwen-plus) / DashScope Embedding
- **后端框架**: FastAPI, Pydantic
- **向量数据库**: ChromaDB, LangChain (Text Splitters)
- **关系型数据库**: MySQL 8.0
- **前端演示**: Streamlit
- **部署**: Docker

## 📂 目录结构
```text
english-tutor/
├── rag_api.py          # FastAPI 接口层（负责接收请求与路由）
├── rag_engine.py       # RAG 核心引擎层（负责检索与生成）
├── db_manager.py       # 数据库操作层（负责 MySQL 读写）
├── app.py              # Streamlit 前端演示
├── my_docs/            # 私有知识库文档（Markdown）
├── Dockerfile          # 容器化构建文件
└── requirements.txt    # 依赖清单
```

🚀 快速启动 (Quick Start)
1. 部署 MySQL 数据库
确保本地已启动 MySQL，并创建库与表：

sql
CREATE DATABASE ai_chat_db;
USE ai_chat_db;
CREATE TABLE chat_messages (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
2. 配置环境变量
bash
export DASHSCOPE_API_KEY="你的通义千问API Key"
3. Docker 启动后端服务
bash
docker build -t rag-api:v1 .
docker run -d --name rag-api -p 8001:8000 --add-host=host.docker.internal:host-gateway -e DASHSCOPE_API_KEY="$DASHSCOPE_API_KEY" rag-api:v1
4. 启动 Streamlit 前端演示
bash
pip install streamlit requests
streamlit run app.py
📈 性能与优化 (Performance)
文档规模：已验证 3 份 Markdown 文档（9 段文本）的批量入库与检索。

防幻觉机制：Prompt 约束机制实现在超纲测试下 100% 拒绝编造。

容器体积：镜像体积精简至 935 MB，实现秒级极速启动。