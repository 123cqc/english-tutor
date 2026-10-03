"""
AI英语学习助手
---------------
基于通义千问API的英语学习工具，支持：
- 翻译英文句子
- 指出语法错误
- 给出更地道的表达建议
"""
import os
from openai import OpenAI
# 初始化客户端（通义千问，兼容OpenAI接口）
client = OpenAI(
        api_key=os.environ.get("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
# 对话历史，system消息定义AI角色
messages = [{"role":"system","content":"You are an English learning assistant.When the user sends an English sentence,you should: 1.Translate it to chinese.2.Point out any grammar mistakes.3.Suggest a more natural expression."}]
print("AI英语学习助手已启动，输入英文句子开始学习，输入exit退出。\n")
# 主循环：持续接收用户输入
while True:
    user_input = input("你:")
    if user_input == "exit":
        print("再见")
        break
    # 把用户输入加入对话历史
    messages.append({"role":"user","content":user_input})
    # 调用大模型API
    response = client.chat.completions.create(
            model="qwen-turbo",
            messages=messages
            )
    # 提取并打印AI回答
    reply = response.choices[0].message.content
    print("AI:",reply)
    messages.append({"role":"assistant","content":reply})
