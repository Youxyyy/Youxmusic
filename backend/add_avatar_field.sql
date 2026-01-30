-- 添加头像字段到 users 表
USE youxmusic;

-- 添加 avatar 字段
ALTER TABLE users ADD COLUMN avatar VARCHAR(500) COMMENT '用户头像路径';

-- 查看表结构
DESCRIBE users;

-- 查看用户信息
SELECT id, username, email, avatar FROM users LIMIT 5;
