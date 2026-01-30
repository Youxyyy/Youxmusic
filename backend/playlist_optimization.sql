-- 歌单功能优化 SQL
-- 执行时间：2025年11月19日

-- 1. 检查并添加字段（如果字段已存在会报错，可以忽略）
-- 添加 is_public 字段
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'playlists' 
AND COLUMN_NAME = 'is_public';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE playlists ADD COLUMN is_public BOOLEAN DEFAULT TRUE COMMENT ''是否公开''',
    'SELECT ''Column is_public already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加 category 字段
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'playlists' 
AND COLUMN_NAME = 'category';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE playlists ADD COLUMN category VARCHAR(50) DEFAULT ''为你推荐'' COMMENT ''分类''',
    'SELECT ''Column category already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加 play_count 字段
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'playlists' 
AND COLUMN_NAME = 'play_count';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE playlists ADD COLUMN play_count INT DEFAULT 0 COMMENT ''播放次数''',
    'SELECT ''Column play_count already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加 is_featured 字段
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'playlists' 
AND COLUMN_NAME = 'is_featured';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE playlists ADD COLUMN is_featured BOOLEAN DEFAULT FALSE COMMENT ''是否推荐''',
    'SELECT ''Column is_featured already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加 tags 字段
SET @col_exists = 0;
SELECT COUNT(*) INTO @col_exists 
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'playlists' 
AND COLUMN_NAME = 'tags';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE playlists ADD COLUMN tags VARCHAR(255) DEFAULT '''' COMMENT ''标签（逗号分隔）''',
    'SELECT ''Column tags already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 2. 添加索引（如果索引已存在会报错，可以忽略）
-- 添加 is_public 索引
SET @index_exists = 0;
SELECT COUNT(*) INTO @index_exists 
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'playlists' 
AND INDEX_NAME = 'idx_is_public';

SET @sql = IF(@index_exists = 0, 
    'CREATE INDEX idx_is_public ON playlists(is_public)',
    'SELECT ''Index idx_is_public already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加 category 索引
SET @index_exists = 0;
SELECT COUNT(*) INTO @index_exists 
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'playlists' 
AND INDEX_NAME = 'idx_category';

SET @sql = IF(@index_exists = 0, 
    'CREATE INDEX idx_category ON playlists(category)',
    'SELECT ''Index idx_category already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加 is_featured 索引
SET @index_exists = 0;
SELECT COUNT(*) INTO @index_exists 
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'playlists' 
AND INDEX_NAME = 'idx_is_featured';

SET @sql = IF(@index_exists = 0, 
    'CREATE INDEX idx_is_featured ON playlists(is_featured)',
    'SELECT ''Index idx_is_featured already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加 play_count 索引
SET @index_exists = 0;
SELECT COUNT(*) INTO @index_exists 
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME = 'playlists' 
AND INDEX_NAME = 'idx_play_count';

SET @sql = IF(@index_exists = 0, 
    'CREATE INDEX idx_play_count ON playlists(play_count)',
    'SELECT ''Index idx_play_count already exists'' AS message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 3. 更新现有歌单为公开状态
UPDATE playlists SET is_public = TRUE WHERE is_public IS NULL;

-- 4. 插入官方推荐歌单（如果不存在）
-- 注意：需要先确保有管理员用户（user_id = 1）

-- 检查是否已有推荐歌单
INSERT INTO playlists (name, description, cover_image, user_id, is_public, category, is_featured, play_count)
SELECT * FROM (
    SELECT 
        '在安静的位置看热闹的世界' as name,
        '人生最好的境界是丰富的安静' as description,
        '/covers/daitu1.jpg' as cover_image,
        1 as user_id,
        TRUE as is_public,
        '为你推荐' as category,
        TRUE as is_featured,
        1087000 as play_count
) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM playlists WHERE name = '在安静的位置看热闹的世界'
);

INSERT INTO playlists (name, description, cover_image, user_id, is_public, category, is_featured, play_count)
SELECT * FROM (
    SELECT 
        '抬头，已是一片星海' as name,
        '我总会把一首好歌形容成一片浩瀚的夜空' as description,
        '/covers/zuozhu2.jpg' as cover_image,
        1 as user_id,
        TRUE as is_public,
        '为你推荐' as category,
        TRUE as is_featured,
        20923000 as play_count
) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM playlists WHERE name = '抬头，已是一片星海'
);

INSERT INTO playlists (name, description, cover_image, user_id, is_public, category, is_featured, play_count)
SELECT * FROM (
    SELECT 
        '心跳和鼓点是同一个频率' as name,
        '年轻人的情感总让人难以捉摸' as description,
        '/covers/mingren1.jpg' as cover_image,
        1 as user_id,
        TRUE as is_public,
        '情歌' as category,
        TRUE as is_featured,
        1859000 as play_count
) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM playlists WHERE name = '心跳和鼓点是同一个频率'
);

INSERT INTO playlists (name, description, cover_image, user_id, is_public, category, is_featured, play_count)
SELECT * FROM (
    SELECT 
        '把风与爱意都藏进歌单' as name,
        '是踩碎落叶的沙沙声' as description,
        '/covers/you1.jpg' as cover_image,
        1 as user_id,
        TRUE as is_public,
        '情歌' as category,
        TRUE as is_featured,
        35481000 as play_count
) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM playlists WHERE name = '把风与爱意都藏进歌单'
);

INSERT INTO playlists (name, description, cover_image, user_id, is_public, category, is_featured, play_count)
SELECT * FROM (
    SELECT 
        '浪漫chill氛围 爵士蓝调布鲁斯' as name,
        '感受音乐带来的浪漫和惬意' as description,
        '/covers/kakaxi1.jpg' as cover_image,
        1 as user_id,
        TRUE as is_public,
        '经典' as category,
        TRUE as is_featured,
        558000 as play_count
) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM playlists WHERE name = '浪漫chill氛围 爵士蓝调布鲁斯'
);

INSERT INTO playlists (name, description, cover_image, user_id, is_public, category, is_featured, play_count)
SELECT * FROM (
    SELECT 
        '海风潮湿微咸 记忆带着海水味道' as name,
        '海浪轻吻礁石' as description,
        '/covers/feijian1.jpg' as cover_image,
        1 as user_id,
        TRUE as is_public,
        '经典' as category,
        FALSE as is_featured,
        892000 as play_count
) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM playlists WHERE name = '海风潮湿微咸 记忆带着海水味道'
);

INSERT INTO playlists (name, description, cover_image, user_id, is_public, category, is_featured, play_count)
SELECT * FROM (
    SELECT 
        '我听见了宇宙的呼吸' as name,
        '和心跳同频' as description,
        '/covers/ban1.jpg' as cover_image,
        1 as user_id,
        TRUE as is_public,
        '网络歌曲' as category,
        FALSE as is_featured,
        892000 as play_count
) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM playlists WHERE name = '我听见了宇宙的呼吸'
);

INSERT INTO playlists (name, description, cover_image, user_id, is_public, category, is_featured, play_count)
SELECT * FROM (
    SELECT 
        '享受宁静与和谐之美' as name,
        '一望无际的海' as description,
        '/covers/zuozhu1.jpg' as cover_image,
        1 as user_id,
        TRUE as is_public,
        '官方歌单' as category,
        FALSE as is_featured,
        892000 as play_count
) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM playlists WHERE name = '享受宁静与和谐之美'
);

INSERT INTO playlists (name, description, cover_image, user_id, is_public, category, is_featured, play_count)
SELECT * FROM (
    SELECT 
        '梦与花火怒放的桀骜篇章' as name,
        '把节奏揉进晚风里' as description,
        '/covers/chutian1.jpg' as cover_image,
        1 as user_id,
        TRUE as is_public,
        '经典' as category,
        FALSE as is_featured,
        892000 as play_count
) AS tmp
WHERE NOT EXISTS (
    SELECT 1 FROM playlists WHERE name = '梦与花火怒放的桀骜篇章'
);

-- 5. 验证数据
SELECT 
    id, 
    name, 
    category, 
    is_public, 
    is_featured, 
    play_count 
FROM playlists 
ORDER BY is_featured DESC, play_count DESC;
