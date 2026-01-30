<template>
  <nav class="navigation">
    <div class="container nav-container">
      <div class="mobile-toggle" @click="toggleMobileMenu">
        <i class="ri-menu-line"></i>
      </div>
      <ul class="nav-links" :class="{ active: isMobileMenuOpen }">
        <li v-for="item in navItems" :key="item.path">
          <router-link 
            :to="item.path" 
            :class="{ active: $route.path === item.path }"
            @click="closeMobileMenu"
          >
            {{ item.name }}
          </router-link>
        </li>
      </ul>
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索..." 
          v-model="searchQuery"
          @keyup.enter="performSearch"
        >
        <i class="ri-search-line search-icon" @click="performSearch"></i>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isMobileMenuOpen = ref(false)
const searchQuery = ref('')

const navItems = [
  { name: '首页', path: '/' },
  { name: '发现音乐', path: '/songs' },
  { name: '榜单', path: '/rankinglist' },
  { name: '白噪音', path: '/whitenoise' },
  { name: '歌手', path: '/singer' },
  { name: '我的', path: '/mine' },
  { name: '关于我们', path: '/about' },
  { name: '联系我们', path: '/contact' }
]

const emit = defineEmits(['search'])

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const performSearch = () => {
  if (searchQuery.value.trim()) {
    emit('search', searchQuery.value)
    searchQuery.value = ''
  }
}

// 路由变化时关闭移动端菜单
watch(() => route.path, () => {
  closeMobileMenu()
})
</script>

<style scoped>
.navigation {
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  /* 粘性导航栏，正常滚动时随页面滚动，顶部时固定在上方 */
  position: sticky;
  top: 0;
  /* 确保导航栏始终在其他内容上方 */
  z-index: 100;
}

.nav-container {
  /* 弹性布局，子元素水平排列且两端对齐 */
  display: flex;
  /* 子元素两端对齐，左侧导航栏，右侧搜索框 */
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  /* 水平排列导航链接 */
  display: flex;
  /* 移除列表默认的圆点标记 */
  list-style: none;
}

.nav-links li {
  position: relative;
}

.nav-links a {
  display: block;
  padding: 20px 25px;
  text-decoration: none;
  color: #444;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
}

/* 鼠标悬停时的颜色变化 */
.nav-links a:hover {
  color: #64AEC2;
}

/* 当前活跃页面效果 */
.nav-links a.router-link-active {
  color: #64AEC2;
  font-weight: 600;
}

/* 活跃页面下划线效果 */
.nav-links a.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 25px;
  right: 25px;
  height: 3px;
  background-color: #64AEC2;
  border-radius: 3px 3px 0 0;
}
/* 搜索框容器 */
.search-box {
  display: flex;
  align-items: center;
  background: #f5f7fa;
  border-radius: 30px;
  padding: 8px 15px;
  margin-left: 20px;
}
/* 搜索输入框容器 */
.search-box input {
  border: none;
  background: transparent;
  padding: 5px 10px;
  outline: none;
  width: 180px;
}

.search-icon {
  color: #777;
  cursor: pointer;
  font-size: 18px;
  transition: color 0.3s;
}

.search-icon:hover {
  color: #64AEC2;
}
/* 移动端菜单栏切换按钮 */
.mobile-toggle {
  display: none;
  font-size: 24px;
  cursor: pointer;
  color: #444;
  transition: color 0.3s;
}

.mobile-toggle:hover {
  color: #64AEC2;
}
/* 移动端响应式布局 */
@media (max-width: 992px) {
  .nav-links {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    flex-direction: column;
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
  }
  
  .nav-links.active {
    display: flex;
  }
  
  .nav-links li {
    width: 100%;
  }
  
  .nav-links a {
    padding: 15px 20px;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .mobile-toggle {
    display: block;
  }
  
  .search-box {
    margin: 15px 20px;
    width: calc(100% - 40px);
  }
  
  .search-box input {
    width: 100%;
  }
}
</style>