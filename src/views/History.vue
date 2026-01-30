<template>
  <div class="history-page">
    <div class="container">
      <!-- 页面头部 -->
      <div class="page-header">
        <div class="header-left">
          <h1 class="page-title">
            <i class="ri-history-line"></i> 播放历史
          </h1>
          <p class="page-subtitle">记录你听过的每一首歌</p>
        </div>
        <button 
          v-if="history.length > 0" 
          @click="clearAllHistory" 
          class="clear-all-btn"
        >
          <i class="ri-delete-bin-line"></i> 清空历史
        </button>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="history.length === 0" class="empty-state">
        <i class="ri-history-line empty-icon"></i>
        <div class="empty-text">还没有播放历史</div>
        <button class="empty-btn" @click="goToSongs">去发现音乐</button>
      </div>

      <!-- 历史列表 -->
      <div v-else class="history-list">
        <div 
          v-for="(song, index) in history" 
          :key="song.id"
          class="history-item"
          @click="playSong(song)"
        >
          <div class="item-index">{{ index + 1 }}</div>
          <img :src="getCoverUrl(song.cover_image)" :alt="song.title" class="item-cover" />
          <div class="item-info">
            <div class="item-title">{{ song.title }}</div>
            <div class="item-artist">{{ song.artist }}</div>
          </div>
          <div class="item-time">{{ formatTime(song.last_played) }}</div>
          <div class="item-actions">
            <FavoriteButton :song-id="song.id" />
            <button 
              @click.stop="deleteItem(song.id)" 
              class="action-btn" 
              title="删除"
            >
              <i class="ri-close-line"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="!loading && history.length > 0" class="pagination">
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
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import { historyAPI } from '../utils/api'
import FavoriteButton from '../components/FavoriteButton.vue'

// 默认封面 - 使用 SVG 占位符
const defaultCover = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%23ddd" width="100" height="100"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="30">🎵</text></svg>'

const router = useRouter()
const toast = inject('toast')
const history = ref([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const perPage = 20

// 加载播放历史
async function loadHistory() {
  loading.value = true
  try {
    const response = await historyAPI.getHistory(currentPage.value, perPage)
    history.value = response.history || []
    totalPages.value = Math.ceil((response.total || 0) / perPage)
  } catch (error) {
    console.error('加载播放历史失败:', error)
    if (error.message.includes('未登录')) {
      alert('请先登录')
      router.push('/login')
    }
  } finally {
    loading.value = false
  }
}

// 播放歌曲
function playSong(song) {
  if (window.playSong) {
    window.playSong(song)
  } else {
    alert('播放器未就绪')
  }
}

// 删除单条历史
async function deleteItem(songId) {
  if (!confirm('确定要删除这条播放记录吗？')) {
    return
  }
  
  try {
    await historyAPI.deleteHistoryItem(songId)
    // 重新加载
    await loadHistory()
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败：' + error.message)
  }
}

// 清空所有历史
async function clearAllHistory() {
  if (!confirm('确定要清空所有播放历史吗？此操作不可恢复！')) {
    return
  }
  
  try {
    await historyAPI.clearHistory()
    history.value = []
    currentPage.value = 1
    totalPages.value = 1
  } catch (error) {
    console.error('清空失败:', error)
    alert('清空失败：' + error.message)
  }
}

// 格式化时间
function formatTime(timestamp) {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  // 小于1分钟
  if (diff < 60000) {
    return '刚刚'
  }
  // 小于1小时
  if (diff < 3600000) {
    return Math.floor(diff / 60000) + '分钟前'
  }
  // 小于1天
  if (diff < 86400000) {
    return Math.floor(diff / 3600000) + '小时前'
  }
  // 小于7天
  if (diff < 604800000) {
    return Math.floor(diff / 86400000) + '天前'
  }
  // 超过7天显示日期
  return date.toLocaleDateString('zh-CN')
}

// 获取封面
function getCoverUrl(coverPath) {
  return coverPath || defaultCover
}

// 跳转到歌曲页面
function goToSongs() {
  router.push('/songs')
}

// 上一页
function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    loadHistory()
  }
}

// 下一页
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    loadHistory()
  }
}

onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
.history-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 20px;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-subtitle {
  font-size: 14px;
  color: #999;
  margin: 0;
}

.clear-all-btn {
  padding: 10px 20px;
  background: #ff4444;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.clear-all-btn:hover {
  background: #ff6666;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 68, 68, 0.3);
}

/* 加载状态 */
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
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
}

.empty-icon {
  font-size: 80px;
  color: #ddd;
  margin-bottom: 20px;
}

.empty-text {
  font-size: 16px;
  color: #999;
  margin-bottom: 24px;
}

.empty-btn {
  padding: 12px 32px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.empty-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* 历史列表 */
.history-list {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.history-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  gap: 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s;
}

.history-item:hover {
  background: #f8f9fa;
}

.history-item:last-child {
  border-bottom: none;
}

.item-index {
  width: 40px;
  text-align: center;
  color: #999;
  font-size: 14px;
  font-weight: 600;
}

.item-cover {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-artist {
  font-size: 13px;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-time {
  font-size: 13px;
  color: #999;
  min-width: 80px;
  text-align: right;
}

.item-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: transparent;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  color: #999;
}

.action-btn:hover {
  background: #f0f0f0;
  color: #ff4444;
  transform: scale(1.1);
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
  border: 2px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  background: #667eea;
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

  .clear-all-btn {
    width: 100%;
    justify-content: center;
  }

  .item-time {
    display: none;
  }

  .item-actions {
    display: none;
  }
}
</style>
