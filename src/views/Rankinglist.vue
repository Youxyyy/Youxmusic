<template>
  <div class="ranking-page">
    <div class="container">
      <!-- 页面头部 -->
      <div class="page-header">
        <h1 class="page-title">音乐排行榜</h1>
        <p class="page-subtitle">基于播放量、收藏量和热度的综合排名</p>
      </div>

      <!-- Tab切换 -->
      <div class="ranking-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.value"
          :class="['tab-btn', { active: activeTab === tab.value }]"
          @click="switchTab(tab.value)"
        >
          <i :class="tab.icon"></i>
          <span>{{ tab.label }}</span>
        </button>
      </div>

      <!-- 分类切换 -->
      <div class="genre-filter">
        <button 
          v-for="g in genres" 
          :key="g.value"
          :class="['genre-btn', { active: activeGenre === g.value }]"
          @click="switchGenre(g.value)"
        >
          {{ g.label }}
        </button>
      </div>

      <!-- 统计信息 -->
      <div v-if="stats" class="stats-bar">
        <div class="stat-item">
          <i class="ri-play-circle-line"></i>
          <span>总播放：{{ formatNumber(stats.total_plays) }}</span>
        </div>
        <div class="stat-item">
          <i class="ri-heart-line"></i>
          <span>总收藏：{{ formatNumber(stats.total_favorites) }}</span>
        </div>
        <div class="stat-item">
          <i class="ri-fire-line"></i>
          <span>近7天：{{ formatNumber(stats.recent_plays) }}</span>
        </div>
        <div class="stat-item update-time">
          <i class="ri-time-line"></i>
          <span>更新：{{ rankingData.updated_at }}</span>
        </div>
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

      <!-- 排行榜列表 -->
      <div v-else class="ranking-list">
        <div 
          v-for="song in songs" 
          :key="song.id"
          :class="['ranking-item', getRankClass(song.rank)]"
          @click="addToQueue(song)"
        >
          <!-- 排名 -->
          <div class="rank-number">
            <span v-if="song.rank <= 3" class="trophy">
              <i v-if="song.rank === 1" class="ri-trophy-fill" style="color: #FFD700;"></i>
              <i v-else-if="song.rank === 2" class="ri-trophy-fill" style="color: #C0C0C0;"></i>
              <i v-else class="ri-trophy-fill" style="color: #CD7F32;"></i>
            </span>
            <span v-else-if="song.rank <= 10" class="medal">
              <i class="ri-medal-line"></i>
            </span>
            <span class="rank-text">{{ song.rank }}</span>
          </div>

          <!-- 封面 -->
          <img 
            :src="getCoverUrl(song.cover_image)" 
            :alt="song.title"
            class="song-cover"
            @error="handleImageError"
          />

          <!-- 歌曲信息 -->
          <div class="song-info">
            <div class="song-title">{{ song.title }}</div>
            <div class="song-meta">
              <span class="song-artist">{{ song.artist }}</span>
              <span class="separator">·</span>
              <span class="song-album">{{ song.album }}</span>
            </div>
          </div>

          <!-- 数据指标 -->
          <div class="song-stats">
            <div class="stat">
              <i class="ri-play-circle-line"></i>
              <span>{{ formatNumber(song.play_count) }}</span>
            </div>
            <div class="stat">
              <i class="ri-heart-line"></i>
              <span>{{ formatNumber(song.favorite_count) }}</span>
            </div>
            <div class="stat score">
              <i class="ri-fire-line"></i>
              <span>{{ song.score }}</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="song-actions">
            <FavoriteButton :song-id="song.id" />
            <button class="action-btn play-btn" @click.stop="playSong(song)" title="播放">
              <i class="ri-play-fill"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && songs.length === 0" class="empty-state">
        <i class="ri-music-line empty-icon"></i>
        <p>暂无排行数据</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { rankingAPI } from '../utils/api.js'
import FavoriteButton from '../components/FavoriteButton.vue'

const toast = inject('toast')

// 响应式数据
const loading = ref(false)
const error = ref('')
const activeTab = ref('week')
const activeGenre = ref('all')
const songs = ref([])
const rankingData = ref({})
const stats = ref(null)

// Tab选项
const tabs = [
  { value: 'day', label: '日榜', icon: 'ri-calendar-line' },
  { value: 'week', label: '周榜', icon: 'ri-calendar-line' },
  { value: 'month', label: '月榜', icon: 'ri-calendar-line' }
]

// 分类选项
const genres = ref([
  { value: 'all', label: '全部' },
  { value: '流行', label: '华语流行' },
  { value: '欧美', label: '欧美' },
  { value: '日韩', label: '日韩' },
  { value: '民谣', label: '民谣' },
  { value: '摇滚', label: '摇滚' },
  { value: '电子', label: '电子' }
])

// 获取排行榜数据
async function fetchRanking() {
  loading.value = true
  error.value = ''
  
  try {
    const response = await rankingAPI.getRanking(activeTab.value, activeGenre.value, 20)
    
    if (response.code === 200) {
      rankingData.value = response.data
      songs.value = response.data.songs || []
    } else {
      throw new Error(response.error || '获取排行榜失败')
    }
  } catch (err) {
    console.error('获取排行榜失败:', err)
    error.value = err.message || '加载失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 获取统计信息
async function fetchStats() {
  try {
    const response = await rankingAPI.getStats()
    if (response.code === 200) {
      stats.value = response.data
    }
  } catch (err) {
    console.error('获取统计信息失败:', err)
  }
}

// 切换Tab
function switchTab(tab) {
  activeTab.value = tab
  fetchRanking()
}

// 切换分类
function switchGenre(genre) {
  activeGenre.value = genre
  fetchRanking()
}

// 获取排名样式类
function getRankClass(rank) {
  if (rank === 1) return 'rank-1'
  if (rank === 2) return 'rank-2'
  if (rank === 3) return 'rank-3'
  if (rank <= 10) return 'rank-top10'
  return ''
}

// 播放歌曲
function playSong(song) {
  if (window.playSong) {
    window.playSong(song)
    toast.success(`正在播放：${song.title}`)
  } else {
    toast.warning('播放器未就绪')
  }
}

// 添加到播放队列
function addToQueue(song) {
  if (window.addToQueue) {
    const success = window.addToQueue(song)
    if (success) {
      toast.success(`已添加到播放列表`)
    } else {
      toast.warning('歌曲已在播放列表中')
    }
  } else {
    toast.warning('播放器未就绪')
  }
}

// 获取封面URL
function getCoverUrl(coverPath) {
  if (!coverPath) return '/default-cover.jpg'
  if (coverPath.startsWith('http')) return coverPath
  return coverPath
}

// 图片加载失败处理
function handleImageError(e) {
  e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%23ddd" width="100" height="100"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="30">🎵</text></svg>'
}

// 格式化数字
function formatNumber(num) {
  if (!num) return '0'
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toString()
}

// 页面加载时获取数据
onMounted(() => {
  fetchRanking()
  fetchStats()
})
</script>

<style scoped>
.ranking-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 40px 20px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

/* 页面头部 */
.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 12px 0;
  color: #333;
}

.page-subtitle {
  font-size: 16px;
  color: #666;
  margin: 0;
}

/* Tab切换 */
.ranking-tabs {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 24px;
}

.tab-btn {
  padding: 12px 32px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 50px;
  color: #666;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.tab-btn:hover {
  border-color: #64AEC2;
  color: #64AEC2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.2);
}

.tab-btn.active {
  background: linear-gradient(135deg, #64AEC2, #5a9fb0);
  color: white;
  border-color: #64AEC2;
  box-shadow: 0 4px 15px rgba(100, 174, 194, 0.3);
}

.tab-btn i {
  font-size: 18px;
}

/* 分类筛选 */
.genre-filter {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
}

.genre-btn {
  padding: 8px 20px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.genre-btn:hover {
  border-color: #64AEC2;
  color: #64AEC2;
}

.genre-btn.active {
  background: #64AEC2;
  color: white;
  border-color: #64AEC2;
}

/* 统计信息 */
.stats-bar {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 24px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
}

.stat-item i {
  font-size: 18px;
  color: #64AEC2;
}

.update-time {
  color: #999;
  font-size: 12px;
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

/* 排行榜列表 */
.ranking-list {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.ranking-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  gap: 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s;
}

.ranking-item:hover {
  background: #f8f9fa;
  transform: translateX(4px);
}

.ranking-item:last-child {
  border-bottom: none;
}

/* 前三名高亮 */
.ranking-item.rank-1 {
  background: linear-gradient(90deg, #fff9e6 0%, #ffffff 100%);
}

.ranking-item.rank-2 {
  background: linear-gradient(90deg, #f5f5f5 0%, #ffffff 100%);
}

.ranking-item.rank-3 {
  background: linear-gradient(90deg, #fff5e6 0%, #ffffff 100%);
}

.ranking-item.rank-top10 {
  background: linear-gradient(90deg, #f8f9ff 0%, #ffffff 100%);
}

/* 排名 */
.rank-number {
  width: 60px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.trophy, .medal {
  font-size: 28px;
  line-height: 1;
}

.rank-text {
  font-size: 18px;
  font-weight: 700;
  color: #333;
  line-height: 1;
}

.rank-1 .trophy {
  font-size: 32px;
}

.rank-1 .rank-text {
  color: #FFD700;
  font-size: 20px;
}

.rank-2 .trophy {
  font-size: 30px;
}

.rank-2 .rank-text {
  color: #C0C0C0;
  font-size: 19px;
}

.rank-3 .trophy {
  font-size: 28px;
}

.rank-3 .rank-text {
  color: #CD7F32;
  font-size: 18px;
}

.rank-top10 .medal {
  font-size: 24px;
  color: #64AEC2;
}

/* 封面 */
.song-cover {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 歌曲信息 */
.song-info {
  flex: 1;
  min-width: 0;
}

.song-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-meta {
  font-size: 13px;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
}

.separator {
  color: #ddd;
}

/* 数据指标 */
.song-stats {
  display: flex;
  gap: 20px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #666;
}

.stat i {
  font-size: 16px;
  color: #999;
}

.stat.score {
  color: #ff6b6b;
  font-weight: 600;
}

.stat.score i {
  color: #ff6b6b;
}

/* 操作按钮 */
.song-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: transparent;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  transform: scale(1.1);
}

.play-btn {
  background: linear-gradient(135deg, #64AEC2, #5a9fb0);
  color: white;
}

.play-btn:hover {
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.4);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
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

/* 响应式 */
@media (max-width: 768px) {
  .page-title {
    font-size: 32px;
  }

  .ranking-tabs {
    flex-direction: column;
  }

  .tab-btn {
    width: 100%;
    justify-content: center;
  }

  .song-stats {
    display: none;
  }

  .song-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .separator {
    display: none;
  }
}
</style>
