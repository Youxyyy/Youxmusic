-- 收藏歌曲表
USE youxmusic;

CREATE TABLE IF NOT EXISTS favorite_songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    song_id INT NOT NULL COMMENT '歌曲ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_song (user_id, song_id),
    INDEX idx_user_id (user_id),
    INDEX idx_song_id (song_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏歌曲表';

-- 查看表结构
DESCRIBE favorite_songs;

-- 示例查询：获取用户收藏的所有歌曲
-- SELECT s.*, f.created_at as favorite_time
-- FROM songs s
-- JOIN favorite_songs f ON s.id = f.song_id
-- WHERE f.user_id = 1
-- ORDER BY f.created_at DESC;
