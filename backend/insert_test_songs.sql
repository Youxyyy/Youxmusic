-- 插入测试歌曲数据
USE youxmusicdb;

-- 清空现有数据（可选）
-- TRUNCATE TABLE songs;

-- 插入测试歌曲
INSERT INTO songs (title, artist, album, duration, file_path, cover_image, genre, release_year, play_count) VALUES
('七里香', '周杰伦', '七里香', 300, '/music_files/qilixiang.mp3', '/covers/qilixiang.jpg', '流行', 2004, 15230),
('稻香', '周杰伦', '魔杰座', 223, '/music_files/daoxiang.mp3', '/covers/daoxiang.jpg', '流行', 2008, 12450),
('晴天', '周杰伦', '叶惠美', 269, '/music_files/qingtian.mp3', '/covers/qingtian.jpg', '流行', 2003, 18900),
('江南', '林俊杰', '江南', 250, '/music_files/jiangnan.mp3', '/covers/jiangnan.jpg', '流行', 2004, 13200),
('修炼爱情', '林俊杰', '因你而在', 267, '/music_files/xiulianaiqing.mp3', '/covers/xiulianaiqing.jpg', '流行', 2013, 9800),
('演员', '薛之谦', '绅士', 270, '/music_files/yanyuan.mp3', '/covers/yanyuan.jpg', '流行', 2015, 16700),
('丑八怪', '薛之谦', '意外', 265, '/music_files/choubaguai.mp3', '/covers/choubaguai.jpg', '流行', 2013, 11500),
('泡沫', '邓紫棋', 'Xposed', 243, '/music_files/paomo.mp3', '/covers/paomo.jpg', '流行', 2012, 14300),
('光年之外', '邓紫棋', '新的心跳', 276, '/music_files/guangnianzhi.mp3', '/covers/guangnianzhi.jpg', '流行', 2017, 10200),
('李白', '李荣浩', '模特', 260, '/music_files/libai.mp3', '/covers/libai.jpg', '流行', 2013, 12800),
('年少有为', '李荣浩', '耳朵', 285, '/music_files/nianshao.mp3', '/covers/nianshao.jpg', '流行', 2018, 8900),
('遇见', '孙燕姿', '逆光', 268, '/music_files/yujian.mp3', '/covers/yujian.jpg', '流行', 2003, 15600),
('天黑黑', '孙燕姿', '孙燕姿同名专辑', 254, '/music_files/tianheihei.mp3', '/covers/tianheihei.jpg', '流行', 2000, 13400),
('告白气球', '周杰伦', '周杰伦的床边故事', 203, '/music_files/gaobai.mp3', '/covers/gaobai.jpg', '流行', 2016, 17800),
('说好不哭', '周杰伦', '单曲', 295, '/music_files/shuohao.mp3', '/covers/shuohao.jpg', '流行', 2019, 19500),
('起风了', '买辣椒也用券', '单曲', 325, '/music_files/qifengle.mp3', '/covers/qifengle.jpg', '民谣', 2017, 21000),
('成都', '赵雷', '无法长大', 327, '/music_files/chengdu.mp3', '/covers/chengdu.jpg', '民谣', 2016, 18200),
('南山南', '马頔', '孤岛', 291, '/music_files/nanshan.mp3', '/covers/nanshan.jpg', '民谣', 2014, 16400),
('理想三旬', '陈鸿宇', '浓烟下的诗歌电台', 296, '/music_files/lixiang.mp3', '/covers/lixiang.jpg', '民谣', 2016, 14700),
('消愁', '毛不易', '明日之子', 264, '/music_files/xiaochou.mp3', '/covers/xiaochou.jpg', '民谣', 2017, 13900);

-- 查看插入的数据
SELECT * FROM songs ORDER BY created_at DESC;

-- 查看统计信息
SELECT 
    COUNT(*) as total_songs,
    COUNT(DISTINCT artist) as total_artists,
    COUNT(DISTINCT genre) as total_genres,
    SUM(play_count) as total_plays
FROM songs;
