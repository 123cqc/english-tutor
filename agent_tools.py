import psutil

def get_server_status() -> str:
    """
    获取当前服务器的 CPU 和内存使用率
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    mem_percent = memory.percent
    
    return f"当前 CPU 使用率: {cpu_percent}%, 内存使用率: {mem_percent}%"