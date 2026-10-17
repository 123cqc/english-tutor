# 1. 基础镜像：Python 3.10 轻量版
FROM docker.1ms.run/library/python:3.10-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 复制依赖清单
COPY requirements.txt .

# 4. 先升级 pip，再安装依赖
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
# 5. 复制项目代码
COPY . .

# 6. 暴露端口
EXPOSE 8000

# 7. 启动命令
CMD ["uvicorn", "rag_api:app", "--host", "0.0.0.0", "--port", "8000"]