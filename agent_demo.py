import os
import json
import dashscope
from agent_tools import get_contract_by_name,check_risks_keywords

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

#1.定义工具说明书(JSON Schema)
tools = [
    {
        "type":"function",
        "function":{
            "name":"get_contract_by_name",
            "description":"根据客户姓名查询合同文本内容",
            "parameters":{
                "type":"object",
                "properties":{"name":{"type":"string","description":"客户姓名"}},
                "required":["name"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"check_risk_keywords",
            "description":"检查合同文本中是否包含高风险/违规词汇",
            "parameters":{
                "type":"object",
                "propreties":{"text":{"type":"string","description":"需要检查的合同文本"}},
                "requied":["text"]
            }
        }
    }
]

messages = [
     {"role": "system", "content": "你是一个专业的企业法务风控助手。请审核客户合同，你需要先查询合同内容，再检查是否有风险词汇，最后生成一份审核报告。"},
    {"role": "user", "content": "请帮我审核一下张三的合同，看看有没有风险。"}
]

#2.引入工程化机制:最大迭代次数(防止死循环)
MAX_ITERATIONS = 5
iteration = 0

while iteration  <  MAX_ITERATIONS:
    iteration += 1
    print(f"\n--- 第{iteration}轮思考")

    #请求大模型
    response = dashscope.Generation.call(
        model="qwen-plus",
        messages=messages,
        tools=tools
    )

    #拿到大模型的回答
    message = response.output["choices"][0]["message"]
    messages.append(message)#把模型的思考记录加入历史

    #如果大模型没有调用工具,说明它思考完毕,给出了最终回答
    if not message.get("tool_calls"):
        print("\n=== 最终审核报告 ===")
        print(message.get("content"))
        break

    #如果调用了工具,开始执行
    for tool_call in message["tool_calls"]:
        function_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])

        print(f"大模型决定调用工具:{function_name},参数:{arguments}")

        #3.引入工程化机制:Try-Except 异常捕获与降级
        try:
            if function_name == "get_contract_by_name":
                result = get_contract_by_name(arguments["name"])
            elif function_name == "check_risk_keyword":
                result = check_risks_keywords(arguments["text"])
            else:
                result = "未知工具调用"
        except Exception as e:
            #如果工具内容崩溃(比如数据库断连),优雅降级
            result = f"工具执行失败,原因:{str(e)},请告诉用户系统繁忙,稍后重试."
            print(f"❌{result}")
        print(f"工具执行结果:{result}")

        #把工具执行结果塞回给大模型
        messages.append({
            "role":"tool",
            "content":result,
            "tool_call_id":tool_call["id"]
        })

#如果循环超过了最大次数
if iteration >= MAX_ITERATIONS:
    print("\n⚠️ 系统提示:Agent 思考次数过多,已触发熔断保护机制,强制终止.")