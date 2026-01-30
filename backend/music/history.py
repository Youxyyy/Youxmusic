from flask import Blueprint, request, jsonify
import jwt
from db import query_one, query_all, execute

history_bp = Blueprint('history', __name__)

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

# 记录播放历史
@history_bp.route('/record', methods=['POST'])
def record_play():
    """记录播放历史"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    data = request.get_json()
    song_id = data.get('song_id')
    
    if not song_id:
        return jsonify({"error": "歌曲ID不能为空"}), 400
    
    try:
        # 检查歌曲是否存在
        song = query_one("SELECT id FROM songs WHERE id = %s", (song_id,))
        if not song:
            return jsonify({"error": "歌曲不存在"}), 404
        
        # 记录播放历史
        success = execute(
            "INSERT INTO play_history (user_id, song_id) VALUES (%s, %s)",
            (user_id, song_id)
        )
        
        if success:
            return jsonify({"message": "记录成功"}), 201
        else:
            return jsonify({"error": "记录失败"}), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"记录播放历史错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 获取播放历史
@history_bp.route('/list', methods=['GET'])
def get_play_history():
    """获取播放历史"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        # 获取分页参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # 获取播放历史（去重，只显示最近一次播放）
        history = query_all(
            """SELECT s.*, MAX(h.played_at) as last_played
               FROM play_history h
               JOIN songs s ON h.song_id = s.id
               WHERE h.user_id = %s
               GROUP BY s.id
               ORDER BY last_played DESC
               LIMIT %s OFFSET %s""",
            (user_id, per_page, offset)
        )
        
        # 获取总数
        total_result = query_one(
            """SELECT COUNT(DISTINCT song_id) as total
               FROM play_history
               WHERE user_id = %s""",
            (user_id,)
        )
        total = total_result['total'] if total_result else 0
        
        return jsonify({
            "history": history,
            "total": total,
            "page": page,
            "per_page": per_page
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取播放历史错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 获取最近播放（限制数量）
@history_bp.route('/recent', methods=['GET'])
def get_recent_plays():
    """获取最近播放"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        limit = int(request.args.get('limit', 10))
        
        # 获取最近播放（去重）
        recent = query_all(
            """SELECT s.*, MAX(h.played_at) as last_played
               FROM play_history h
               JOIN songs s ON h.song_id = s.id
               WHERE h.user_id = %s
               GROUP BY s.id
               ORDER BY last_played DESC
               LIMIT %s""",
            (user_id, limit)
        )
        
        return jsonify({
            "songs": recent,
            "total": len(recent)
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取最近播放错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 清空播放历史
@history_bp.route('/clear', methods=['DELETE'])
def clear_history():
    """清空播放历史"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        success = execute(
            "DELETE FROM play_history WHERE user_id = %s",
            (user_id,)
        )
        
        if success:
            return jsonify({"message": "清空成功"}), 200
        else:
            return jsonify({"error": "清空失败"}), 500
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 删除单条播放历史
@history_bp.route('/<int:song_id>', methods=['DELETE'])
def delete_history_item(song_id):
    """删除单条播放历史"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        success = execute(
            "DELETE FROM play_history WHERE user_id = %s AND song_id = %s",
            (user_id, song_id)
        )
        
        if success:
            return jsonify({"message": "删除成功"}), 200
        else:
            return jsonify({"error": "删除失败"}), 500
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500
