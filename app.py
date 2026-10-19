import streamlit as st
import requests

st.set_page_config(page_title="AI 助手", page_icon="🤖")
st.title("🤖 智能 AI 助手")

# 初始化聊天历史（存在浏览器的 session 里）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 每次页面刷新，都重新渲染历史聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 在页面底部显示聊天输入框
if prompt := st.chat_input("在这里输入你的问题..."):
    # 1. 把用户的问题显示在页面上，并存入历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 调用后端 API
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                api_url = "http://localhost:8001/ask"
                response = requests.post(api_url, json={"question": prompt})
                
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.markdown(answer)
                    # 把 AI 的回答也存入历史
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("后端服务响应异常")
            except Exception as e:
                st.error(f"连接后端失败: {e}")