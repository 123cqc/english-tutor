# 导入 FastAPI 和请求体模型
from fastapi import FastAPI
from pydantic import BaseModel
#导入RAG 需要的库
import openai
import dashscope
import os
import chromadb
#设置API Key
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
openai.api_key = os.environ.get("DASHSCOPE_API_KEY")
openai.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
#创建FastAPI应用
app = FastAPI()
#连接ChromaDB(启动是执行一次)
client = chromadb.PersistentClient(path="/home/qiancheng/english-tutor/chroma_db")
collection = client.get_collection(name ="python_notes")
#定义请求体模型
class Question(BaseModel):
    question: str
#定义RAG回答函数
def ask_rag(question: str) -> str:
    #1.把问题转成向量
    response = dashscope.TextEmbedding.call(
          model="text-embedding-v3",
          input=question
    )
    question_embedding = response.output["embeddings"][0]["embedding"]
    #2.检索最相关的3段
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )
    #3.拼接检索内容
    context = "\n\n".join(results["documents"][0])
    #4.构造prompt
    prompt = f"""请根据以下资料回答问题。如果资料里没有答案，就说"资料中没有相关信息"。
资料：
{context}

问题：{question}
"""
    #5.调用大模型
    response = openai.ChatCompletion.create(
        model="qwen3.8-max",
        messages=[
            {"role": "system", "content": "你是一个基于资料回答问题的助手。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
#定义POST接口
@app.post("/ask")
def ask(q:Question):
    answer = ask_rag(q.question)
    return {"answer": answer}

  