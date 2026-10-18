# 导入 openai，用来调用大模型生成回答
import openai
import os

# 设置 API Key 和 base_url（旧版写法）
openai.api_key = os.environ.get("DASHSCOPE_API_KEY")
openai.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# 导入 dashscope，用来把问题转成向量
import dashscope
import os

# 导入 chromadb，用来查询数据库
import chromadb

# 从环境变量读 API Key
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

# 1. 连接已有的 ChromaDB
client = chromadb.PersistentClient(path="/home/qiancheng/english-tutor/chroma_db")

# 获取之前创建的集合
collection = client.get_collection(name="multi_docs")

# 2. 输入问题
question = input("请输入你的问题: ")

# 3. 把问题转成向量
response = dashscope.TextEmbedding.call(
    model="text-embedding-v3",
    input=question
)

question_embedding = response.output["embeddings"][0]["embedding"]

# 4. 在数据库里找最相似的 3 段
results = collection.query(
    query_embeddings=[question_embedding],   # 用问题的向量去查
    n_results=3                               # 返回最相似的 3 段
)

# 5. 打印检索结果
print("\n=== 检索到的内容 ===")

# results["documents"][0] 是检索到的原文列表
# results["metadatas"][0] 是对应的元数据
# results["distances"][0] 是相似度距离（越小越相似）
for i in range(len(results["documents"][0])):
    print(f"\n--- 第 {i+1} 段 ---")
    print("内容:", results["documents"][0][i][:150])
    print("来源:", results["metadatas"][0][i])
    print("距离:", results["distances"][0][i])

results = collection.query(
    query_embeddings=[question_embedding],   # 用问题的向量去查
    n_results=3                               # 返回最相似的 3 段
)
#2.把检索到的内容拼接成一个字符串
context = "\n\n".join(results["documents"][0])

#3.构造prompt
prompt = f"""请根据以下资料回答问题.如何资料里没有答案,就说"资料中没有相关信息"
资料:
{context}
问题:{question}
"""
#4.发给大模型
#用OpenAI库
response = openai.ChatCompletion.create(
    model="qwen3.8-max",
    messages=[
        {"role": "system", "content": "你是一个基于资料回答问题的助手。"},
        {"role": "user", "content": prompt}
    ]
)
print(response.choices[0].message.content)