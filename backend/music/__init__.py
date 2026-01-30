from flask import Blueprint
from .auth import auth_bp
from .songs import songs_bp
from .playlist import playlist_bp
from .favorite import favorite_bp
from .admin import admin_bp
from .history import history_bp
from .singers import singers_bp
from .ranking import ranking_bp

# 创建主蓝图
music_bp = Blueprint('music', __name__)

# 注册子蓝图
music_bp.register_blueprint(auth_bp, url_prefix='/auth')
music_bp.register_blueprint(songs_bp, url_prefix='/songs')
music_bp.register_blueprint(playlist_bp, url_prefix='/playlist')
music_bp.register_blueprint(favorite_bp, url_prefix='/favorite')
music_bp.register_blueprint(admin_bp, url_prefix='/admin')
music_bp.register_blueprint(history_bp, url_prefix='/history')
music_bp.register_blueprint(singers_bp, url_prefix='/singers')
music_bp.register_blueprint(ranking_bp, url_prefix='/ranking')