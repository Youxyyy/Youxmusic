from flask import g
import pymysql
from pymysql.cursors import DictCursor

# 数据库配置信息
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "wjy1227jy",
    "db": "youxmusicdb",
    "charset": "utf8mb4",
    "cursorclass": DictCursor
}

# 获取数据库连接
def get_db():
    db = getattr(g, "__database__", None)
    if db is None:
        db = g.__database__ = pymysql.connect(**DB_CONFIG)
    return db

# 关闭数据库连接
def close_db(exception):
    db = getattr(g, "__database__", None)
    if db is not None:
        db.close()

# 初始化数据库
def init_db(app):
    # 注册请求结束时，自动关闭数据库连接
    app.teardown_appcontext(close_db)

# 通用的数据库操作
def query_one(sql, params=None):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        result = cursor.fetchone()
        return result

def query_all(sql, params=None):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        result = cursor.fetchall()
        return result

def execute(sql, params=None):
    db = None
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(sql, params)
            db.commit()
            return True
    except Exception as ex:
        if db:
            db.rollback()
        print(f"数据库操作错误: {ex}")
        import traceback
        traceback.print_exc()
        return False