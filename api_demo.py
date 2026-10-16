from  fastapi import FastAPI
#创建app 对象
app = FastAPI()
#定义一个GET接口,路径是 /hello
@app.get("/hello")
def hello():
    return {"message":"Hello,FastAPI!"}
