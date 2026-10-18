import os
import time
import dashscope
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 初始化
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
client = chromadb.PersistentClient(path="./chroma_db")

# 更换新的集合名字，防止和 python_notes 冲突
collection_name = "multi_docs"
collection = client.get_or_create_collection(name=collection_name)

# 2. 设置切分器（固定切 500 个字符，重叠 50 个字符）
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, 
    chunk_overlap=50,
    separators=["\n## ", "\n# ", "\n\n", "\n", " ", ""]
)

# 3. 读取 my_docs 文件夹下的所有 .md 文件
DOCS_DIR = "./my_docs"
all_chunks = []

print("开始读取文档")
for filename in os.listdir(DOCS_DIR):
    if filename.endswith(".md"):
        file_path = os.path.join(DOCS_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

            # 使用 split_text 切分
            raw_chunks = splitter.split_text(content)

            # 手动包装类
            class ChunkWrapper:
                def __init__(self, text, meta):
                    self.page_content = text
                    self.metadata = meta

            # 把切好的文本包装起来
            chunks = [ChunkWrapper(text, {"source_file": filename}) for text in raw_chunks]

            # 注意：这里用 extend 将列表展平，不要用 append
            all_chunks.extend(chunks)

            print(f"已读取: {filename}, 切分出 {len(chunks)} 段")

print(f"\n总共切分出 {len(all_chunks)} 段文本。")

# 4. 批量向量化并入库
print("开始向量化并存入数据库...")
start_time = time.time()

# 记录一个时间戳，用于生成唯一的 ID，防止重复运行覆盖旧数据
batch_timestamp = int(time.time())

for i, chunk in enumerate(all_chunks):
    response = dashscope.TextEmbedding.call(
        model="text-embedding-v3",
        input=chunk.page_content
    )
    # 注意：这里必须用字典键取值 ["embedding"]
    embedding = response.output["embeddings"][0]["embedding"]

    # 存入数据库
    collection.add(
        ids=[f"chunk_{batch_timestamp}_{i}"],
        embeddings=[embedding],
        documents=[chunk.page_content],
        metadatas=[chunk.metadata]
    )

    # 每五段打印一次进度，避免刷屏
    if (i + 1) % 5 == 0 or (i + 1) == len(all_chunks):
        print(f"已处理 {i + 1}/{len(all_chunks)} 段...")

end_time = time.time()
print(f"\n全部入库完成！总耗时: {end_time - start_time:.2f} 秒")