from flask import Blueprint, request, jsonify
import jwt
from db import query_one, query_all, execute

favorite_bp = Blueprint('favorite', __name__)

# JWT配置
JWT_SECRET = 'your-secret-key-here'

def get_user_from_token():
    """从token获取用户ID"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload.get('user_id')
    except:
        return None

# 获取用户收藏的所有歌曲
@favorite_bp.route('/songs', methods=['GET'])
def get_favorite_songs():
    """获取我收藏的歌曲"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        songs = query_all(
            """SELECT s.*, f.created_at as favorite_time
               FROM songs s
               JOIN favorite_songs f ON s.id = f.song_id
               WHERE f.user_id = %s
               ORDER BY f.created_at DESC""",
            (user_id,)
        )
        
        return jsonify({
            "songs": songs if songs else [],
            "total": len(songs) if songs else 0
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取收藏歌曲错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 收藏歌曲
@favorite_bp.route('/songs/<int:song_id>', methods=['POST'])
def add_favorite_song(song_id):
    """收藏歌曲"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        # 检查歌曲是否存在
        song = query_one("SELECT id FROM songs WHERE id = %s", (song_id,))
        if not song:
            return jsonify({"error": "歌曲不存在"}), 404
        
        # 检查是否已收藏
        existing = query_one(
            "SELECT id FROM favorite_songs WHERE user_id = %s AND song_id = %s",
            (user_id, song_id)
        )
        if existing:
            return jsonify({"error": "已经收藏过了"}), 400
        
        # 添加收藏
        success = execute(
            "INSERT INTO favorite_songs (user_id, song_id) VALUES (%s, %s)",
            (user_id, song_id)
        )
        
        if success:
            return jsonify({"message": "收藏成功"}), 201
        else:
            return jsonify({"error": "收藏失败"}), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"收藏歌曲错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 取消收藏
@favorite_bp.route('/songs/<int:song_id>', methods=['DELETE'])
def remove_favorite_song(song_id):
    """取消收藏歌曲"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        # 检查是否已收藏
        existing = query_one(
            "SELECT id FROM favorite_songs WHERE user_id = %s AND song_id = %s",
            (user_id, song_id)
        )
        if not existing:
            return jsonify({"error": "还未收藏"}), 400
        
        # 取消收藏
        success = execute(
            "DELETE FROM favorite_songs WHERE user_id = %s AND song_id = %s",
            (user_id, song_id)
        )
        
        if success:
            return jsonify({"message": "取消收藏成功"}), 200
        else:
            return jsonify({"error": "取消收藏失败"}), 500
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 检查歌曲是否已收藏
@favorite_bp.route('/songs/<int:song_id>/check', methods=['GET'])
def check_favorite_song(song_id):
    """检查歌曲是否已收藏"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"is_favorite": False}), 200
    
    try:
        existing = query_one(
            "SELECT id FROM favorite_songs WHERE user_id = %s AND song_id = %s",
            (user_id, song_id)
        )
        
        return jsonify({"is_favorite": existing is not None}), 200
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 批量检查歌曲是否已收藏
@favorite_bp.route('/songs/check-batch', methods=['POST'])
def check_favorite_songs_batch():
    """批量检查歌曲是否已收藏"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"favorites": {}}), 200
    
    try:
        data = request.get_json()
        song_ids = data.get('song_ids', [])
        
        if not song_ids:
            return jsonify({"favorites": {}}), 200
        
        # 构建查询
        placeholders = ','.join(['%s'] * len(song_ids))
        query = f"""
            SELECT song_id 
            FROM favorite_songs 
            WHERE user_id = %s AND song_id IN ({placeholders})
        """
        params = [user_id] + song_ids
        
        favorites = query_all(query, tuple(params))
        favorite_ids = [f['song_id'] for f in favorites] if favorites else []
        
        # 构建返回结果
        result = {song_id: song_id in favorite_ids for song_id in song_ids}
        
        return jsonify({"favorites": result}), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"批量检查收藏错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500
