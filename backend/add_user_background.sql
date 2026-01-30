-- 为users表添加背景图片字段
-- 用于存储用户自定义的背景图片设置

ALTER TABLE users 
ADD COLUMN background_image VARCHAR(500) DEFAULT NULL COMMENT '用户自定义背景图片路径',
ADD COLUMN background_type ENUM('default', 'preset', 'custom') DEFAULT 'default' COMMENT '背景类型：default默认，preset预设，custom自定义';

-- 创建索引
CREATE INDEX idx_background_type ON users(background_type);

-- 查看表结构
DESCRIBE users;
