"""
AI 英语学习助手
----------------
基于通义千问API的英语学习工具
"""
import os
import json
from openai import OpenAI
# 初始化客户端
client = OpenAI(
        api_key=os.environ.get("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
# 历史文件路径
HISTORY_FILE = os.path.expanduser("~/english-tutor/history.json")
# 读取历史，如果文件不存在，就初始化
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE,"r",encoding="utf-8") as f:
        messages = json.load(f)
else:
    messages = [
            {"role":"system","content":"You are an English learning assistant..."}
            ]
# 打印欢迎语
print("AI 英语学习助手已启动，输入英文句子开始学习，输入exit退出。\n")
# 主循环
while True:
    user_input = input("You:")
    if user_input == "exit":
        print("再见！")
        break
    messages.append({"role":"user","content":user_input})
    response = client.chat.completions.create(
            model="qwen-turbo",
            messages=messages
            )
    reply = response.choices[0].message.content
    print("AI:",reply)
    messages.append({"role":"assistant","content":reply})
    with open(HISTORY_FILE,"w",encoding="utf-8") as f:
        json.dump(messages,f,ensure_ascii=False,indent=2)
