from fastapi import FastAPI
from pydantic import BaseModel
from db_manager import save_chat_message
from rag_engine import ask_rag

app = FastAPI()

class Question(BaseModel):
    question: str
    user_id: int = 1 # 顺便把 user_id 变成动态的

@app.post("/ask")
def ask(q: Question):
    # 1. 存用户提问
    save_chat_message(user_id=q.user_id, role='user', content=q.question)
    
    # 2. 获取 AI 回答
    answer = ask_rag(question=q.question, user_id=q.user_id)
    
    # 3. 存 AI 回答
    save_chat_message(user_id=q.user_id, role='assistant', content=answer)
    
    return {"answer": answer}