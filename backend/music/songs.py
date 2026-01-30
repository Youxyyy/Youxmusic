from flask import Blueprint, request, jsonify
from db import query_one, query_all, execute
import os

# 创建歌曲蓝图
songs_bp = Blueprint('songs', __name__)

# 配置：本地音乐文件存储路径
MUSIC_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'music_files')
COVER_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'covers')

# 确保文件夹存在
os.makedirs(MUSIC_FOLDER, exist_ok=True)
os.makedirs(COVER_FOLDER, exist_ok=True)


# 获取歌曲列表
@songs_bp.route('/list', methods=['GET'])
def get_songs():
    """获取歌曲列表（支持分页）- 首页推荐歌曲优先返回is_recommended=TRUE的歌曲"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # 优先获取管理员标记为推荐的歌曲
        songs = query_all(
            """SELECT id, title, artist, album, duration, file_path, cover_image, 
                      genre, release_year, play_count, is_recommended 
               FROM songs 
               WHERE is_recommended = TRUE
               ORDER BY id ASC 
               LIMIT %s OFFSET %s""",
            (per_page, offset)
        )
        
        # 如果推荐歌曲不足，补充其他歌曲
        if not songs or len(songs) < per_page:
            remaining = per_page - (len(songs) if songs else 0)
            additional_songs = query_all(
                """SELECT id, title, artist, album, duration, file_path, cover_image, 
                          genre, release_year, play_count, is_recommended 
                   FROM songs 
                   WHERE is_recommended = FALSE OR is_recommended IS NULL
                   ORDER BY id ASC 
                   LIMIT %s OFFSET %s""",
                (remaining, offset)
            )
            if additional_songs:
                songs = (songs or []) + additional_songs
        
        # 查询总数
        total_result = query_one("SELECT COUNT(*) as total FROM songs")
        total = total_result['total'] if total_result else 0
        
        return jsonify({
            "code": 200,
            "msg": "获取成功",
            "data": {
                "songs": songs if songs else [],
                "total": total,
                "page": page,
                "per_page": per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误: {str(e)}"}), 500


# 获取歌曲详情
@songs_bp.route('/<int:song_id>', methods=['GET'])
def get_song(song_id):
    """获取单个歌曲详情"""
    try:
        song = query_one(
            """SELECT id, title, artist, album, duration, file_path, 
                      cover_image, genre, release_year, play_count, created_at
               FROM songs 
               WHERE id = %s""",
            (song_id,)
        )
        
        if not song:
            return jsonify({"code": 404, "msg": "歌曲不存在"}), 404
        
        return jsonify({
            "code": 200,
            "msg": "获取成功",
            "data": song
        }), 200
        
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误: {str(e)}"}), 500


# 添加歌曲（管理员功能）
@songs_bp.route('/add', methods=['POST'])
def add_song():
    """添加新歌曲"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['title', 'artist', 'file_path']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"code": 400, "msg": f"缺少必填字段: {field}"}), 400
        
        # 插入歌曲
        success = execute(
            """INSERT INTO songs 
               (title, artist, album, duration, file_path, cover_image, genre, release_year) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                data.get('title'),
                data.get('artist'),
                data.get('album', ''),
                data.get('duration', 0),
                data.get('file_path'),
                data.get('cover_image', ''),
                data.get('genre', ''),
                data.get('release_year', None)
            )
        )
        
        if success:
            return jsonify({"code": 200, "msg": "添加成功"}), 201
        else:
            return jsonify({"code": 500, "msg": "添加失败"}), 500
            
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误: {str(e)}"}), 500


# 搜索歌曲
@songs_bp.route('/search', methods=['GET'])
def search_songs():
    """搜索歌曲"""
    try:
        keyword = request.args.get('keyword', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        if not keyword:
            return jsonify({"code": 400, "msg": "请输入搜索关键词"}), 400
        
        # 模糊搜索
        search_pattern = f"%{keyword}%"
        songs = query_all(
            """SELECT id, title, artist, album, duration, file_path, cover_image, 
                      genre, release_year, play_count 
               FROM songs 
               WHERE title LIKE %s OR artist LIKE %s OR album LIKE %s
               ORDER BY play_count DESC
               LIMIT %s OFFSET %s""",
            (search_pattern, search_pattern, search_pattern, per_page, offset)
        )
        
        # 查询匹配总数
        total_result = query_one(
            """SELECT COUNT(*) as total FROM songs 
               WHERE title LIKE %s OR artist LIKE %s OR album LIKE %s""",
            (search_pattern, search_pattern, search_pattern)
        )
        total = total_result['total'] if total_result else 0
        
        return jsonify({
            "code": 200,
            "msg": "搜索成功",
            "data": {
                "songs": songs,
                "total": total,
                "page": page,
                "per_page": per_page,
                "keyword": keyword
            }
        }), 200
        
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误: {str(e)}"}), 500


# 增加播放次数
@songs_bp.route('/<int:song_id>/play', methods=['POST'])
def increment_play_count(song_id):
    """增加歌曲播放次数"""
    try:
        success = execute(
            "UPDATE songs SET play_count = play_count + 1 WHERE id = %s",
            (song_id,)
        )
        
        if success:
            return jsonify({"code": 200, "msg": "播放次数已更新"}), 200
        else:
            return jsonify({"code": 500, "msg": "更新失败"}), 500
            
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误: {str(e)}"}), 500


# 获取热门歌曲
@songs_bp.route('/hot', methods=['GET'])
def get_hot_songs():
    """获取热门歌曲（大家都在听 - 根据is_featured标记）"""
    try:
        limit = int(request.args.get('limit', 10))
        
        # 优先获取管理员标记为推荐的歌曲
        songs = query_all(
            """SELECT id, title, artist, album, duration, file_path, cover_image, 
                      genre, play_count, is_featured 
               FROM songs 
               WHERE is_featured = TRUE
               ORDER BY play_count DESC 
               LIMIT %s""",
            (limit,)
        )
        
        # 如果推荐歌曲不足，补充播放量高的歌曲
        if not songs or len(songs) < limit:
            remaining = limit - (len(songs) if songs else 0)
            additional_songs = query_all(
                """SELECT id, title, artist, album, duration, file_path, cover_image, 
                          genre, play_count, is_featured 
                   FROM songs 
                   WHERE is_featured = FALSE OR is_featured IS NULL
                   ORDER BY play_count DESC 
                   LIMIT %s""",
                (remaining,)
            )
            if additional_songs:
                songs = (songs or []) + additional_songs
        
        return jsonify({
            "code": 200,
            "msg": "获取成功",
            "data": songs if songs else []
        }), 200
        
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误: {str(e)}"}), 500


# 获取最新歌曲
@songs_bp.route('/latest', methods=['GET'])
def get_latest_songs():
    """获取最新歌曲（根据is_new标记）"""
    try:
        limit = int(request.args.get('limit', 10))
        
        # 优先获取管理员标记为新歌的歌曲
        songs = query_all(
            """SELECT id, title, artist, album, duration, file_path, cover_image, 
                      genre, release_year, created_at, is_new 
               FROM songs 
               WHERE is_new = TRUE
               ORDER BY created_at DESC 
               LIMIT %s""",
            (limit,)
        )
        
        # 如果新歌不足，补充最近添加的歌曲
        if not songs or len(songs) < limit:
            remaining = limit - (len(songs) if songs else 0)
            additional_songs = query_all(
                """SELECT id, title, artist, album, duration, file_path, cover_image, 
                          genre, release_year, created_at, is_new 
                   FROM songs 
                   WHERE is_new = FALSE OR is_new IS NULL
                   ORDER BY created_at DESC 
                   LIMIT %s""",
                (remaining,)
            )
            if additional_songs:
                songs = (songs or []) + additional_songs
        
        return jsonify({
            "code": 200,
            "msg": "获取成功",
            "data": songs if songs else []
        }), 200
        
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误: {str(e)}"}), 500
