import os
import openai
import dashscope
import chromadb
from db_manager import get_chat_history

#初始化连接
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
openai.api_key = os.environ.get("DASHSCOPE_API_KEY")
openai.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="multi_docs")

def ask_rag(question:str,user_id:int) -> str:
    """核心 RAG 逻辑,只负责思考和查资料"""
    try:
        #1.拿历史
        history_messages = get_chat_history(user_id=user_id,limit=6)

        #2.问题重写
        rewrite_messages = history_messages.copy()
        rewrite_messages.append({
            "role": "user", 
            "content": f"请结合上面的对话历史，将下面这句话重写为一个独立的、完整的问题。不要回答问题，只输出重写后的问题。如果原句已经很完整，直接输出原句。\n原句：{question}"
        })
        rewrite_response = openai.ChatCompletion.create(model="qwen-plus",messages=rewrite_messages)
        rewritten_question = rewrite_response.choices[0].message.content.strip()
        print(f"✅ 原始问题: {question} -> 重写后: {rewritten_question}")

        #3.检索
        response_embed = dashscope.TextEmbedding.call(model="text-embedding-v3",input=rewritten_question)
        question_embedding = response_embed.output["embeddings"][0]["embedding"]
        results = collection.query(query_embeddings=[question_embedding],n_results=3)
        context = "\n\n".join(results["documents"][0])

        #4.拼prompt
        prompt = f"请根据以下资料回答问题。如果资料里没有答案，就说'资料中没有相关信息'。\n资料：\n{context}\n\n问题：{rewritten_question}\n"

        #5.最终生成
        final_messages = [{"role":"system","content":"你是一个基于资料回答的助手."}]
        final_messages.extend(history_messages)
        final_messages.append({"role":"user","content":prompt})

        response = openai.ChatCompletion.create(model="qwen-plus",messages=final_messages)
        return response.choices[0].message.content

    except Exception as e:
        print(f"RAG内部报错:{e}")
        return f"系统内部错误:{str(e)}"