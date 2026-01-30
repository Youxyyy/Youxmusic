from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from music import music_bp
from db import init_db
import os

app = Flask(__name__)
CORS(app)  # 启用CORS

# 注册蓝图
app.register_blueprint(music_bp, url_prefix='/api')

# 初始化数据库
init_db(app)

# 静态文件服务 - 提供音乐文件
@app.route('/music_files/<path:filename>')
def serve_music(filename):
    """提供音乐文件"""
    music_folder = os.path.join(os.path.dirname(__file__), 'music_files')
    return send_from_directory(music_folder, filename)

# 静态文件服务 - 提供封面图片
@app.route('/covers/<path:filename>')
def serve_cover(filename):
    """提供封面图片"""
    covers_folder = os.path.join(os.path.dirname(__file__), 'covers')
    return send_from_directory(covers_folder, filename)

# 静态文件服务 - 提供用户头像
@app.route('/avatars/<path:filename>')
def serve_avatar(filename):
    """提供用户头像"""
    avatars_folder = os.path.join(os.path.dirname(__file__), 'avatars')
    return send_from_directory(avatars_folder, filename)

# 静态文件服务 - 提供歌单封面
@app.route('/static/playlist_covers/<path:filename>')
def serve_playlist_cover(filename):
    """提供歌单封面图片"""
    playlist_covers_folder = os.path.join(os.path.dirname(__file__), 'static', 'playlist_covers')
    return send_from_directory(playlist_covers_folder, filename)

# 静态文件服务 - 提供歌手头像
@app.route('/static/singers/<path:filename>')
def serve_singer_avatar(filename):
    """提供歌手头像图片"""
    singers_folder = os.path.join(os.path.dirname(__file__), 'static', 'singers')
    return send_from_directory(singers_folder, filename)

# 静态文件服务 - 提供背景图片
@app.route('/backgrounds/<path:filename>')
def serve_background(filename):
    """提供背景图片"""
    backgrounds_folder = os.path.join(os.path.dirname(__file__), 'backgrounds')
    return send_from_directory(backgrounds_folder, filename)

@app.route('/')
def index():
    return jsonify({
        "code": 200,
        "msg": "YouxMusic后端服务运行正常",
        "version": "1.0.0"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)