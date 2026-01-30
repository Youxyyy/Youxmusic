-- 快速关联歌曲到歌手 SQL脚本
-- 使用方法：mysql -u root -p youxmusicdb < 快速关联歌曲到歌手.sql

-- ==================== 方法1：查看未关联的歌曲 ====================

SELECT '=== 未关联的歌曲 ===' AS 提示;

SELECT 
    s.id AS 歌曲ID, 
    s.title AS 歌曲名, 
    s.artist AS 歌手名
FROM songs s
LEFT JOIN song_singers ss ON s.id = ss.song_id
WHERE ss.song_id IS NULL
ORDER BY s.id DESC;

-- ==================== 方法2：自动关联（根据artist字段匹配） ====================

SELECT '=== 开始自动关联 ===' AS 提示;

-- 自动关联：根据songs.artist匹配singers.name
INSERT IGNORE INTO song_singers (song_id, singer_id)
SELECT s.id, sg.id
FROM songs s
INNER JOIN singers sg ON s.artist = sg.name
LEFT JOIN song_singers ss ON s.id = ss.song_id AND ss.singer_id = sg.id
WHERE ss.song_id IS NULL;

SELECT '=== 自动关联完成 ===' AS 提示;

-- ==================== 方法3：查看关联结果 ====================

SELECT '=== 关联统计 ===' AS 提示;

SELECT 
    '已关联歌曲数' AS 类型,
    COUNT(DISTINCT song_id) AS 数量
FROM song_singers
UNION ALL
SELECT 
    '未关联歌曲数' AS 类型,
    COUNT(*) AS 数量
FROM songs s
LEFT JOIN song_singers ss ON s.id = ss.song_id
WHERE ss.song_id IS NULL;

-- ==================== 方法4：查看每个歌手的歌曲数 ====================

SELECT '=== 歌手歌曲统计 ===' AS 提示;

SELECT 
    sg.id AS 歌手ID,
    sg.name AS 歌手名,
    COUNT(ss.song_id) AS 歌曲数
FROM singers sg
LEFT JOIN song_singers ss ON sg.id = ss.singer_id
GROUP BY sg.id, sg.name
ORDER BY 歌曲数 DESC;

-- ==================== 方法5：仍然未关联的歌曲（需要手动处理） ====================

SELECT '=== 仍需手动关联的歌曲 ===' AS 提示;

SELECT 
    s.id AS 歌曲ID, 
    s.title AS 歌曲名, 
    s.artist AS 歌手名,
    '歌手不存在或名称不匹配' AS 原因
FROM songs s
LEFT JOIN song_singers ss ON s.id = ss.song_id
WHERE ss.song_id IS NULL
ORDER BY s.id DESC;

-- ==================== 使用说明 ====================

/*
使用方法：

1. 自动关联（推荐）
   mysql -u root -p youxmusicdb < 快速关联歌曲到歌手.sql

2. 手动关联单首歌曲
   INSERT INTO song_singers (song_id, singer_id) VALUES (歌曲ID, 歌手ID);

3. 查看某首歌的关联情况
   SELECT s.title, sg.name 
   FROM songs s
   INNER JOIN song_singers ss ON s.id = ss.song_id
   INNER JOIN singers sg ON ss.singer_id = sg.id
   WHERE s.id = 你的歌曲ID;

4. 如果歌手不存在，先创建歌手
   INSERT INTO singers (name, country, genre) VALUES ('歌手名', '中国', '流行');

注意事项：
- 执行前请备份数据库
- 自动关联基于songs.artist和singers.name的精确匹配
- 如果名称不匹配，需要手动关联
- 使用INSERT IGNORE避免重复关联
*/
