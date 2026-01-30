-- 收藏歌单表
CREATE TABLE IF NOT EXISTS favorite_playlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    playlist_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_playlist (user_id, playlist_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏的歌单';

-- 创建索引
CREATE INDEX idx_user_id ON favorite_playlists(user_id);
CREATE INDEX idx_playlist_id ON favorite_playlists(playlist_id);
CREATE INDEX idx_created_at ON favorite_playlists(created_at);
