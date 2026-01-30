<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="logo" @click="goHome">
          <i class="ri-headphone-line logo-icon"></i>
          <span>{{ siteName }}</span>
        </div>
        
        <!-- 未登录状态 -->
        <div class="header-actions" v-if="!isLoggedIn">
          <button class="btn btn-login" @click="goToLogin">登录</button>
          <button class="btn btn-signup" @click="goToRegister">注册</button>
        </div>
        
        <!-- 已登录状态 -->
        <div class="user-info" v-else>
          <div class="user-profile" @click="toggleDropdown">
            <img :src="userAvatar" :alt="username" class="user-avatar" />
            <span class="username">{{ username }}</span>
            <span class="dropdown-icon">▼</span>
          </div>
          
          <!-- 下拉菜单 -->
          <div class="dropdown-menu" v-if="showDropdown">
            <div class="dropdown-item" @click="goToMine">
              <i class="ri-user-line item-icon"></i>
              <span>我的主页</span>
            </div>
            <div class="dropdown-item" @click="logout">
              <i class="ri-logout-box-line item-icon"></i>
              <span>退出登录</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../utils/api.js'

const router = useRouter()
const siteName = ref('YouxMusic')
const showDropdown = ref(false)

// 默认头像
const defaultAvatar = 'https://cdn.jsdelivr.net/gh/Nikaple/avatar/default-boy.png'

// 检查是否登录
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('access_token')
})

// 获取用户信息
const userInfo = computed(() => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
})

// 用户名
const username = computed(() => {
  return userInfo.value?.username || '用户'
})

// 用户头像
const userAvatar = computed(() => {
  return userInfo.value?.avatar || defaultAvatar
})

// 跳转到首页
const goHome = () => {
  router.push('/')
}

// 跳转到登录页
const goToLogin = () => {
  router.push('/login')
}

// 跳转到注册页（注册模式）
const goToRegister = () => {
  router.push('/login?mode=register')
}

// 跳转到我的页面
const goToMine = () => {
  router.push('/mine')
  showDropdown.value = false
}

// 切换下拉菜单
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

// 退出登录
const logout = () => {
  authAPI.logout()
  showDropdown.value = false
  router.push('/')
  // 刷新页面以更新状态
  window.location.reload()
}

// 点击页面其他地方关闭下拉菜单
onMounted(() => {
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.user-profile') && !e.target.closest('.dropdown-menu')) {
      showDropdown.value = false
    }
  })
})
</script>

<style scoped>
.header {
  background: linear-gradient(135deg, #64AEC2 0%, #a7c5fb 100%);
  color: white;
  padding: 20px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 28px;
  font-weight: 700;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
}

.logo:hover {
  transform: scale(1.05);
}

/* logo图标 */
.logo-icon {
  margin-right: 10px;
  font-size: 28px;
}
/* 按钮容器 */
.header-actions {
  display: flex;
  gap: 15px;
}
/* 按钮基础样式 */
.btn {
  padding: 10px 20px;
  border-radius: 30px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-login {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}
/* 悬停 */
.btn-login:hover {
  background: rgba(255, 255, 255, 0.3);
}

.btn-signup {
  background: white;
  color: #64AEC2;
}
/* 悬停 */
.btn-signup:hover {
  background: #f0f0f0;
  transform: translateY(-2px);
}

/* 用户信息区域 */
.user-info {
  position: relative;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s;
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.3);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
}

.username {
  font-weight: 600;
  font-size: 15px;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-icon {
  font-size: 10px;
  transition: transform 0.3s;
}

.user-profile:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* 下拉菜单 */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 10px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  min-width: 180px;
  z-index: 1000;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  color: #333;
  cursor: pointer;
  transition: all 0.3s;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

.item-icon {
  font-size: 18px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: center;
  }
  
  .username {
    display: none;
  }
}
</style>