<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <!-- 标题 -->
        <div class="login-header">
          <h2 class="login-title">{{ isLogin ? '登录' : '注册' }}</h2>
          <p class="login-subtitle">{{ isLogin ? '欢迎回来' : '创建你的账号' }}</p>
        </div>

        <!-- 登录表单 -->
        <form class="login-form" @submit.prevent="handleSubmit" v-if="isLogin">
          <div class="form-group">
            <label class="form-label">手机号/邮箱</label>
            <input 
              type="text" 
              class="form-input" 
              v-model="loginForm.account"
              placeholder="请输入手机号或邮箱"
            />
          </div>

          <div class="form-group">
            <label class="form-label">密码</label>
            <input 
              type="password" 
              class="form-input" 
              v-model="loginForm.password"
              placeholder="请输入密码"
            />
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="loginForm.remember" />
              <span>记住我</span>
            </label>
            <a href="#" class="forgot-link">忘记密码？</a>
          </div>

          <button type="submit" class="submit-btn">登录</button>
        </form>

        <!-- 注册表单 -->
        <form class="login-form" @submit.prevent="handleSubmit" v-else>
          <div class="form-group">
            <label class="form-label">用户名</label>
            <input 
              type="text" 
              class="form-input" 
              v-model="registerForm.username"
              placeholder="请输入用户名"
            />
          </div>

          <div class="form-group">
            <label class="form-label">手机号</label>
            <input 
              type="tel" 
              class="form-input" 
              v-model="registerForm.phone"
              placeholder="请输入手机号"
            />
          </div>

          <div class="form-group">
            <label class="form-label">邮箱</label>
            <input 
              type="email" 
              class="form-input" 
              v-model="registerForm.email"
              placeholder="请输入邮箱"
            />
          </div>

          <div class="form-group">
            <label class="form-label">密码</label>
            <input 
              type="password" 
              class="form-input" 
              v-model="registerForm.password"
              placeholder="请输入密码（6-20位）"
            />
          </div>

          <div class="form-group">
            <label class="form-label">确认密码</label>
            <input 
              type="password" 
              class="form-input" 
              v-model="registerForm.confirmPassword"
              placeholder="请再次输入密码"
            />
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="registerForm.agree" />
              <span>我已阅读并同意<a href="#" class="link">用户协议</a>和<a href="#" class="link">隐私政策</a></span>
            </label>
          </div>

          <button type="submit" class="submit-btn">注册</button>
        </form>

        <!-- 切换登录/注册 -->
        <div class="switch-mode">
          <span v-if="isLogin">还没有账号？</span>
          <span v-else>已有账号？</span>
          <a href="#" @click.prevent="toggleMode" class="switch-link">
            {{ isLogin ? '立即注册' : '立即登录' }}
          </a>
        </div>

        <!-- 第三方登录 -->
        <div class="social-login">
          <div class="divider">
            <span>或使用以下方式登录</span>
          </div>
          <div class="social-buttons">
            <button class="social-btn" @click="socialLogin('wechat')">
              <span class="social-icon">💬</span>
              <span>微信</span>
            </button>
            <button class="social-btn" @click="socialLogin('qq')">
              <span class="social-icon">🐧</span>
              <span>QQ</span>
            </button>
            <button class="social-btn" @click="socialLogin('weibo')">
              <span class="social-icon">📱</span>
              <span>微博</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { authAPI } from '../utils/api.js'

const route = useRoute()
const isLogin = ref(true)

// 检查URL参数，如果有mode=register则显示注册表单
onMounted(() => {
  if (route.query.mode === 'register') {
    isLogin.value = false
  }
})

const loginForm = reactive({
  account: '',
  password: '',
  remember: false
})

const registerForm = reactive({
  username: '',
  phone: '',
  email: '',
  password: '',
  confirmPassword: '',
  agree: false
})

function toggleMode() {
  isLogin.value = !isLogin.value
}

async function handleSubmit() {
  if (isLogin.value) {
    // 登录逻辑
    if (!loginForm.account || !loginForm.password) {
      alert('请填写完整信息')
      return
    }
    // 调用API
    try {
      const data = await authAPI.login({
        account: loginForm.account,
        password: loginForm.password
      })
      
      // 保存token和用户信息
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      alert('登录成功！')
      // 跳转到首页或我的页面
      window.location.href = '/'
    } catch (error) {
      alert(error.message || '登录失败')
    }
  } else {
    // 注册逻辑
    if (!registerForm.username || !registerForm.email || !registerForm.password) {
      alert('请填写完整信息')
      return
    }
    if (registerForm.password !== registerForm.confirmPassword) {
      alert('两次密码不一致')
      return
    }
    if (!registerForm.agree) {
      alert('请同意用户协议和隐私政策')
      return
    }
    
    try {
      await authAPI.register({
        username: registerForm.username,
        email: registerForm.email,
        phone: registerForm.phone,
        password: registerForm.password
      })
      
      alert('注册成功！请登录')
      // 切换到登录模式
      isLogin.value = true
      // 清空表单
      registerForm.username = ''
      registerForm.phone = ''
      registerForm.email = ''
      registerForm.password = ''
      registerForm.confirmPassword = ''
      registerForm.agree = false
    } catch (error) {
      alert(error.message || '注册失败')
    }
  }
}

function socialLogin(type) {
  alert(`使用${type}登录功能开发中...`)
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.login-card {
  width: 100%;
  max-width: 440px;
  background: white;
  border-radius: 16px;
  padding: 40px 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* 标题 */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px 0;
}

.login-subtitle {
  font-size: 14px;
  color: #999;
  margin: 0;
}

/* 表单 */
.login-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  font-size: 14px;
  color: #333;
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  background: white;
  border-color: #ff4444;
}

.form-input::placeholder {
  color: #bbb;
}

/* 选项 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  font-size: 13px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  cursor: pointer;
}

.forgot-link {
  color: #ff4444;
  text-decoration: none;
  transition: all 0.3s;
}

.forgot-link:hover {
  color: #ff6666;
}

.link {
  color: #ff4444;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  height: 48px;
  background: #ff4444;
  color: white;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-btn:hover {
  background: #ff6666;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 68, 68, 0.3);
}

.submit-btn:active {
  transform: translateY(0);
}

/* 切换模式 */
.switch-mode {
  text-align: center;
  font-size: 14px;
  color: #666;
  padding: 20px 0;
  border-top: 1px solid #f0f0f0;
}

.switch-link {
  color: #ff4444;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  transition: all 0.3s;
}

.switch-link:hover {
  color: #ff6666;
}

/* 第三方登录 */
.social-login {
  margin-top: 24px;
}

.divider {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e0e0e0;
}

.divider span {
  padding: 0 16px;
  font-size: 13px;
  color: #999;
}

.social-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.social-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px;
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.social-btn:hover {
  background: white;
  border-color: #ff4444;
  transform: translateY(-2px);
}

.social-icon {
  font-size: 24px;
}

.social-btn span:last-child {
  font-size: 12px;
  color: #666;
}

/* 响应式 */
@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px;
  }

  .login-title {
    font-size: 24px;
  }

  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
