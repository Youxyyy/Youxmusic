-- 添加管理员字段到 users 表
USE youxmusic;

-- 添加 is_admin 字段
ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE COMMENT '是否为管理员';

-- 创建索引
ALTER TABLE users ADD INDEX idx_is_admin (is_admin);

-- 设置第一个用户为管理员（可选，根据实际情况修改）
-- UPDATE users SET is_admin = TRUE WHERE id = 1;

-- 或者根据用户名设置管理员
-- UPDATE users SET is_admin = TRUE WHERE username = 'admin';

-- 查看表结构
DESCRIBE users;

-- 查看管理员用户
SELECT id, username, email, is_admin FROM users WHERE is_admin = TRUE;
