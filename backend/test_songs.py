import pymysql
from pymysql.cursors import DictCursor

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "wjy1227jy",
    "db": "youxmusicdb",
    "charset": "utf8mb4",
    "cursorclass": DictCursor
}

try:
    # 连接数据库
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 查询歌曲
    cursor.execute("SELECT id, title, artist, file_path, cover_image FROM songs LIMIT 5")
    songs = cursor.fetchall()
    
    print("数据库中的歌曲数据：")
    print("-" * 80)
    for song in songs:
        print(f"ID: {song['id']}")
        print(f"标题: {song['title']}")
        print(f"歌手: {song['artist']}")
        print(f"文件路径: {song['file_path']}")
        print(f"封面: {song['cover_image']}")
        print("-" * 80)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"错误: {e}")
