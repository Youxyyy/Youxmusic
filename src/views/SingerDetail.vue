<template>
  <div class="singer-detail-page">
    <div class="container">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 错误提示 -->
      <div v-else-if="error" class="error-message">
        {{ error }}
        <button @click="$router.back()" class="back-btn">返回</button>
      </div>

      <!-- 歌手信息 -->
      <div v-else-if="singer" class="singer-content">
        <!-- 歌手头部 -->
        <div class="singer-header">
          <div class="singer-avatar-large">
            <img 
              :src="getSingerAvatar(singer.avatar)" 
              :alt="singer.name"
              @error="handleSingerImageError"
            />
          </div>
          <div class="singer-header-info">
            <h1 class="singer-name">{{ singer.name }}</h1>
            <div class="singer-tags">
              <span class="tag">{{ singer.country }}</span>
              <span class="tag">{{ singer.genre }}</span>
            </div>
            <p class="singer-stats">
              <i class="ri-music-2-line"></i>
              {{ singer.song_count || 0 }} 首歌曲
            </p>
            <div class="singer-actions">
              <button @click="playAll" class="btn-play-all">
                <i class="ri-play-circle-line"></i>
                播放全部
              </button>
              <button @click="$router.back()" class="btn-back">
                <i class="ri-arrow-left-line"></i>
                返回
              </button>
            </div>
          </div>
        </div>

        <!-- 歌手简介 -->
        <div v-if="singer.bio" class="singer-bio">
          <h2 class="section-title">歌手简介</h2>
          <p class="bio-text">{{ singer.bio }}</p>
        </div>

        <!-- 歌曲列表 -->
        <div class="singer-songs">
          <h2 class="section-title">热门歌曲</h2>
          
          <div v-if="loadingSongs" class="loading-songs">
            <div class="spinner-small"></div>
            <span>加载歌曲中...</span>
          </div>

          <div v-else-if="songs.length === 0" class="empty-songs">
            <i class="ri-music-line"></i>
            <p>暂无歌曲</p>
          </div>

          <div v-else class="songs-list">
            <div 
              v-for="(song, index) in songs" 
              :key="song.id"
              class="song-item"
              @click="playSong(song)"
            >
              <div class="song-number">{{ index + 1 }}</div>
              <img 
                :src="getCoverUrl(song.cover_image)" 
                :alt="song.title"
                class="song-cover"
                @error="handleImageError"
              />
              <div class="song-info">
                <div class="song-title">{{ song.title }}</div>
                <div class="song-artist">{{ song.artist }}</div>
              </div>
              <div class="song-album">{{ song.album || '-' }}</div>
              <div class="song-duration">{{ formatDuration(song.duration) }}</div>
              <div class="song-actions">
                <FavoriteButton :song-id="song.id" />
                <button class="action-btn" @click.stop="addToQueue(song)" title="添加到播放列表">
                  <i class="ri-add-line"></i>
                </button>
              </div>
            </div>
          </div>

          <!-- 分页 -->
          <div v-if="songs.length > 0 && totalPages > 1" class="pagination">
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRoute } from 'vue-router'
import { singerAPI } from '../utils/api.js'
import FavoriteButton from '../components/FavoriteButton.vue'

const route = useRoute()
const toast = inject('toast')

// 响应式数据
const singer = ref(null)
const songs = ref([])
const loading = ref(false)
const loadingSongs = ref(false)
const error = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const perPage = 20

// 获取歌手详情
async function fetchSingerDetail() {
  loading.value = true
  error.value = ''
  
  try {
    const singerId = route.params.id
    const response = await singerAPI.getSinger(singerId)
    
    if (response.code === 200) {
      singer.value = response.data
      // 获取歌手的歌曲
      await fetchSingerSongs()
    } else {
      throw new Error(response.error || '获取歌手详情失败')
    }
  } catch (err) {
    console.error('获取歌手详情失败:', err)
    error.value = err.message || '加载失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 获取歌手的歌曲
async function fetchSingerSongs() {
  loadingSongs.value = true
  
  try {
    const singerId = route.params.id
    const response = await singerAPI.getSingerSongs(singerId, currentPage.value, perPage)
    
    if (response.code === 200) {
      songs.value = response.data.songs || []
      totalPages.value = Math.ceil(response.data.total / perPage)
    } else {
      throw new Error(response.error || '获取歌曲列表失败')
    }
  } catch (err) {
    console.error('获取歌曲失败:', err)
    toast.error('获取歌曲失败')
  } finally {
    loadingSongs.value = false
  }
}

// 播放全部
function playAll() {
  if (songs.value.length === 0) {
    toast.warning('暂无歌曲')
    return
  }
  
  // 播放第一首歌
  playSong(songs.value[0])
  
  // 将其他歌曲添加到播放列表
  for (let i = 1; i < songs.value.length; i++) {
    if (window.addToQueue) {
      window.addToQueue(songs.value[i])
    }
  }
  
  toast.success(`已添加 ${songs.value.length} 首歌曲到播放列表`)
}

// 播放歌曲
function playSong(song) {
  if (window.playSong) {
    window.playSong(song)
  }
}

// 添加到播放列表
function addToQueue(song) {
  if (window.addToQueue) {
    const success = window.addToQueue(song)
    if (success) {
      toast.success('已添加到播放列表')
    } else {
      toast.warning('歌曲已在播放列表中')
    }
  } else {
    toast.warning('播放器未就绪')
  }
}

// 获取歌手头像
function getSingerAvatar(avatar) {
  if (!avatar) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect fill="%23ddd" width="200" height="200"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="60">🎤</text></svg>'
  if (avatar.startsWith('http')) return avatar
  return avatar
}

// 获取封面 URL
function getCoverUrl(coverPath) {
  if (!coverPath) return '/default-cover.jpg'
  if (coverPath.startsWith('http')) return coverPath
  return coverPath
}

// 歌手头像加载失败处理
function handleSingerImageError(e) {
  e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect fill="%23ddd" width="200" height="200"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="60">🎤</text></svg>'
}

// 歌曲封面加载失败处理
function handleImageError(e) {
  e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%23ddd" width="100" height="100"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="30">🎵</text></svg>'
}

// 格式化时长
function formatDuration(seconds) {
  if (!seconds) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 上一页
function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchSingerSongs()
  }
}

// 下一页
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchSingerSongs()
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchSingerDetail()
})
</script>

<style scoped>
.singer-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
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

.back-btn {
  margin-top: 16px;
  padding: 8px 24px;
  background: white;
  border: 1px solid #c33;
  border-radius: 8px;
  color: #c33;
  cursor: pointer;
  transition: all 0.3s;
}

.back-btn:hover {
  background: #c33;
  color: white;
}

/* 歌手头部 */
.singer-header {
  display: flex;
  gap: 32px;
  background: white;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.singer-avatar-large {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.singer-avatar-large img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.singer-header-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.singer-name {
  font-size: 36px;
  font-weight: 700;
  color: #333;
  margin: 0 0 16px 0;
}

.singer-tags {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.tag {
  padding: 6px 16px;
  background: #f0f8fa;
  color: #64AEC2;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.singer-stats {
  font-size: 16px;
  color: #666;
  margin: 0 0 24px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.singer-stats i {
  font-size: 20px;
  color: #64AEC2;
}

.singer-actions {
  display: flex;
  gap: 12px;
}

.btn-play-all {
  padding: 12px 32px;
  background: linear-gradient(135deg, #64AEC2, #4a9eb0);
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-play-all:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.3);
}

.btn-back {
  padding: 12px 24px;
  background: white;
  color: #666;
  border: 2px solid #e0e0e0;
  border-radius: 24px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-back:hover {
  border-color: #64AEC2;
  color: #64AEC2;
}

/* 歌手简介 */
.singer-bio {
  background: white;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin: 0 0 16px 0;
}

.bio-text {
  font-size: 15px;
  line-height: 1.8;
  color: #666;
  margin: 0;
}

/* 歌曲列表 */
.singer-songs {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.loading-songs {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 40px;
  color: #666;
}

.spinner-small {
  width: 24px;
  height: 24px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #64AEC2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.empty-songs {
  text-align: center;
  padding: 40px;
  color: #999;
}

.empty-songs i {
  font-size: 48px;
  margin-bottom: 12px;
}

.songs-list {
  margin-top: 16px;
}

.song-item {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 8px;
}

.song-item:hover {
  background: #f8f9fa;
}

.song-item:last-child {
  border-bottom: none;
}

.song-number {
  width: 40px;
  text-align: center;
  color: #999;
  font-size: 14px;
  font-weight: 600;
}

.song-cover {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.song-info {
  flex: 1;
  min-width: 0;
}

.song-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-artist {
  font-size: 13px;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-album {
  width: 200px;
  font-size: 13px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-duration {
  width: 60px;
  text-align: center;
  font-size: 13px;
  color: #999;
}

.song-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 16px;
}

.action-btn:hover {
  background: #64AEC2;
  border-color: #64AEC2;
  color: white;
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
  .singer-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .singer-avatar-large {
    width: 150px;
    height: 150px;
  }

  .singer-name {
    font-size: 28px;
  }

  .singer-actions {
    justify-content: center;
  }

  .song-album {
    display: none;
  }

  .song-actions {
    display: none;
  }
}
</style>
