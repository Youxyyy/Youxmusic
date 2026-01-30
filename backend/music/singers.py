from flask import Blueprint, request, jsonify
import jwt
from db import query_one, query_all, execute
import os
from werkzeug.utils import secure_filename

singers_bp = Blueprint('singers', __name__)

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

def check_admin():
    """检查是否是管理员"""
    user_id = get_user_from_token()
    if not user_id:
        return False
    user = query_one("SELECT is_admin FROM users WHERE id = %s", (user_id,))
    return user and user.get('is_admin', False)

# ==================== 公共API ====================

@singers_bp.route('/list', methods=['GET'])
def get_singers():
    """获取歌手列表（支持分页、搜索、筛选）"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        keyword = request.args.get('keyword', '')
        country = request.args.get('country', '')
        genre = request.args.get('genre', '')
        letter = request.args.get('letter', '')  # 首字母筛选
        
        # 构建查询条件
        conditions = []
        params = []
        
        if keyword:
            conditions.append("name LIKE %s")
            params.append(f"%{keyword}%")
        
        if country:
            conditions.append("country = %s")
            params.append(country)
        
        if genre:
            conditions.append("genre LIKE %s")
            params.append(f"%{genre}%")
        
        if letter:
            conditions.append("name LIKE %s")
            params.append(f"{letter}%")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        # 获取总数
        count_sql = f"SELECT COUNT(*) as total FROM singers WHERE {where_clause}"
        total_result = query_one(count_sql, tuple(params))
        total = total_result['total'] if total_result else 0
        
        # 获取歌手列表
        offset = (page - 1) * per_page
        list_sql = f"""
            SELECT s.*, 
                   (SELECT COUNT(*) FROM song_singers WHERE singer_id = s.id) as song_count
            FROM singers s
            WHERE {where_clause}
            ORDER BY s.name
            LIMIT %s OFFSET %s
        """
        params.extend([per_page, offset])
        singers = query_all(list_sql, tuple(params))
        
        return jsonify({
            "code": 200,
            "data": {
                "singers": singers if singers else [],
                "total": total,
                "page": page,
                "per_page": per_page
            }
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取歌手列表错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

@singers_bp.route('/<int:singer_id>', methods=['GET'])
def get_singer_detail(singer_id):
    """获取歌手详情"""
    try:
        # 获取歌手信息
        singer = query_one(
            """SELECT s.*,
                      (SELECT COUNT(*) FROM song_singers WHERE singer_id = s.id) as song_count
               FROM singers s
               WHERE s.id = %s""",
            (singer_id,)
        )
        
        if not singer:
            return jsonify({"code": 404, "error": "歌手不存在"}), 404
        
        return jsonify({
            "code": 200,
            "data": singer
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取歌手详情错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

@singers_bp.route('/<int:singer_id>/songs', methods=['GET'])
def get_singer_songs(singer_id):
    """获取歌手的所有歌曲"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # 检查歌手是否存在
        singer = query_one("SELECT * FROM singers WHERE id = %s", (singer_id,))
        if not singer:
            return jsonify({"code": 404, "error": "歌手不存在"}), 404
        
        # 获取总数
        count_sql = """
            SELECT COUNT(*) as total
            FROM songs s
            INNER JOIN song_singers ss ON s.id = ss.song_id
            WHERE ss.singer_id = %s
        """
        total_result = query_one(count_sql, (singer_id,))
        total = total_result['total'] if total_result else 0
        
        # 获取歌曲列表
        offset = (page - 1) * per_page
        songs_sql = """
            SELECT s.*
            FROM songs s
            INNER JOIN song_singers ss ON s.id = ss.song_id
            WHERE ss.singer_id = %s
            ORDER BY s.created_at DESC
            LIMIT %s OFFSET %s
        """
        songs = query_all(songs_sql, (singer_id, per_page, offset))
        
        return jsonify({
            "code": 200,
            "data": {
                "singer": singer,
                "songs": songs if songs else [],
                "total": total,
                "page": page,
                "per_page": per_page
            }
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取歌手歌曲错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

@singers_bp.route('/countries', methods=['GET'])
def get_countries():
    """获取所有国家/地区列表"""
    try:
        countries = query_all("SELECT DISTINCT country FROM singers ORDER BY country")
        country_list = [c['country'] for c in countries] if countries else []
        return jsonify({
            "code": 200,
            "data": country_list
        }), 200
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

@singers_bp.route('/genres', methods=['GET'])
def get_genres():
    """获取所有流派列表"""
    try:
        genres = query_all("SELECT DISTINCT genre FROM singers ORDER BY genre")
        genre_list = [g['genre'] for g in genres] if genres else []
        return jsonify({
            "code": 200,
            "data": genre_list
        }), 200
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

# ==================== 管理员API ====================

@singers_bp.route('/create', methods=['POST'])
def create_singer():
    """创建歌手（管理员）"""
    if not check_admin():
        return jsonify({"code": 403, "error": "需要管理员权限"}), 403
    
    try:
        data = request.get_json()
        name = data.get('name')
        avatar = data.get('avatar', '')
        country = data.get('country', '中国')
        genre = data.get('genre', '流行')
        bio = data.get('bio', '')
        
        if not name:
            return jsonify({"code": 400, "error": "歌手名称不能为空"}), 400
        
        # 检查歌手是否已存在
        existing = query_one("SELECT id FROM singers WHERE name = %s", (name,))
        if existing:
            return jsonify({"code": 400, "error": "歌手已存在"}), 400
        
        # 创建歌手
        success = execute(
            "INSERT INTO singers (name, avatar, country, genre, bio) VALUES (%s, %s, %s, %s, %s)",
            (name, avatar, country, genre, bio)
        )
        
        if success:
            singer = query_one(
                "SELECT * FROM singers WHERE name = %s ORDER BY id DESC LIMIT 1",
                (name,)
            )
            return jsonify({
                "code": 200,
                "message": "创建成功",
                "data": singer
            }), 201
        else:
            return jsonify({"code": 500, "error": "创建失败"}), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"创建歌手错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

@singers_bp.route('/<int:singer_id>', methods=['PUT'])
def update_singer(singer_id):
    """更新歌手信息（管理员）"""
    if not check_admin():
        return jsonify({"code": 403, "error": "需要管理员权限"}), 403
    
    try:
        data = request.get_json()
        
        # 检查歌手是否存在
        singer = query_one("SELECT * FROM singers WHERE id = %s", (singer_id,))
        if not singer:
            return jsonify({"code": 404, "error": "歌手不存在"}), 404
        
        # 构建更新SQL
        update_fields = []
        update_values = []
        
        if 'name' in data:
            update_fields.append("name = %s")
            update_values.append(data['name'])
        
        if 'avatar' in data:
            update_fields.append("avatar = %s")
            update_values.append(data['avatar'])
        
        if 'country' in data:
            update_fields.append("country = %s")
            update_values.append(data['country'])
        
        if 'genre' in data:
            update_fields.append("genre = %s")
            update_values.append(data['genre'])
        
        if 'bio' in data:
            update_fields.append("bio = %s")
            update_values.append(data['bio'])
        
        if not update_fields:
            return jsonify({"code": 400, "error": "没有要更新的字段"}), 400
        
        # 执行更新
        update_values.append(singer_id)
        sql = f"UPDATE singers SET {', '.join(update_fields)} WHERE id = %s"
        success = execute(sql, tuple(update_values))
        
        if success:
            updated_singer = query_one("SELECT * FROM singers WHERE id = %s", (singer_id,))
            return jsonify({
                "code": 200,
                "message": "更新成功",
                "data": updated_singer
            }), 200
        else:
            return jsonify({"code": 500, "error": "更新失败"}), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"更新歌手错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

@singers_bp.route('/<int:singer_id>', methods=['DELETE'])
def delete_singer(singer_id):
    """删除歌手（管理员）"""
    if not check_admin():
        return jsonify({"code": 403, "error": "需要管理员权限"}), 403
    
    try:
        # 检查歌手是否存在
        singer = query_one("SELECT * FROM singers WHERE id = %s", (singer_id,))
        if not singer:
            return jsonify({"code": 404, "error": "歌手不存在"}), 404
        
        # 删除歌手（关联的song_singers会因为外键CASCADE自动删除）
        success = execute("DELETE FROM singers WHERE id = %s", (singer_id,))
        
        if success:
            return jsonify({
                "code": 200,
                "message": "删除成功"
            }), 200
        else:
            return jsonify({"code": 500, "error": "删除失败"}), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"删除歌手错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

@singers_bp.route('/upload-avatar', methods=['POST'])
def upload_singer_avatar():
    """上传歌手头像（管理员）"""
    if not check_admin():
        return jsonify({"code": 403, "error": "需要管理员权限"}), 403
    
    try:
        if 'avatar' not in request.files:
            return jsonify({"code": 400, "error": "没有上传文件"}), 400
        
        file = request.files['avatar']
        if file.filename == '':
            return jsonify({"code": 400, "error": "没有选择文件"}), 400
        
        # 检查文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({"code": 400, "error": "不支持的文件类型"}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'static', 'singers')
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # 返回文件路径
        file_url = f'/static/singers/{filename}'
        return jsonify({
            "code": 200,
            "message": "上传成功",
            "data": {"url": file_url}
        }), 200
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"上传头像错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

# ==================== 歌曲-歌手关联API ====================

@singers_bp.route('/link-song', methods=['POST'])
def link_song_singer():
    """关联歌曲和歌手（管理员）"""
    if not check_admin():
        return jsonify({"code": 403, "error": "需要管理员权限"}), 403
    
    try:
        data = request.get_json()
        song_id = data.get('song_id')
        singer_id = data.get('singer_id')
        
        if not song_id or not singer_id:
            return jsonify({"code": 400, "error": "歌曲ID和歌手ID不能为空"}), 400
        
        # 检查是否已关联
        existing = query_one(
            "SELECT id FROM song_singers WHERE song_id = %s AND singer_id = %s",
            (song_id, singer_id)
        )
        if existing:
            return jsonify({"code": 400, "error": "已经关联过了"}), 400
        
        # 创建关联
        success = execute(
            "INSERT INTO song_singers (song_id, singer_id) VALUES (%s, %s)",
            (song_id, singer_id)
        )
        
        if success:
            return jsonify({
                "code": 200,
                "message": "关联成功"
            }), 201
        else:
            return jsonify({"code": 500, "error": "关联失败"}), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"关联歌曲歌手错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

@singers_bp.route('/unlink-song', methods=['POST'])
def unlink_song_singer():
    """取消歌曲和歌手的关联（管理员）"""
    if not check_admin():
        return jsonify({"code": 403, "error": "需要管理员权限"}), 403
    
    try:
        data = request.get_json()
        song_id = data.get('song_id')
        singer_id = data.get('singer_id')
        
        if not song_id or not singer_id:
            return jsonify({"code": 400, "error": "歌曲ID和歌手ID不能为空"}), 400
        
        # 删除关联
        success = execute(
            "DELETE FROM song_singers WHERE song_id = %s AND singer_id = %s",
            (song_id, singer_id)
        )
        
        if success:
            return jsonify({
                "code": 200,
                "message": "取消关联成功"
            }), 200
        else:
            return jsonify({"code": 500, "error": "取消关联失败"}), 500
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

@singers_bp.route('/song/<int:song_id>/singers', methods=['GET'])
def get_song_singers(song_id):
    """获取歌曲的所有歌手"""
    try:
        singers = query_all(
            """SELECT s.*
               FROM singers s
               INNER JOIN song_singers ss ON s.id = ss.singer_id
               WHERE ss.song_id = %s
               ORDER BY ss.id""",
            (song_id,)
        )
        
        return jsonify({
            "code": 200,
            "data": singers if singers else []
        }), 200
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500
