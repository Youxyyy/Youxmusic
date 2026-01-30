# 🎵 YouxMusic - 在线音乐平台

<div align="center">

![Vue](https://img.shields.io/badge/Vue-3.3.0-brightgreen.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

一个功能完整的全栈在线音乐播放平台

[功能特性](#-功能特性) | [快速开始](#-快速开始) | [技术栈](#️-技术栈) | [项目结构](#-项目结构) | [API文档](./API接口文档.md)

</div>

---

## 📖 项目简介

YouxMusic 是一个基于 **Vue 3 + Flask + MySQL** 开发的全栈在线音乐平台，提供完整的音乐播放、用户管理、歌单创建、收藏功能等核心特性。项目采用前后端分离架构，包含用户端和管理端两套完整系统。

### ✨ 项目亮点

- 🎯 **功能完整** - 涵盖音乐平台所有核心功能模块
- 🏗️ **架构清晰** - 前后端分离，模块化设计
- 🔐 **安全可靠** - JWT认证 + bcrypt密码加密
- 📱 **响应式设计** - 适配多种设备屏幕
- 🎨 **界面美观** - 现代化UI设计，流畅交互体验
- 📚 **文档齐全** - 详细的开发文档和API文档

---

## 🎯 功能特性

### 用户端功能

#### 🎵 音乐播放
- 在线播放音乐，支持播放/暂停/上一首/下一首
- 进度条拖拽、音量控制
- 播放模式切换（顺序/随机/单曲循环）
- 播放列表管理

#### 📁 歌单管理
- 创建个人歌单，自定义封面和描述
- 添加/移除歌曲到歌单
- 公开/私密歌单设置
- 收藏他人歌单

#### 👤 用户系统
- 用户注册/登录
- 个人信息管理
- 头像上传
- 自定义背景图片

#### ❤️ 收藏功能
- 收藏喜欢的歌曲
- 收藏优质歌单
- 收藏列表管理

#### 🎤 歌手功能
- 浏览歌手列表
- 按地区/首字母筛选
- 查看歌手详情和作品

#### 📊 排行榜
- 日榜/周榜/月榜
- 按音乐类型筛选
- 综合评分排名

#### 🔍 搜索功能
- 歌曲搜索
- 歌手搜索
- 歌单搜索

#### 📜 播放历史
- 自动记录播放历史
- 查看历史记录
- 清空历史功能

### 管理端功能

#### 📈 数据概览
- 歌曲/用户/歌手/歌单总数统计
- 总播放量和收藏数统计

#### 🎵 内容管理
- 歌曲上传、编辑、删除
- 歌手信息管理
- 歌单审核和推荐
- 首页内容配置

#### 👥 用户管理
- 查看所有用户
- 设置管理员权限
- 用户搜索和筛选

#### 🔒 权限控制
- 基于JWT的身份认证
- 管理员权限验证
- API接口权限控制

---

## 🛠️ 技术栈

### 前端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue 3 | 3.3.0 | 渐进式JavaScript框架 |
| Vue Router | 4.2.0 | 官方路由管理器 |
| Vite | 4.3.0 | 下一代前端构建工具 |
| Remix Icon | - | 开源图标库 |

### 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Flask | 2.3.3 | Python Web框架 |
| PyMySQL | 1.1.0 | MySQL数据库驱动 |
| Flask-CORS | 4.0.0 | 跨域资源共享 |
| bcrypt | 4.0.1 | 密码加密 |
| PyJWT | 2.8.0 | JWT认证 |

### 数据库

| 技术 | 版本 | 说明 |
|------|------|------|
| MySQL | 8.0+ | 关系型数据库 |

---

## 📂 项目结构

```
YouxMusic/
├── backend/                    # 后端代码
│   ├── music/                 # 业务模块
│   │   ├── __init__.py       # 蓝图注册
│   │   ├── auth.py           # 用户认证
│   │   ├── admin.py          # 管理员功能
│   │   ├── songs.py          # 歌曲管理
│   │   ├── singers.py        # 歌手管理
│   │   ├── playlist.py       # 歌单管理
│   │   ├── favorite.py       # 收藏功能
│   │   ├── history.py        # 播放历史
│   │   └── ranking.py        # 排行榜
│   ├── music_files/          # 音乐文件存储
│   ├── covers/               # 封面图片存储
│   ├── avatars/              # 用户头像存储
│   ├── backgrounds/          # 背景图片存储
│   ├── app.py                # Flask应用入口
│   ├── db.py                 # 数据库连接
│   ├── requirements.txt      # Python依赖
│   └── *.sql                 # 数据库脚本
├── src/                       # 前端代码
│   ├── views/                # 页面组件
│   │   ├── Home.vue         # 首页
│   │   ├── Songs.vue        # 歌曲列表
│   │   ├── Singer.vue       # 歌手列表
│   │   ├── SingerDetail.vue # 歌手详情
│   │   ├── PlaylistDetail.vue # 歌单详情
│   │   ├── Mine.vue         # 个人中心
│   │   ├── Favorite.vue     # 收藏页面
│   │   ├── History.vue      # 播放历史
│   │   ├── Rankinglist.vue  # 排行榜
│   │   ├── Admin.vue        # 管理后台
│   │   ├── Login.vue        # 登录
│   │   └── Register.vue     # 注册
│   ├── components/           # 公共组件
│   │   ├── Navigation.vue   # 导航栏
│   │   ├── MusicPlayer.vue  # 播放器
│   │   └── FavoriteButton.vue # 收藏按钮
│   ├── router/              # 路由配置
│   ├── utils/               # 工具函数
│   └── assets/             # 静态资源
├── public/                  # 公共资源
├── package.json            # 前端依赖
├── vite.config.js         # Vite配置
└── README.md              # 项目文档
```

---

## 🚀 快速开始

### 环境要求

- Node.js 16+
- Python 3.8+
- MySQL 8.0+

### 1. 克隆项目

```bash
git clone https://github.com/Youxyyy/YouxMusic.git
cd YouxMusic
```

### 2. 数据库配置

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE youxmusicdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入数据库表结构
mysql -u root -p youxmusicdb < backend/完整数据库表结构.sql
```

### 3. 后端配置

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置数据库连接
# 编辑 db.py 文件，修改数据库连接信息
```

**db.py 配置示例：**
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_password",  # 修改为你的密码
    "db": "youxmusicdb",
    "charset": "utf8mb4"
}
```

```bash
# 启动后端服务
python app.py
```

后端服务将运行在 `http://localhost:5000`

### 4. 前端配置

```bash
# 返回项目根目录
cd ..

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将运行在 `http://localhost:5173`

### 5. 访问应用

- **用户端首页**: http://localhost:5173
- **管理后台**: http://localhost:5173/admin
- **后端API**: http://localhost:5000/api

### 默认管理员账号

首次使用需要注册账号，然后在数据库中手动设置管理员权限：

```sql
UPDATE users SET is_admin = TRUE WHERE username = 'your_username';
```

---

## 📡 API文档

### 基础信息

- **Base URL**: `http://localhost:5000/api`
- **认证方式**: JWT Token (Bearer Token)
- **数据格式**: JSON

### 主要接口

#### 用户认证

```
POST   /api/auth/register      # 用户注册
POST   /api/auth/login         # 用户登录
GET    /api/auth/profile       # 获取用户信息
POST   /api/auth/upload-avatar # 上传头像
```

#### 歌曲管理

```
GET    /api/songs/list         # 获取歌曲列表
GET    /api/songs/:id          # 获取歌曲详情
GET    /api/songs/search       # 搜索歌曲
GET    /api/songs/hot          # 获取热门歌曲
POST   /api/songs/:id/play     # 增加播放次数
```

#### 歌单管理

```
GET    /api/playlist/public    # 获取公开歌单
GET    /api/playlist/my        # 获取我的歌单
POST   /api/playlist/create    # 创建歌单
GET    /api/playlist/:id       # 获取歌单详情
PUT    /api/playlist/:id       # 更新歌单
DELETE /api/playlist/:id       # 删除歌单
```

#### 收藏功能

```
GET    /api/favorite/songs     # 获取收藏的歌曲
POST   /api/favorite/songs     # 收藏歌曲
DELETE /api/favorite/songs/:id # 取消收藏歌曲
```

#### 管理员接口

```
GET    /api/admin/stats        # 获取统计信息
GET    /api/admin/songs        # 获取所有歌曲
POST   /api/admin/songs/upload # 上传歌曲
PUT    /api/admin/songs/:id    # 更新歌曲
DELETE /api/admin/songs/:id    # 删除歌曲
```

完整API文档请查看：[API接口文档.md](./API接口文档.md)

---

## 🗄️ 数据库设计

### 核心表结构

#### users (用户表)
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar VARCHAR(500),
    background_image VARCHAR(500),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### songs (歌曲表)
```sql
CREATE TABLE songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    artist VARCHAR(100) NOT NULL,
    album VARCHAR(100),
    duration INT,
    file_path VARCHAR(500) NOT NULL,
    cover_image VARCHAR(500),
    play_count INT DEFAULT 0,
    is_recommended BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    is_new BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### playlists (歌单表)
```sql
CREATE TABLE playlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    cover MEDIUMTEXT,
    description TEXT,
    user_id INT NOT NULL,
    is_public BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 关联表

- `song_singers` - 歌曲与歌手多对多关系
- `playlist_songs` - 歌单与歌曲多对多关系
- `favorite_songs` - 用户收藏歌曲
- `favorite_playlists` - 用户收藏歌单
- `play_history` - 播放历史记录

---

## 🔧 核心技术实现

### 1. JWT认证流程

```python
# 生成Token
def generate_token(user_id, username):
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# 验证Token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None
```

### 2. 密码加密

```python
import bcrypt

# 注册时加密
password_hash = bcrypt.hashpw(
    password.encode('utf-8'), 
    bcrypt.gensalt()
).decode('utf-8')

# 登录时验证
is_valid = bcrypt.checkpw(
    password.encode('utf-8'), 
    stored_hash.encode('utf-8')
)
```

### 3. 跨域处理

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有跨域请求
```

### 4. 文件上传

```python
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join('uploads', filename))
    return jsonify({"path": f"/uploads/{filename}"})
```

---

## 🎓 学习价值

这个项目适合：

- 🎯 **全栈开发学习** - 完整的前后端分离项目实践
- 📚 **毕业设计项目** - 功能完整，文档齐全
- 💼 **求职作品集** - 展示全栈开发能力
- 🚀 **二次开发基础** - 可扩展的架构设计

### 技能收获

**前端技能**
- Vue 3 Composition API
- 组件化开发
- 路由管理
- 状态管理
- API调用

**后端技能**
- Flask框架
- RESTful API设计
- 数据库设计
- JWT认证
- 文件上传

**全栈技能**
- 前后端分离架构
- 跨域处理
- 权限控制
- 数据流转
- 项目部署

---

## 📝 开发文档

- [API接口文档](./API接口文档.md) - 完整的API接口说明
- [部署指南](./部署指南.md) - 详细的部署步骤
- [项目技术分析](./📋项目技术分析-面试版.md) - 技术实现详解
- [数据库表说明](./backend/数据库表说明.md) - 数据库设计文档

---

## 🚀 部署

### 生产环境部署

#### 前端部署

```bash
# 构建生产版本
npm run build

# 使用Nginx部署
# 将dist目录内容复制到Nginx的html目录
```

#### 后端部署

```bash
# 使用Gunicorn运行Flask应用
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Nginx配置示例

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # 前端静态文件
    location / {
        root /var/www/youxmusic/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 静态资源
    location /music_files {
        proxy_pass http://localhost:5000;
    }
}
```

详细部署指南请查看：[部署指南.md](./部署指南.md)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 👨‍💻 作者

**Youx**

- Email: 2116157050@qq.com

---

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 发送邮件至2116157050@qq.com

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个Star！⭐**

Made with ❤️ by Youx

</div>
