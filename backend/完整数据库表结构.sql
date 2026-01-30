-- ========================================
-- YouxMusic 完整数据库表结构
-- ========================================

-- 使用数据库
USE youxmusic;

-- ========================================
-- 1. 用户表（如果已存在则跳过）
-- ========================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(120) NOT NULL UNIQUE COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '手机号（可选）',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ========================================
-- 2. 歌曲表（如果已存在则跳过）
-- ========================================
CREATE TABLE IF NOT EXISTS songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL COMMENT '歌曲名称',
    artist VARCHAR(200) NOT NULL COMMENT '歌手/艺术家',
    album VARCHAR(200) COMMENT '专辑名称',
    duration INT COMMENT '时长(秒)',
    file_path VARCHAR(500) NOT NULL COMMENT '音频文件路径',
    cover_image VARCHAR(500) COMMENT '封面图片路径',
    genre VARCHAR(100) COMMENT '音乐类型',
    release_year INT COMMENT '发行年份',
    play_count INT DEFAULT 0 COMMENT '播放次数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_title (title),
    INDEX idx_artist (artist),
    INDEX idx_genre (genre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='歌曲表';

-- ========================================
-- 3. 歌单表（新建）
-- ========================================
CREATE TABLE IF NOT EXISTS playlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '歌单名称',
    cover VARCHAR(500) COMMENT '封面图片路径',
    description TEXT COMMENT '歌单描述',
    user_id INT NOT NULL COMMENT '创建者ID',
    song_count INT DEFAULT 0 COMMENT '歌曲数量',
    play_count INT DEFAULT 0 COMMENT '播放次数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='歌单表';

-- ========================================
-- 4. 歌单-歌曲关联表（新建）
-- ========================================
CREATE TABLE IF NOT EXISTS playlist_songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_id INT NOT NULL COMMENT '歌单ID',
    song_id INT NOT NULL COMMENT '歌曲ID',
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
    position INT DEFAULT 0 COMMENT '歌曲在歌单中的位置',
    FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_playlist_song (playlist_id, song_id),
    INDEX idx_playlist_id (playlist_id),
    INDEX idx_song_id (song_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='歌单-歌曲关联表';

-- ========================================
-- 查看所有表
-- ========================================
SHOW TABLES;

-- ========================================
-- 查看表结构
-- ========================================
DESCRIBE users;
DESCRIBE songs;
DESCRIBE playlists;
DESCRIBE playlist_songs;

-- ========================================
-- 说明
-- ========================================
-- users: 存储用户信息
-- songs: 存储所有歌曲（音乐库）
-- playlists: 存储用户创建的歌单
-- playlist_songs: 记录歌单包含哪些歌曲（多对多关系）
