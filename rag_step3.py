#导入dashscope,用来吧问题转成向量
import dashscope
import os
#导入chromadb,用来查询数据库
import chromadb
#从环境变量读API Key
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
#1.连接已有的ChrromaDB
client = chromadb.PersistentClient(path="/home/qiancheng/english-tutor/chroma_db")
#获取之前创建的集合
collection = client.get_collection(name="multi_docs")
#2.输入问题
question = input("请输入你的问题:")
#3.把问题转成向量
response = dashscope.TextEmbedding.call(
    model="text-embedding-v3",
    input=question
)
question_embedding = response.output["embeddings"][0]["embedding"]
#4.在数据库里找最相似的3段
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)
#5.打印检索结果
print("\n=== 检索到的内容 ===")
# results["documents"][0] 是检索到的原文列表
# results["metadatas"][0] 是对应的元数据
# results["distances"][0] 是相似度距离（越小越相似）
for i in range(len(results["documents"][0])):
    print(f"\n--- 第{i+1}段 ---")
    print("内容:", results["documents"][0][i][:150])
    print("来源:", results["metadatas"][0][i])
    print("距离:", results["distances"][0][i])