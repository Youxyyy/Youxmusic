from flask import Blueprint, request, jsonify
from db import query_all, query_one
from datetime import datetime, timedelta

ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/', methods=['GET'])
def get_ranking():
    """
    获取排行榜
    参数：
    - type: day|week|month (默认week)
    - genre: all|华语|欧美|日韩|民谣|摇滚|电子 (默认all)
    - limit: 返回数量 (默认50)
    """
    try:
        ranking_type = request.args.get('type', 'week')
        genre = request.args.get('genre', 'all')
        limit = request.args.get('limit', 50, type=int)
        
        # 计算时间范围
        now = datetime.now()
        if ranking_type == 'day':
            time_range = now - timedelta(days=1)
            time_label = '日榜'
        elif ranking_type == 'month':
            time_range = now - timedelta(days=30)
            time_label = '月榜'
        else:  # week
            time_range = now - timedelta(days=7)
            time_label = '周榜'
        
        # 构建查询条件
        genre_condition = ""
        params = []
        
        if genre != 'all':
            genre_condition = "AND s.genre LIKE %s"
            params.append(f"%{genre}%")
        
        # 排行算法：
        # 综合权重 = 播放量×0.6 + 收藏量×0.3 + 最近7天播放增量×0.1
        sql = f"""
            SELECT 
                s.id,
                s.title,
                s.artist,
                s.album,
                s.duration,
                s.file_path,
                s.cover_image,
                s.genre,
                s.release_year,
                s.play_count,
                COALESCE(fc.favorite_count, 0) as favorite_count,
                COALESCE(rc.recent_play_count, 0) as recent_play_count,
                (
                    s.play_count * 0.6 + 
                    COALESCE(fc.favorite_count, 0) * 0.3 + 
                    COALESCE(rc.recent_play_count, 0) * 0.1
                ) as score
            FROM songs s
            LEFT JOIN (
                SELECT song_id, COUNT(*) as favorite_count
                FROM favorite_songs
                GROUP BY song_id
            ) fc ON s.id = fc.song_id
            LEFT JOIN (
                SELECT song_id, COUNT(*) as recent_play_count
                FROM play_history
                WHERE played_at >= %s
                GROUP BY song_id
            ) rc ON s.id = rc.song_id
            WHERE 1=1 {genre_condition}
            ORDER BY score DESC, s.play_count DESC
            LIMIT %s
        """
        
        params.insert(0, time_range)
        params.append(limit)
        
        songs = query_all(sql, tuple(params))
        
        # 添加排名
        for index, song in enumerate(songs, 1):
            song['rank'] = index
            song['score'] = round(song['score'], 2)
        
        return jsonify({
            "code": 200,
            "data": {
                "type": ranking_type,
                "type_label": time_label,
                "genre": genre,
                "songs": songs if songs else [],
                "total": len(songs) if songs else 0,
                "updated_at": now.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 200
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"获取排行榜错误: {error_detail}")
        return jsonify({"code": 500, "error": str(e)}), 500

@ranking_bp.route('/genres', methods=['GET'])
def get_genres():
    """获取所有音乐流派"""
    try:
        genres = query_all("SELECT DISTINCT genre FROM songs WHERE genre IS NOT NULL ORDER BY genre")
        genre_list = ['all'] + [g['genre'] for g in genres] if genres else ['all']
        
        return jsonify({
            "code": 200,
            "data": genre_list
        }), 200
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500

@ranking_bp.route('/stats', methods=['GET'])
def get_ranking_stats():
    """获取排行榜统计信息"""
    try:
        # 总播放量
        total_plays = query_one("SELECT SUM(play_count) as total FROM songs")
        
        # 总收藏量
        total_favorites = query_one("SELECT COUNT(*) as total FROM favorite_songs")
        
        # 最近7天播放量
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_plays = query_one(
            "SELECT COUNT(*) as total FROM play_history WHERE played_at >= %s",
            (seven_days_ago,)
        )
        
        return jsonify({
            "code": 200,
            "data": {
                "total_plays": total_plays['total'] if total_plays else 0,
                "total_favorites": total_favorites['total'] if total_favorites else 0,
                "recent_plays": recent_plays['total'] if recent_plays else 0
            }
        }), 200
    except Exception as e:
        return jsonify({"code": 500, "error": str(e)}), 500
