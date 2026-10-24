import pymysql

def get_db_connection():
    return pymysql.connect(
        host='host.docker.internal',
        port=3306,
        user='root',
        password='root123',
        database='ai_chat_db',
        charset='utf8mb4'
    )

def get_chat_history(user_id:int,limit:int=6):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role,content FROM chat_messages WHERE user_id = %s ORDER BY id DESC LIMIT %s",
        (user_id,limit)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    rows_list = list(rows)
    rows_list.reverse()
    return [{"role":row[0],"content":row[1]} for row in rows_list]

def save_chat_message(user_id:int,role:str,content:str):
    """新增一个专门保存消息的函数"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_messages (user_id,role,content) VALUES (%s,%s,%s)",
            (user_id,role,content)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"存数据失败:{e}")