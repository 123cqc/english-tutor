#导入dashscope 库,调用Embedding API
import dashscope
import os
#导入ChromaDB,用来存向量
import chromadb
#从环境变量读 API Key
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
#导入文本切分器
from langchain_text_splitters import MarkdownHeaderTextSplitter
#1.读文件并切分
FILE_PATH = "/home/qiancheng/english-tutor/python_notes.md"
with open(FILE_PATH,"r",encoding="utf=8") as f:
    content = f.read()
headers_to_split_on = [
    ("#","一级标题"),
    ("##","二级1标题"),
]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
chunks = splitter.split_text(content)
#2.创建ChromaDB 客户端
#path 指定数据存到哪个目录
client = chromadb.PersistentClient(path="/home/qiancheng/english-tutor/chroma_db")

#创建一个集合
collection = client.get_or_create_collection(name="python_notes")

#3.把每段转成向量.存在ChromaDB
for i,chunk in enumerate(chunks):
    #调用Embedding API,把这段文字转成向量
    response = dashscope.TextEmbedding.call(
        model="text-embedding-v3",
        input=chunk.page_content
    )
    #从返回结果里提取向量
    embedding = response.output["embeddings"][0]["embedding"]

    #存入ChromaDB
    collection.add(
        ids=[f"chunk_{i}"],
        embeddings=[embedding],
        documents=[chunk.page_content],
        metadatas=[chunk.metadata],
    )
    print(f"已存入第{i+1}段")
print(f"\n全部完成,共存入{len(chunks)}段")