from flask import Blueprint, request, jsonify
import jwt
from db import query_one, query_all, execute

playlist_bp = Blueprint('playlist', __name__)

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

# 获取用户的歌单列表
@playlist_bp.route('/my', methods=['GET'])
def get_my_playlists():
    """获取我的歌单"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        playlists = query_all(
            """SELECT p.*, u.username as creator
               FROM playlists p
               JOIN users u ON p.user_id = u.id
               WHERE p.user_id = %s
               ORDER BY p.created_at DESC""",
            (user_id,)
        )
        
        return jsonify({
            "playlists": playlists,
            "total": len(playlists)
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取歌单错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 创建歌单
@playlist_bp.route('/create', methods=['POST'])
def create_playlist():
    """创建歌单"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    data = request.get_json()
    name = data.get('name')
    cover = data.get('cover', '')
    description = data.get('description', '')
    
    if not name:
        return jsonify({"error": "歌单名称不能为空"}), 400
    
    try:
        print(f"尝试创建歌单: name={name}, user_id={user_id}, cover_length={len(cover) if cover else 0}")
        
        success = execute(
            "INSERT INTO playlists (name, cover, description, user_id) VALUES (%s, %s, %s, %s)",
            (name, cover, description, user_id)
        )
        
        print(f"执行结果: success={success}")
        
        if success:
            # 获取新创建的歌单
            playlist = query_one(
                "SELECT * FROM playlists WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                (user_id,)
            )
            return jsonify({
                "message": "创建成功",
                "playlist": playlist
            }), 201
        else:
            return jsonify({"error": "创建失败，请检查数据库连接"}), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"创建歌单错误: {error_detail}")
        return jsonify({"error": f"创建失败: {str(e)}"}), 500

# 获取歌单详情
@playlist_bp.route('/<int:playlist_id>', methods=['GET'])
def get_playlist_detail(playlist_id):
    """获取歌单详情"""
    try:
        # 获取歌单信息
        playlist = query_one(
            """SELECT p.*, u.username as creator
               FROM playlists p
               JOIN users u ON p.user_id = u.id
               WHERE p.id = %s""",
            (playlist_id,)
        )
        
        if not playlist:
            return jsonify({"error": "歌单不存在"}), 404
        
        # 获取歌单中的歌曲
        songs = query_all(
            """SELECT s.*, ps.added_at, ps.position
               FROM songs s
               JOIN playlist_songs ps ON s.id = ps.song_id
               WHERE ps.playlist_id = %s
               ORDER BY ps.position, ps.added_at""",
            (playlist_id,)
        )
        
        return jsonify({
            "playlist": playlist,
            "songs": songs if songs else []
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取歌单详情错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 更新歌单
@playlist_bp.route('/<int:playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    """更新歌单信息"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        # 检查歌单是否属于当前用户
        playlist = query_one(
            "SELECT user_id FROM playlists WHERE id = %s",
            (playlist_id,)
        )
        
        if not playlist:
            return jsonify({"error": "歌单不存在"}), 404
        
        if playlist['user_id'] != user_id:
            return jsonify({"error": "无权限操作"}), 403
        
        # 获取更新数据
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        cover = data.get('cover')
        
        # 构建更新SQL
        update_fields = []
        update_values = []
        
        if name is not None:
            update_fields.append("name = %s")
            update_values.append(name)
        
        if description is not None:
            update_fields.append("description = %s")
            update_values.append(description)
        
        if cover is not None:
            update_fields.append("cover = %s")
            update_values.append(cover)
        
        if not update_fields:
            return jsonify({"error": "没有要更新的字段"}), 400
        
        # 执行更新
        update_values.append(playlist_id)
        sql = f"UPDATE playlists SET {', '.join(update_fields)} WHERE id = %s"
        success = execute(sql, tuple(update_values))
        
        if success:
            # 获取更新后的歌单信息
            updated_playlist = query_one(
                """SELECT p.*, u.username as creator
                   FROM playlists p
                   JOIN users u ON p.user_id = u.id
                   WHERE p.id = %s""",
                (playlist_id,)
            )
            return jsonify({
                "message": "更新成功",
                "playlist": updated_playlist
            }), 200
        else:
            return jsonify({"error": "更新失败"}), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"更新歌单错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 删除歌单
@playlist_bp.route('/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    """删除歌单"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        # 检查歌单是否属于当前用户
        playlist = query_one(
            "SELECT user_id FROM playlists WHERE id = %s",
            (playlist_id,)
        )
        
        if not playlist:
            return jsonify({"error": "歌单不存在"}), 404
        
        if playlist['user_id'] != user_id:
            return jsonify({"error": "无权限操作"}), 403
        
        # 删除歌单（关联的歌曲会因为外键CASCADE自动删除）
        success = execute("DELETE FROM playlists WHERE id = %s", (playlist_id,))
        
        if success:
            return jsonify({"message": "删除成功"}), 200
        else:
            return jsonify({"error": "删除失败"}), 500
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 添加歌曲到歌单
@playlist_bp.route('/<int:playlist_id>/songs', methods=['POST'])
def add_song_to_playlist(playlist_id):
    """添加歌曲到歌单"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        data = request.get_json()
        song_id = data.get('song_id')
        
        if not song_id:
            return jsonify({"error": "歌曲ID不能为空"}), 400
        
        # 检查歌单是否属于当前用户
        playlist = query_one(
            "SELECT user_id FROM playlists WHERE id = %s",
            (playlist_id,)
        )
        
        if not playlist:
            return jsonify({"error": "歌单不存在"}), 404
        
        if playlist['user_id'] != user_id:
            return jsonify({"error": "无权限操作"}), 403
        
        # 检查歌曲是否存在
        song = query_one("SELECT id FROM songs WHERE id = %s", (song_id,))
        if not song:
            return jsonify({"error": "歌曲不存在"}), 404
        
        # 检查歌曲是否已在歌单中
        existing = query_one(
            "SELECT id FROM playlist_songs WHERE playlist_id = %s AND song_id = %s",
            (playlist_id, song_id)
        )
        if existing:
            return jsonify({"error": "歌曲已在歌单中"}), 400
        
        # 添加歌曲到歌单
        success = execute(
            "INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)",
            (playlist_id, song_id)
        )
        
        if success:
            # 更新歌单的歌曲数量
            execute(
                "UPDATE playlists SET song_count = (SELECT COUNT(*) FROM playlist_songs WHERE playlist_id = %s) WHERE id = %s",
                (playlist_id, playlist_id)
            )
            return jsonify({"message": "添加成功"}), 201
        else:
            return jsonify({"error": "添加失败"}), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"添加歌曲错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 从歌单移除歌曲
@playlist_bp.route('/<int:playlist_id>/songs/<int:song_id>', methods=['DELETE'])
def remove_song_from_playlist(playlist_id, song_id):
    """从歌单移除歌曲"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        # 检查歌单是否属于当前用户
        playlist = query_one(
            "SELECT user_id FROM playlists WHERE id = %s",
            (playlist_id,)
        )
        
        if not playlist:
            return jsonify({"error": "歌单不存在"}), 404
        
        if playlist['user_id'] != user_id:
            return jsonify({"error": "无权限操作"}), 403
        
        # 移除歌曲
        success = execute(
            "DELETE FROM playlist_songs WHERE playlist_id = %s AND song_id = %s",
            (playlist_id, song_id)
        )
        
        if success:
            # 更新歌单的歌曲数量
            execute(
                "UPDATE playlists SET song_count = (SELECT COUNT(*) FROM playlist_songs WHERE playlist_id = %s) WHERE id = %s",
                (playlist_id, playlist_id)
            )
            return jsonify({"message": "移除成功"}), 200
        else:
            return jsonify({"error": "移除失败"}), 500
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# ==================== 新增：公共歌单功能 ====================

# 获取公共歌单
@playlist_bp.route('/public', methods=['GET'])
def get_public_playlists():
    """获取公共歌单"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category', '')
        
        # 构建查询
        if category and category != '为你推荐':
            playlists = query_all(
                """SELECT p.*, u.username as creator,
                   (SELECT COUNT(*) FROM playlist_songs WHERE playlist_id = p.id) as song_count
                   FROM playlists p
                   JOIN users u ON p.user_id = u.id
                   WHERE p.is_public = TRUE AND p.category = %s
                   ORDER BY p.id ASC
                   LIMIT %s OFFSET %s""",
                (category, per_page, (page - 1) * per_page)
            )
        else:
            playlists = query_all(
                """SELECT p.*, u.username as creator,
                   (SELECT COUNT(*) FROM playlist_songs WHERE playlist_id = p.id) as song_count
                   FROM playlists p
                   JOIN users u ON p.user_id = u.id
                   WHERE p.is_public = TRUE
                   ORDER BY p.id ASC
                   LIMIT %s OFFSET %s""",
                (per_page, (page - 1) * per_page)
            )
        
        return jsonify({
            "code": 200,
            "data": playlists if playlists else [],
            "total": len(playlists) if playlists else 0
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取公共歌单错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

# 获取推荐歌单
@playlist_bp.route('/featured', methods=['GET'])
def get_featured_playlists():
    """获取推荐歌单"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        playlists = query_all(
            """SELECT p.*, u.username as creator,
               (SELECT COUNT(*) FROM playlist_songs WHERE playlist_id = p.id) as song_count
               FROM playlists p
               JOIN users u ON p.user_id = u.id
               WHERE p.is_public = TRUE AND p.is_featured = TRUE
               ORDER BY p.play_count DESC
               LIMIT %s""",
            (limit,)
        )
        
        return jsonify({
            "code": 200,
            "data": playlists if playlists else []
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取推荐歌单错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

# 增加播放次数
@playlist_bp.route('/<int:playlist_id>/play', methods=['POST'])
def increment_play_count(playlist_id):
    """增加歌单播放次数"""
    try:
        success = execute(
            "UPDATE playlists SET play_count = play_count + 1 WHERE id = %s",
            (playlist_id,)
        )
        if success:
            return jsonify({"code": 200, "message": "成功"}), 200
        else:
            return jsonify({"code": 500, "error": "更新失败"}), 500
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

# 更新歌单设置
@playlist_bp.route('/<int:playlist_id>/settings', methods=['PUT'])
def update_playlist_settings(playlist_id):
    """更新歌单设置（公开/私密、分类、首页推荐等）"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        data = request.get_json()
        is_public = data.get('is_public')
        category = data.get('category')
        is_featured = data.get('is_featured')
        
        # 检查歌单是否存在
        playlist = query_one(
            "SELECT * FROM playlists WHERE id = %s",
            (playlist_id,)
        )
        if not playlist:
            return jsonify({"error": "歌单不存在"}), 404
        
        # 检查权限：
        # 1. 歌单所有者可以修改 is_public 和 category
        # 2. 管理员可以修改所有字段（包括 is_featured）
        is_owner = playlist['user_id'] == user_id
        
        # 检查是否是管理员
        user = query_one("SELECT is_admin FROM users WHERE id = %s", (user_id,))
        is_admin = user and user.get('is_admin', False)
        
        if not is_owner and not is_admin:
            return jsonify({"error": "无权限"}), 403
        
        # 构建更新SQL
        update_fields = []
        update_values = []
        
        # 所有者和管理员都可以修改这些字段
        if is_public is not None:
            update_fields.append("is_public = %s")
            update_values.append(is_public)
        
        if category is not None:
            update_fields.append("category = %s")
            update_values.append(category)
        
        # 只有管理员可以修改 is_featured
        if is_featured is not None:
            if not is_admin:
                return jsonify({"error": "只有管理员可以设置首页推荐"}), 403
            update_fields.append("is_featured = %s")
            update_values.append(is_featured)
        
        if not update_fields:
            return jsonify({"error": "没有要更新的字段"}), 400
        
        # 执行更新
        update_values.append(playlist_id)
        sql = f"UPDATE playlists SET {', '.join(update_fields)} WHERE id = %s"
        success = execute(sql, tuple(update_values))
        
        if success:
            return jsonify({"code": 200, "message": "更新成功"}), 200
        else:
            return jsonify({"code": 500, "error": "更新失败"}), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"更新歌单设置错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500


# ==================== 收藏歌单功能 ====================

@playlist_bp.route('/<int:playlist_id>/collect', methods=['POST'])
def collect_playlist(playlist_id):
    """收藏歌单"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        # 检查歌单是否存在
        playlist = query_one("SELECT id FROM playlists WHERE id = %s", (playlist_id,))
        if not playlist:
            return jsonify({"error": "歌单不存在"}), 404
        
        # 检查是否已收藏
        existing = query_one(
            "SELECT id FROM favorite_playlists WHERE user_id = %s AND playlist_id = %s",
            (user_id, playlist_id)
        )
        
        if existing:
            return jsonify({"message": "已经收藏过了"}), 200
        
        # 添加收藏
        success = execute(
            "INSERT INTO favorite_playlists (user_id, playlist_id) VALUES (%s, %s)",
            (user_id, playlist_id)
        )
        
        if success:
            return jsonify({"message": "收藏成功"}), 201
        else:
            return jsonify({"error": "收藏失败"}), 500
            
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"收藏歌单错误: {error_detail}")
        return jsonify({"error": str(e)}), 500

@playlist_bp.route('/<int:playlist_id>/collect', methods=['DELETE'])
def uncollect_playlist(playlist_id):
    """取消收藏歌单"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        success = execute(
            "DELETE FROM favorite_playlists WHERE user_id = %s AND playlist_id = %s",
            (user_id, playlist_id)
        )
        
        if success:
            return jsonify({"message": "取消收藏成功"}), 200
        else:
            return jsonify({"error": "取消收藏失败"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@playlist_bp.route('/<int:playlist_id>/is-collected', methods=['GET'])
def check_playlist_collected(playlist_id):
    """检查歌单是否已收藏"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"is_collected": False}), 200
    
    try:
        result = query_one(
            "SELECT id FROM favorite_playlists WHERE user_id = %s AND playlist_id = %s",
            (user_id, playlist_id)
        )
        
        return jsonify({"is_collected": result is not None}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@playlist_bp.route('/collected', methods=['GET'])
def get_collected_playlists():
    """获取收藏的歌单"""
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "未登录"}), 401
    
    try:
        playlists = query_all("""
            SELECT p.*, u.username as creator,
                   (SELECT COUNT(*) FROM playlist_songs WHERE playlist_id = p.id) as song_count,
                   fp.created_at as collected_at
            FROM favorite_playlists fp
            JOIN playlists p ON fp.playlist_id = p.id
            JOIN users u ON p.user_id = u.id
            WHERE fp.user_id = %s
            ORDER BY fp.created_at DESC
        """, (user_id,))
        
        return jsonify({
            "playlists": playlists if playlists else [],
            "total": len(playlists) if playlists else 0
        }), 200
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取收藏歌单错误: {error_detail}")
        return jsonify({"error": str(e)}), 500
