import os
import json
import dashscope
from agent_tools import get_server_status

# 从环境变量读取 Key
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

# 1. 定义“工具说明书”
# 告诉大模型，我们有一个叫 get_server_status 的工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_server_status",
            "description": "获取当前服务器的CPU和内存使用率",
            "parameters": {}  # 这个工具不需要传参数
        }
    }
]

# 2. 初始化对话历史
messages = [
    {"role": "system", "content": "你是一个智能运维助手，你可以调用工具来查询服务器状态。"},
    {"role": "user", "content": "帮我看一下现在服务器的CPU和内存占用高不高？"}
]

print("正在请求大模型...")

# 3. 第一次请求大模型
response = dashscope.Generation.call(
    model="qwen-plus",
    messages=messages,
    tools=tools  # 把说明书传给大模型
)
print("大模型原始返回:", response)
# 4. 检查大模型是不是要调用工具
# 注意：tool_calls 在 choices[0].message 里
message = response.output["choices"][0]["message"]

if message.get("tool_calls"):
    # 拿到大模型要求的工具名
    tool_call = message["tool_calls"][0]
    function_name = tool_call["function"]["name"]
    
    print(f"大模型决定调用工具: {function_name}")
    
    # 5. 本地执行工具函数
    if function_name == "get_server_status":
        result = get_server_status()
        print(f"工具执行结果: {result}")
        
        # 6. 把工具执行的结果，作为一条新消息发给大模型
        # 这里要注意把 assistant 的原始消息和 tool 的结果都加入历史
        messages.append(message) 
        messages.append({
            "role": "tool",
            "content": result,
            "tool_call_id": tool_call["id"] 
        })
        
        # 7. 第二次请求大模型，让它根据结果总结回答
        print("正在请求大模型总结回答...")
        final_response = dashscope.Generation.call(
            model="qwen-plus",  # 记得还是用纯文本模型
            messages=messages
        )
        
        print("\n=== 最终回答 ===")
        # 最终回答的文本在 output.text 里
        print(final_response.output.text)
else:
    # 如果大模型没调用工具，直接回答了
    print("\n=== 直接回答 ===")
    print(message.get("content"))