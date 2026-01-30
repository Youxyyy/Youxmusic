-- 为songs表添加"推荐歌曲"标记字段
-- 用于控制首页"推荐歌曲"板块显示的歌曲

ALTER TABLE songs 
ADD COLUMN is_recommended BOOLEAN DEFAULT FALSE COMMENT '是否推荐歌曲（首页推荐歌曲板块）';

-- 创建索引
CREATE INDEX idx_is_recommended ON songs(is_recommended);

-- 查看表结构
DESCRIBE songs;

-- 使用说明：
-- is_featured = TRUE：显示在"大家都在听"板块
-- is_new = TRUE：显示在"新歌推荐"板块
-- is_recommended = TRUE：显示在"推荐歌曲"板块
