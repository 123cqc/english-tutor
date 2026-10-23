import pymysql
#写一个获取数据库连接的函数
def get_db_connection():
    return pymysql.connect(
        host='host.docker.internal',
        port=3306,
        user='root',
        password='root123',
        database='ai_chat_db',
        charset='utf8mb4'
    )

def get_chat_history(user_id: int, limit: int = 6):
    """从 MySQL 获取用户最近的聊天记录，并按时间正序返回"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM chat_messages WHERE user_id = %s ORDER BY id DESC LIMIT %s",
        (user_id, limit)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # 反转列表，变成按时间正序
    rows_list = list(rows) # 先把元组转成列表
    rows_list.reverse()    # 然后反转列表
    # 注意：这里是 row[0] 和 row[1]
    history = [{"role": row[0], "content": row[1]} for row in rows_list]
    return history

 #导入 FastAPI 和请求体模型
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
        # 1. 获取历史记录（只获取一次）
        history_messages = get_chat_history(user_id=1, limit=6)
        
        # 2. 问题重写 (Query Rewrite) -> 必须先做这一步！
        rewrite_messages = history_messages.copy()
        rewrite_messages.append({
            "role": "user", 
            "content": f"请结合上面的对话历史，将下面这句话重写为一个独立的、完整的问题。不要回答问题，只输出重写后的问题。如果原句已经很完整，直接输出原句。\n原句：{question}"
        })
        
        rewrite_response = openai.ChatCompletion.create(
            model="qwen-plus",
            messages=rewrite_messages
        )
        # 拿到重写后的问题
        rewritten_question = rewrite_response.choices[0].message.content.strip()
        print(f"✅ 原始问题: {question} -> 重写后: {rewritten_question}")
        
        # 3. 用【重写后的问题】去向量化检索
        response_embed = dashscope.TextEmbedding.call(
            model="text-embedding-v3",
            input=rewritten_question 
        )
        output_data = response_embed.output 
        question_embedding = output_data["embeddings"][0]["embedding"]
        
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=3
        )
        context = "\n\n".join(results["documents"][0])
        
        # 4. 构造 prompt
        prompt = f"""请根据以下资料回答问题。如果资料里没有答案，就说"资料中没有相关信息"。
资料：
{context}

问题：{rewritten_question}
"""
        
        # 5. 构造最终的 messages (系统+历史+当前)
        final_messages = [
            {"role": "system", "content": "你是一个基于资料回答问题的助手。"}
        ]
        final_messages.extend(history_messages)
        final_messages.append({"role": "user", "content": prompt})

        # 6. 调用大模型
        response = openai.ChatCompletion.create(
            model="qwen-plus",
            messages=final_messages
        )
        answer_text = response.choices[0].message.content
        
        # 7. 存数据库（存用户的原话，只存一次！）
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO chat_messages (user_id, role, content) VALUES (%s, %s, %s)", (1, 'user', question))
            cursor.execute("INSERT INTO chat_messages (user_id, role, content) VALUES (%s, %s, %s)", (1, 'assistant', answer_text))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"存数据失败:{e}")

        return answer_text

    except Exception as e:
        print(f"内部报错: {e}") 
        return f"系统内部错误: {str(e)}"
# 定义 POST 接口
@app.post("/ask")
def ask(q: Question):
    answer = ask_rag(q.question)
    return {"answer": answer}
  