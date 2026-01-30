-- 歌手表
CREATE TABLE IF NOT EXISTS singers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    avatar VARCHAR(255) DEFAULT NULL,
    country VARCHAR(50) DEFAULT '中国',
    genre VARCHAR(100) DEFAULT '流行',
    bio TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_country (country),
    INDEX idx_genre (genre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 歌曲歌手关联表
CREATE TABLE IF NOT EXISTS song_singers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    song_id INT NOT NULL,
    singer_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
    FOREIGN KEY (singer_id) REFERENCES singers(id) ON DELETE CASCADE,
    UNIQUE KEY unique_song_singer (song_id, singer_id),
    INDEX idx_song (song_id),
    INDEX idx_singer (singer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入测试歌手数据
-- 注意：需要在 backend/static/singers/ 目录下放置对应的图片文件
-- 如果图片不存在，前端会自动显示默认的🎤图标
INSERT INTO singers (name, avatar, country, genre, bio) VALUES
('周杰伦', '/static/singers/jay.jpg', '中国', '流行/R&B', '华语流行音乐天王，创作型歌手，擅长融合中国风与现代流行音乐。'),
('林俊杰', '/static/singers/jj.jpg', '新加坡', '流行', '华语流行音乐创作歌手，以细腻的情感表达和精湛的唱功著称。'),
('邓紫棋', '/static/singers/gem.jpg', '中国', '流行/R&B', '香港创作型女歌手，拥有独特的嗓音和强大的创作能力。'),
('薛之谦', '/static/singers/joker.jpg', '中国', '流行', '内地男歌手、音乐制作人，以幽默风趣的性格和深情的歌曲著称。'),
('Taylor Swift', '/static/singers/taylor.jpg', '美国', '流行/乡村', 'American singer-songwriter known for narrative songwriting and genre versatility.'),
('Ed Sheeran', '/static/singers/ed.jpg', '英国', '流行/民谣', 'British singer-songwriter known for acoustic pop and heartfelt lyrics.'),
('Adele', '/static/singers/adele.jpg', '英国', '流行/灵魂', 'British singer known for powerful vocals and emotional ballads.'),
('米津玄师', '/static/singers/yonezu.jpg', '日本', 'J-POP/摇滚', '日本创作型歌手，以独特的音乐风格和深刻的歌词著称。'),
('YOASOBI', '/static/singers/yoasobi.jpg', '日本', 'J-POP', '日本音乐组合，以将小说改编成歌曲的独特创作方式闻名。'),
('李荣浩', '/static/singers/ronghao.jpg', '中国', '流行/摇滚', '华语流行音乐创作歌手、音乐制作人，以简约风格和深情演唱著称。');

-- 为现有歌曲关联歌手（假设songs表已有数据）
-- 这里需要根据实际的song_id来关联，示例：
-- INSERT INTO song_singers (song_id, singer_id) VALUES (1, 1), (2, 2), (3, 3);
