import openai
import json
import os
openai.api_key = os.environ.get("DASHSCOPE_API_KEY")
openai.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
#历史文件路径
HISTORY_FILE = os.path.expanduser("~/ai_tutor_history.json")
#如果历史文件存在,读进来;否则初始化
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE,"r",encoding="utf-8") as f:
        messages=json.load(f)
else:
        messages = [
                {"role":"system","contont":"You are an English assinstant.When the user sends an English sentence,you should: 1.Translate it to Chinese. 2.Point out any grammar mistakes. 3.Suggset a more natural expression"}
                ]
#主循环
while True:
    user_input = input("You:")
    if user_input == "exit":
        break
    #把用户输入加入历史
    messages.append({"role":"user","content":user_input})
    #调用API,传入完整的历史
    response = openai.ChatCompletion.create(
            model="qwen3.8-max",
            messages=messages
            )
    #提前AI回答
    reply = response.choices[0].message.content
    print("AI:",reply)
    #把AI的回答也加入历史
    messages.append({"role":"assistant","content":reply})
    #保存历史到文件
    with open(HISTORY_FILE,"w",encoding="utf-8") as f:
        json.dump(messages,f,ensure_ascii=False,indent=2)
