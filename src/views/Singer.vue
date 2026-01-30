<template>
  <div class="singer-page">
    <div class="container">
      <!-- 页面头部 -->
      <div class="page-header">
        <h1 class="page-title">歌手</h1>
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchKeyword" 
            @keyup.enter="searchSingers"
            placeholder="搜索歌手..."
            class="search-input"
          />
          <button @click="searchSingers" class="search-btn">
            <i class="ri-search-line"></i>
          </button>
        </div>
      </div>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <!-- 地区筛选 -->
        <div class="filter-group">
          <span class="filter-label">地区：</span>
          <div class="filter-options">
            <button 
              :class="['filter-btn', { active: selectedCountry === '' }]"
              @click="selectCountry('')"
            >
              全部
            </button>
            <button 
              v-for="country in countries" 
              :key="country"
              :class="['filter-btn', { active: selectedCountry === country }]"
              @click="selectCountry(country)"
            >
              {{ country }}
            </button>
          </div>
        </div>

        <!-- 字母导航 -->
        <!-- <div class="filter-group">
          <span class="filter-label">首字母：</span>
          <div class="filter-options letter-nav">
            <button 
              :class="['filter-btn', { active: selectedLetter === '' }]"
              @click="selectLetter('')"
            >
              全部
            </button>
            <button 
              v-for="letter in letters" 
              :key="letter"
              :class="['filter-btn', { active: selectedLetter === letter }]"
              @click="selectLetter(letter)"
            >
              {{ letter }}
            </button>
          </div> -->
        <!-- </div> -->
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 错误提示 -->
      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- 歌手列表 -->
      <div v-else class="singers-grid">
        <div 
          v-for="singer in singers" 
          :key="singer.id"
          class="singer-card"
          @click="goToSingerDetail(singer.id)"
        >
          <div class="singer-avatar">
            <img :src="getSingerAvatar(singer.avatar)" :alt="singer.name" />
            <div class="singer-overlay">
              <i class="ri-play-circle-line"></i>
            </div>
          </div>
          <div class="singer-info">
            <h3 class="singer-name">{{ singer.name }}</h3>
            <p class="singer-meta">
              <span class="singer-country">{{ singer.country }}</span>
              <span class="singer-genre">{{ singer.genre }}</span>
            </p>
            <p class="singer-songs">{{ singer.song_count || 0 }} 首歌曲</p>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && singers.length === 0" class="empty-state">
        <i class="ri-user-voice-line empty-icon"></i>
        <p>暂无歌手</p>
      </div>

      <!-- 分页 -->
      <div v-if="!loading && singers.length > 0 && totalPages > 1" class="pagination">
        <button 
          @click="prevPage" 
          :disabled="currentPage === 1"
          class="page-btn"
        >
          上一页
        </button>
        <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
        <button 
          @click="nextPage" 
          :disabled="currentPage >= totalPages"
          class="page-btn"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { singerAPI } from '../utils/api.js'

const router = useRouter()

// 响应式数据
const singers = ref([])
const loading = ref(false)
const error = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const perPage = 10

// 筛选条件
const selectedCountry = ref('')
const selectedLetter = ref('')
const countries = ref(['中国', '美国', '英国', '日本', '韩国', '新加坡'])
const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')

// 获取歌手列表
async function fetchSingers() {
  loading.value = true
  error.value = ''
  
  try {
    const params = {
      page: currentPage.value,
      per_page: perPage
    }
    
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    
    if (selectedCountry.value) {
      params.country = selectedCountry.value
    }
    
    if (selectedLetter.value) {
      params.letter = selectedLetter.value
    }
    
    const response = await singerAPI.getSingers(params)
    
    if (response.code === 200) {
      singers.value = response.data.singers || []
      totalPages.value = Math.ceil(response.data.total / perPage)
    } else {
      throw new Error(response.error || '获取歌手列表失败')
    }
  } catch (err) {
    console.error('获取歌手失败:', err)
    error.value = err.message || '加载失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 搜索歌手
function searchSingers() {
  currentPage.value = 1
  fetchSingers()
}

// 选择地区
function selectCountry(country) {
  selectedCountry.value = country
  currentPage.value = 1
  fetchSingers()
}

// 选择首字母
function selectLetter(letter) {
  selectedLetter.value = letter
  currentPage.value = 1
  fetchSingers()
}

// 获取歌手头像
function getSingerAvatar(avatar) {
  if (!avatar) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect fill="%23ddd" width="200" height="200"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="60">🎤</text></svg>'
  if (avatar.startsWith('http')) return avatar
  return avatar
}

// 跳转到歌手详情
function goToSingerDetail(singerId) {
  router.push(`/singer/${singerId}`)
}

// 上一页
function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchSingers()
  }
}

// 下一页
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchSingers()
  }
}

// 页面加载时获取歌手
onMounted(() => {
  fetchSingers()
})
</script>

<style scoped>
.singer-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 修改页面头部 */
.page-header {
  display: flex;
  justify-content: center; /* 改为居中 */
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 20px;
  position: relative; /* 添加相对定位 */
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.search-box {
  position: absolute; /* 搜索框绝对定位 */
  right: 0; /* 靠右对齐 */
}

.search-input {
  width: 300px;
  height: 44px;
  padding: 0 16px;
  border: 2px solid #e0e0e0;
  border-radius: 22px;
  font-size: 14px;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #64AEC2;
}

.search-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #64AEC2, #4a9eb0);
  color: white;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s;
}

.search-btn:hover {
  transform: scale(1.05);
}

/* 筛选栏 */
.filter-bar {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.filter-group {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
}

.filter-group:last-child {
  margin-bottom: 0;
}

.filter-label {
  font-size: 14px;
  font-weight: 600;
  color: #666;
  min-width: 80px;
  padding-top: 8px;
}

.filter-options {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-btn {
  padding: 6px 16px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 20px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-btn:hover {
  border-color: #64AEC2;
  color: #64AEC2;
}

.filter-btn.active {
  background: #64AEC2;
  border-color: #64AEC2;
  color: white;
}

.letter-nav .filter-btn {
  min-width: 36px;
  padding: 6px 8px;
  text-align: center;
}

/* 加载和错误状态 */
.loading {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 16px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #64AEC2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

/* 歌手网格 */
.singers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.singer-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.singer-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(100, 174, 194, 0.2);
}

.singer-avatar {
  position: relative;
  width: 100%;
  padding-top: 100%;
  overflow: hidden;
  background: #f5f5f5;
}

.singer-avatar img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.singer-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s;
}

.singer-card:hover .singer-overlay {
  opacity: 1;
}

.singer-overlay i {
  font-size: 48px;
  color: white;
}

.singer-info {
  padding: 16px;
}

.singer-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.singer-meta {
  font-size: 12px;
  color: #999;
  margin: 0 0 8px 0;
  display: flex;
  gap: 8px;
}

.singer-country,
.singer-genre {
  padding: 2px 8px;
  background: #f5f5f5;
  border-radius: 10px;
}

.singer-songs {
  font-size: 13px;
  color: #666;
  margin: 0;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  color: #ddd;
  margin-bottom: 16px;
}

.empty-state p {
  color: #999;
  font-size: 16px;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 32px;
}

.page-btn {
  padding: 10px 24px;
  border: 2px solid #64AEC2;
  background: white;
  color: #64AEC2;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  background: #64AEC2;
  color: white;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #666;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .singers-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 16px;
  }

  .filter-group {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-label {
    margin-bottom: 8px;
  }
}
</style>
