# 导入 FastAPI 和请求体模型
from fastapi import FastAPI
from pydantic import BaseModel

# 导入 RAG 需要的库
import openai
import dashscope
import os
import chromadb

# 设置 API Key
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
openai.api_key = os.environ.get("DASHSCOPE_API_KEY")
openai.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 创建 FastAPI 应用
app = FastAPI()

# 连接 ChromaDB (启动时执行一次)
# 注意：这里改成我们最新建的多文档集合 multi_docs
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="multi_docs")

# 定义请求体模型
class Question(BaseModel):
    question: str

# 定义 RAG 回答函数
def ask_rag(question: str) -> str:
    try:
        # 1. 把问题转成向量
        response = dashscope.TextEmbedding.call(
            model="text-embedding-v3",
            input=question
        )
        # 先把 output 取出来
        output_data = response.output 
        question_embedding = output_data["embeddings"][0]["embedding"]
        
        # 2. 检索最相关的 3 段
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=3
        )
        
        # 3. 拼接检索内容
        context = "\n\n".join(results["documents"][0])
        
        # 4. 构造 prompt
        prompt = f"""请根据以下资料回答问题。如果资料里没有答案，就说"资料中没有相关信息"。
资料：
{context}

问题：{question}
"""
        
        # 5. 调用大模型（注意：换成 qwen-plus）
        response = openai.ChatCompletion.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个基于资料回答问题的助手。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"内部报错: {e}") # 打印真实错误
        return f"系统内部错误: {str(e)}"

# 定义 POST 接口
@app.post("/ask")
def ask(q: Question):
    answer = ask_rag(q.question)
    return {"answer": answer}
  