# 导入文本切分器
from langchain_text_splitters import MarkdownHeaderTextSplitter

# 1. 直接用 Python 自带的 open 读取文件
FILE_PATH = "/home/qiancheng/english-tutor/python_notes.md"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 2. 打印读取结果
print("文档内容长度:", len(content))
print("前 200 个字符:")
print(content[:200])

# 3. 按 Markdown 标题切分
headers_to_split_on = [
    ("#", "一级标题"),
    ("##", "二级标题"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# 对文档内容进行切分
chunks = splitter.split_text(content)

# 4. 打印切分结果
print("\n切分后的段落数量:", len(chunks))
print("\n前 3 个段落的内容:")
for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- 第 {i+1} 段 ---")
    print("内容:", chunk.page_content[:100])
    print("元数据:", chunk.metadata)