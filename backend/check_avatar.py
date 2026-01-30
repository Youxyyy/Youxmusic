"""检查用户头像配置"""
import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='wjy1227jy',
        database='youxmusic',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    
    print("查询用户头像信息：")
    cursor.execute("SELECT id, username, avatar FROM users")
    users = cursor.fetchall()
    
    for user in users:
        print(f"用户ID: {user[0]}, 用户名: {user[1]}, 头像: {user[2]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"错误: {e}")
