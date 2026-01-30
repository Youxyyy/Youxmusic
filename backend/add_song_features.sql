-- 为songs表添加首页推荐和新歌标记字段
ALTER TABLE songs 
ADD COLUMN is_featured BOOLEAN DEFAULT FALSE COMMENT '是否首页推荐（大家都在听）',
ADD COLUMN is_new BOOLEAN DEFAULT FALSE COMMENT '是否新歌';

-- 创建索引
CREATE INDEX idx_is_featured ON songs(is_featured);
CREATE INDEX idx_is_new ON songs(is_new);
