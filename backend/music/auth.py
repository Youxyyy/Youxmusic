from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
from db import query_one, execute

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__)

# JWT配置
JWT_SECRET = 'your-secret-key-here'
JWT_ALGORITHM = 'HS256'


def generate_token(user_id, username):
    """生成JWT Token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token):
    """验证JWT Token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# 用户注册
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        phone = data.get('phone', '')

        # 验证输入
        if not username or not password or not email:
            return jsonify({"error": "用户名、邮箱和密码不能为空"}), 400

        if len(password) < 6:
            return jsonify({"error": "密码长度至少6位"}), 400

        # 检查用户名是否已存在
        existing_user = query_one("SELECT id FROM users WHERE username = %s", (username,))
        if existing_user:
            return jsonify({"error": "用户名已存在"}), 400

        # 检查邮箱是否已存在
        existing_email = query_one("SELECT id FROM users WHERE email = %s", (email,))
        if existing_email:
            return jsonify({"error": "邮箱已被注册"}), 400

        # 检查手机号是否已存在
        if phone:
            existing_phone = query_one("SELECT id FROM users WHERE phone = %s", (phone,))
            if existing_phone:
                return jsonify({"error": "手机号已被注册"}), 400

        # 加密密码
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 插入用户
        success = execute(
            "INSERT INTO users (username, password_hash, email, phone) VALUES (%s, %s, %s, %s)",
            (username, password_hash, email, phone)
        )

        if success:
            # 获取新创建的用户
            user = query_one("SELECT id, username, email, phone FROM users WHERE username = %s", (username,))
            return jsonify({
                "message": "注册成功",
                "user": {
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email'],
                    "phone": user['phone']
                }
            }), 201
        else:
            return jsonify({"error": "注册失败，请重试"}), 500

    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


# 用户登录
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        account = data.get('account')  # 支持用户名/邮箱/手机号登录
        password = data.get('password')

        if not account or not password:
            return jsonify({"error": "账号和密码不能为空"}), 400

        # 查询用户（支持用户名、邮箱、手机号登录）
        user = query_one(
            """SELECT id, username, password_hash, email, phone 
               FROM users 
               WHERE username = %s OR email = %s OR (phone IS NOT NULL AND phone = %s)""",
            (account, account, account)
        )

        if not user:
            return jsonify({"error": "账号或密码错误"}), 401

        # 验证密码
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            # 生成token
            token = generate_token(user['id'], user['username'])

            return jsonify({
                "message": "登录成功",
                "access_token": token,
                "user": {
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email'],
                    "phone": user['phone']
                }
            }), 200
        else:
            return jsonify({"error": "账号或密码错误"}), 401

    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


# 验证token
@auth_bp.route('/verify', methods=['POST'])
def verify():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')

    if not token:
        return jsonify({"code": 401, "msg": "未提供token"})

    payload = verify_token(token)
    if payload:
        return jsonify({
            "code": 200,
            "msg": "token有效",
            "data": payload
        })
    else:
        return jsonify({"code": 401, "msg": "token无效或已过期"})


# 上传头像
@auth_bp.route('/upload-avatar', methods=['POST'])
def upload_avatar():
    """上传用户头像"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({"error": "未登录"}), 401
    
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "token无效"}), 401
    
    user_id = payload.get('user_id')
    
    try:
        # 检查是否有文件
        if 'avatar' not in request.files:
            return jsonify({"error": "请上传头像文件"}), 400
        
        avatar_file = request.files['avatar']
        if avatar_file.filename == '':
            return jsonify({"error": "未选择文件"}), 400
        
        # 检查文件类型
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        if '.' not in avatar_file.filename or \
           avatar_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({"error": "不支持的图片格式"}), 400
        
        # 保存文件
        import os
        from werkzeug.utils import secure_filename
        
        filename = secure_filename(avatar_file.filename)
        # 使用用户ID作为文件名，避免重复
        ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"avatar_{user_id}.{ext}"
        
        avatar_folder = 'avatars'
        os.makedirs(avatar_folder, exist_ok=True)
        
        avatar_path = os.path.join(avatar_folder, new_filename)
        avatar_file.save(avatar_path)
        
        # 更新数据库
        avatar_url = f'/{avatar_path}'
        success = execute(
            "UPDATE users SET avatar = %s WHERE id = %s",
            (avatar_url, user_id)
        )
        
        if success:
            return jsonify({
                "message": "头像上传成功",
                "avatar": avatar_url
            }), 200
        else:
            return jsonify({"error": "更新失败"}), 500
            
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"上传头像错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


# 获取用户信息
@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """获取当前用户信息"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({"error": "未登录"}), 401
    
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "token无效"}), 401
    
    user_id = payload.get('user_id')
    
    try:
        user = query_one(
            "SELECT id, username, email, phone, avatar, background_image, background_type FROM users WHERE id = %s",
            (user_id,)
        )
        
        if user:
            return jsonify({"user": user}), 200
        else:
            return jsonify({"error": "用户不存在"}), 404
            
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500



# 更新背景设置
@auth_bp.route('/background', methods=['PUT'])
def update_background():
    """更新用户背景设置"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({"error": "未登录"}), 401
    
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "token无效"}), 401
    
    user_id = payload.get('user_id')
    
    try:
        data = request.get_json()
        background_type = data.get('background_type', 'default')
        background_image = data.get('background_image', None)
        
        # 验证背景类型
        if background_type not in ['default', 'preset', 'custom']:
            return jsonify({"error": "无效的背景类型"}), 400
        
        # 更新用户背景设置
        success = execute(
            "UPDATE users SET background_type = %s, background_image = %s WHERE id = %s",
            (background_type, background_image, user_id)
        )
        
        if success:
            return jsonify({
                "message": "背景设置更新成功",
                "background_type": background_type,
                "background_image": background_image
            }), 200
        else:
            return jsonify({"error": "更新失败"}), 500
            
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


# 上传自定义背景
@auth_bp.route('/background/upload', methods=['POST'])
def upload_background():
    """上传自定义背景图片"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({"error": "未登录"}), 401
    
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "token无效"}), 401
    
    user_id = payload.get('user_id')
    
    try:
        # 检查是否有文件
        if 'background' not in request.files:
            return jsonify({"error": "请上传背景图片"}), 400
        
        bg_file = request.files['background']
        if bg_file.filename == '':
            return jsonify({"error": "未选择文件"}), 400
        
        # 检查文件类型
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        if '.' not in bg_file.filename or \
           bg_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({"error": "不支持的图片格式"}), 400
        
        # 检查文件大小（限制5MB）
        bg_file.seek(0, 2)  # 移动到文件末尾
        file_size = bg_file.tell()
        bg_file.seek(0)  # 重置到文件开头
        
        if file_size > 5 * 1024 * 1024:  # 5MB
            return jsonify({"error": "图片大小不能超过5MB"}), 400
        
        # 保存文件
        import os
        from werkzeug.utils import secure_filename
        import time
        
        filename = secure_filename(bg_file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"bg_user_{user_id}_{int(time.time())}.{ext}"
        
        bg_folder = 'backgrounds'
        os.makedirs(bg_folder, exist_ok=True)
        
        bg_path = os.path.join(bg_folder, new_filename)
        bg_file.save(bg_path)
        
        # 更新数据库
        bg_url = f'/{bg_path.replace(os.sep, "/")}'
        success = execute(
            "UPDATE users SET background_type = 'custom', background_image = %s WHERE id = %s",
            (bg_url, user_id)
        )
        
        if success:
            return jsonify({
                "message": "背景上传成功",
                "background_url": bg_url
            }), 200
        else:
            return jsonify({"error": "更新失败"}), 500
            
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"上传背景错误: {error_detail}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500
