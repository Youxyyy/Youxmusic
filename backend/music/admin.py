from flask import Blueprint, request, jsonify
import jwt
import os
from werkzeug.utils import secure_filename
from db import query_one, query_all, execute

admin_bp = Blueprint('admin', __name__)

# JWT配置
JWT_SECRET = 'your-secret-key-here'

# 文件上传配置
UPLOAD_FOLDER = 'music_files'
COVER_FOLDER = 'covers'
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'flac', 'm4a'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

def get_user_from_token():
    """从token获取用户信息"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = payload.get('user_id')
        # 查询用户信息，包括是否为管理员
        user = query_one("SELECT id, username, is_admin FROM users WHERE id = %s", (user_id,))
        return user
    except:
        return None

def check_admin():
    """检查是否为管理员"""
    user = get_user_from_token()
    if not user:
        return False, "未登录"
    if not user.get('is_admin'):
        return False, "无管理员权限"
    return True, user

def allowed_file(filename, allowed_extensions):
    """检查文件扩展名"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# 检查管理员权限
@admin_bp.route('/check', methods=['GET'])
def check_admin_permission():
    """检查当前用户是否为管理员"""
    user = get_user_from_token()
    if not user:
        return jsonify({"is_admin": False, "message": "未登录"}), 401
    
    return jsonify({
        "is_admin": user.get('is_admin', False),
        "username": user.get('username')
    }), 200

# 上传歌曲
@admin_bp.route('/songs/upload', methods=['POST'])
def upload_song():
    """上传歌曲"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        # 获取表单数据
        title = request.form.get('title')
        artist = request.form.get('artist')
        album = request.form.get('album', '')
        duration = request.form.get('duration', 0)
        genre = request.form.get('genre', '')
        release_year = request.form.get('release_year', None)
        
        if not title or not artist:
            return jsonify({"error": "歌曲名称和歌手不能为空"}), 400
        
        # 处理音频文件
        if 'audio_file' not in request.files:
            return jsonify({"error": "请上传音频文件"}), 400
        
        audio_file = request.files['audio_file']
        if audio_file.filename == '':
            return jsonify({"error": "未选择音频文件"}), 400
        
        if not allowed_file(audio_file.filename, ALLOWED_AUDIO_EXTENSIONS):
            return jsonify({"error": "不支持的音频格式"}), 400
        
        # 保存音频文件
        audio_filename = secure_filename(audio_file.filename)
        audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        audio_file.save(audio_path)
        
        # 处理封面图片（可选）
        cover_path = None
        if 'cover_file' in request.files:
            cover_file = request.files['cover_file']
            if cover_file.filename != '' and allowed_file(cover_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                cover_filename = secure_filename(cover_file.filename)
                cover_path = os.path.join(COVER_FOLDER, cover_filename)
                os.makedirs(COVER_FOLDER, exist_ok=True)
                cover_file.save(cover_path)
                cover_path = f'/{cover_path}'
        
        # 插入数据库
        success = execute(
            """INSERT INTO songs (title, artist, album, duration, file_path, cover_image, genre, release_year)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (title, artist, album, duration, f'/{audio_path}', cover_path, genre, release_year)
        )
        
        if success:
            # 获取新插入的歌曲
            song = query_one(
                "SELECT * FROM songs ORDER BY id DESC LIMIT 1"
            )
            return jsonify({
                "message": "上传成功",
                "song": song
            }), 201
        else:
            return jsonify({"error": "上传失败"}), 500
            
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"上传歌曲错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 更新歌曲信息
@admin_bp.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    """更新歌曲信息"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        data = request.get_json()
        
        # 检查歌曲是否存在
        song = query_one("SELECT id FROM songs WHERE id = %s", (song_id,))
        if not song:
            return jsonify({"error": "歌曲不存在"}), 404
        
        # 构建更新语句
        update_fields = []
        params = []
        
        if 'title' in data:
            update_fields.append("title = %s")
            params.append(data['title'])
        if 'artist' in data:
            update_fields.append("artist = %s")
            params.append(data['artist'])
        if 'album' in data:
            update_fields.append("album = %s")
            params.append(data['album'])
        if 'duration' in data:
            update_fields.append("duration = %s")
            params.append(data['duration'])
        if 'genre' in data:
            update_fields.append("genre = %s")
            params.append(data['genre'])
        if 'release_year' in data:
            update_fields.append("release_year = %s")
            params.append(data['release_year'])
        
        if not update_fields:
            return jsonify({"error": "没有要更新的字段"}), 400
        
        params.append(song_id)
        sql = f"UPDATE songs SET {', '.join(update_fields)} WHERE id = %s"
        
        success = execute(sql, tuple(params))
        
        if success:
            # 获取更新后的歌曲
            updated_song = query_one("SELECT * FROM songs WHERE id = %s", (song_id,))
            return jsonify({
                "message": "更新成功",
                "song": updated_song
            }), 200
        else:
            return jsonify({"error": "更新失败"}), 500
            
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"更新歌曲错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 删除歌曲
@admin_bp.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    """删除歌曲"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        # 检查歌曲是否存在
        song = query_one("SELECT * FROM songs WHERE id = %s", (song_id,))
        if not song:
            return jsonify({"error": "歌曲不存在"}), 404
        
        # 删除文件（可选）
        # 这里可以添加删除实际文件的逻辑
        
        # 删除数据库记录
        success = execute("DELETE FROM songs WHERE id = %s", (song_id,))
        
        if success:
            return jsonify({"message": "删除成功"}), 200
        else:
            return jsonify({"error": "删除失败"}), 500
            
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 获取所有歌曲（管理员视图）
@admin_bp.route('/songs', methods=['GET'])
def get_all_songs_admin():
    """获取所有歌曲（管理员）"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        offset = (page - 1) * per_page
        
        songs = query_all(
            "SELECT * FROM songs ORDER BY id ASC LIMIT %s OFFSET %s",
            (per_page, offset)
        )
        
        total = query_one("SELECT COUNT(*) as count FROM songs")
        
        return jsonify({
            "songs": songs if songs else [],
            "total": total['count'] if total else 0,
            "page": page,
            "per_page": per_page
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 获取统计信息
@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        # 歌曲总数
        songs_count = query_one("SELECT COUNT(*) as count FROM songs")
        
        # 用户总数
        users_count = query_one("SELECT COUNT(*) as count FROM users")
        
        # 歌单总数
        playlists_count = query_one("SELECT COUNT(*) as count FROM playlists")
        
        # 总播放次数
        total_plays = query_one("SELECT SUM(play_count) as total FROM songs")
        
        # 歌手总数
        singers_count = query_one("SELECT COUNT(*) as count FROM singers")
        
        # 收藏总数
        favorites_count = query_one("SELECT COUNT(*) as count FROM favorite_songs")
        
        return jsonify({
            "songs_count": songs_count['count'] if songs_count else 0,
            "users_count": users_count['count'] if users_count else 0,
            "playlists_count": playlists_count['count'] if playlists_count else 0,
            "total_plays": total_plays['total'] if total_plays and total_plays['total'] else 0,
            "total_singers": singers_count['count'] if singers_count else 0,
            "total_favorites": favorites_count['count'] if favorites_count else 0
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# ==================== 歌手管理 ====================

@admin_bp.route('/singers', methods=['GET'])
def get_all_singers():
    """获取所有歌手（管理员）"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        singers = query_all("""
            SELECT s.*, 
                   COUNT(DISTINCT ss.song_id) as song_count
            FROM singers s
            LEFT JOIN song_singers ss ON s.id = ss.singer_id
            GROUP BY s.id
            ORDER BY s.id ASC
        """)
        
        return jsonify({
            "code": 200,
            "data": {
                "singers": singers if singers else []
            }
        }), 200
        
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

@admin_bp.route('/singers', methods=['POST'])
def create_singer():
    """创建歌手"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        data = request.get_json()
        name = data.get('name')
        country = data.get('country', '中国')
        genre = data.get('genre', '流行')
        bio = data.get('bio', '')
        avatar = data.get('avatar', '')
        
        if not name:
            return jsonify({"code": 400, "error": "歌手名称不能为空"}), 400
        
        # 检查歌手是否已存在
        existing = query_one("SELECT id FROM singers WHERE name = %s", (name,))
        if existing:
            return jsonify({"code": 400, "error": "歌手已存在"}), 400
        
        # 插入歌手
        success = execute(
            "INSERT INTO singers (name, country, genre, bio, avatar) VALUES (%s, %s, %s, %s, %s)",
            (name, country, genre, bio, avatar)
        )
        
        if success:
            return jsonify({"code": 200, "message": "创建成功"}), 200
        else:
            return jsonify({"code": 500, "error": "创建失败"}), 500
        
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

@admin_bp.route('/singers/<int:singer_id>', methods=['PUT'])
def update_singer(singer_id):
    """更新歌手信息"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        data = request.get_json()
        name = data.get('name')
        country = data.get('country')
        genre = data.get('genre')
        bio = data.get('bio')
        avatar = data.get('avatar')
        
        if not name:
            return jsonify({"code": 400, "error": "歌手名称不能为空"}), 400
        
        # 检查歌手是否存在
        singer = query_one("SELECT id FROM singers WHERE id = %s", (singer_id,))
        if not singer:
            return jsonify({"code": 404, "error": "歌手不存在"}), 404
        
        # 检查名称是否与其他歌手重复
        existing = query_one("SELECT id FROM singers WHERE name = %s AND id != %s", (name, singer_id))
        if existing:
            return jsonify({"code": 400, "error": "歌手名称已存在"}), 400
        
        # 更新歌手
        success = execute(
            "UPDATE singers SET name = %s, country = %s, genre = %s, bio = %s, avatar = %s WHERE id = %s",
            (name, country, genre, bio, avatar, singer_id)
        )
        
        if success:
            return jsonify({"code": 200, "message": "更新成功"}), 200
        else:
            return jsonify({"code": 500, "error": "更新失败"}), 500
        
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

@admin_bp.route('/singers/<int:singer_id>', methods=['DELETE'])
def delete_singer(singer_id):
    """删除歌手"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        # 检查歌手是否存在
        singer = query_one("SELECT id, name FROM singers WHERE id = %s", (singer_id,))
        if not singer:
            return jsonify({"code": 404, "error": "歌手不存在"}), 404
        
        # 删除歌手（外键约束会自动删除关联记录）
        success = execute("DELETE FROM singers WHERE id = %s", (singer_id,))
        
        if success:
            return jsonify({"code": 200, "message": "删除成功"}), 200
        else:
            return jsonify({"code": 500, "error": "删除失败"}), 500
        
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

# ==================== 用户管理 ====================

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    """获取所有用户"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        users = query_all("""
            SELECT u.id, u.username, u.email, u.is_admin, u.created_at,
                   COUNT(DISTINCT p.id) as playlist_count,
                   COUNT(DISTINCT f.id) as favorite_count
            FROM users u
            LEFT JOIN playlists p ON u.id = p.user_id
            LEFT JOIN favorite_songs f ON u.id = f.user_id
            GROUP BY u.id
            ORDER BY u.id ASC
        """)
        
        return jsonify({
            "code": 200,
            "data": {
                "users": users if users else []
            }
        }), 200
        
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

@admin_bp.route('/users/<int:user_id>/admin', methods=['PUT'])
def toggle_admin(user_id):
    """切换用户管理员权限"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        data = request.get_json()
        is_admin_status = data.get('is_admin', False)
        
        # 检查用户是否存在
        user = query_one("SELECT id FROM users WHERE id = %s", (user_id,))
        if not user:
            return jsonify({"code": 404, "error": "用户不存在"}), 404
        
        # 更新管理员权限
        success = execute("UPDATE users SET is_admin = %s WHERE id = %s", (is_admin_status, user_id))
        
        if success:
            return jsonify({"code": 200, "message": "权限更新成功"}), 200
        else:
            return jsonify({"code": 500, "error": "更新失败"}), 500
        
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        # 检查用户是否存在
        user = query_one("SELECT id, username FROM users WHERE id = %s", (user_id,))
        if not user:
            return jsonify({"code": 404, "error": "用户不存在"}), 404
        
        # 删除用户（外键约束会自动删除关联记录）
        success = execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        if success:
            return jsonify({"code": 200, "message": "删除成功"}), 200
        else:
            return jsonify({"code": 500, "error": "删除失败"}), 500
        
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500


# ==================== 歌曲推荐管理 ====================

@admin_bp.route('/songs/<int:song_id>/featured', methods=['PUT'])
def toggle_song_featured(song_id):
    """切换歌曲首页推荐状态"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        data = request.get_json()
        is_featured = data.get('is_featured', False)
        
        # 检查歌曲是否存在
        song = query_one("SELECT id FROM songs WHERE id = %s", (song_id,))
        if not song:
            return jsonify({"code": 404, "error": "歌曲不存在"}), 404
        
        # 更新推荐状态
        success = execute("UPDATE songs SET is_featured = %s WHERE id = %s", (is_featured, song_id))
        
        if success:
            return jsonify({"code": 200, "message": "更新成功"}), 200
        else:
            return jsonify({"code": 500, "error": "更新失败"}), 500
        
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

@admin_bp.route('/songs/<int:song_id>/new', methods=['PUT'])
def toggle_song_new(song_id):
    """切换歌曲新歌状态"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        data = request.get_json()
        is_new = data.get('is_new', False)
        
        # 检查歌曲是否存在
        song = query_one("SELECT id FROM songs WHERE id = %s", (song_id,))
        if not song:
            return jsonify({"code": 404, "error": "歌曲不存在"}), 404
        
        # 更新新歌状态
        success = execute("UPDATE songs SET is_new = %s WHERE id = %s", (is_new, song_id))
        
        if success:
            return jsonify({"code": 200, "message": "更新成功"}), 200
        else:
            return jsonify({"code": 500, "error": "更新失败"}), 500
        
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

@admin_bp.route('/songs/<int:song_id>/recommended', methods=['PUT'])
def toggle_song_recommended(song_id):
    """切换歌曲推荐状态（首页推荐歌曲板块）"""
    is_admin, result = check_admin()
    if not is_admin:
        return jsonify({"error": result}), 403
    
    try:
        data = request.get_json()
        is_recommended = data.get('is_recommended', False)
        
        # 检查歌曲是否存在
        song = query_one("SELECT id FROM songs WHERE id = %s", (song_id,))
        if not song:
            return jsonify({"code": 404, "error": "歌曲不存在"}), 404
        
        # 更新推荐状态
        success = execute("UPDATE songs SET is_recommended = %s WHERE id = %s", (is_recommended, song_id))
        
        if success:
            return jsonify({"code": 200, "message": "更新成功"}), 200
        else:
            return jsonify({"code": 500, "error": "更新失败"}), 500
        
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500
