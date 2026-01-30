<template>
  <div class="favorite-page">
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else class="favorite-content">
      <!-- 页面头部 -->
      <div class="favorite-header">
        <div class="cover-section">
          <div class="favorite-cover">
            <i class="ri-heart-fill heart-icon"></i>
          </div>
        </div>
        
        <div class="info-section">
          <div class="playlist-tag">我的收藏</div>
          <h1 class="playlist-name">我喜欢的音乐</h1>
          
          <div class="playlist-meta">
            <span class="creator">
              <i class="ri-user-line creator-avatar"></i>
              {{ userInfo.name }}
            </span>
          </div>
          
          <div class="playlist-stats">
            <span class="stat-item">
              <i class="ri-music-2-line stat-icon"></i>
              {{ songs.length }} 首歌曲
            </span>
          </div>
          
          <div class="action-buttons">
            <button class="btn-primary" @click="playAll" v-if="songs.length > 0">
              <i class="ri-play-fill btn-icon"></i>
              播放全部
            </button>
          </div>
        </div>
      </div>
      
      <!-- 歌曲列表 -->
      <div class="songs-section">
        <div class="section-header">
          <h2 class="section-title">歌曲列表</h2>
          <span class="song-count">共 {{ songs.length }} 首</span>
        </div>
        
        <div v-if="songs.length === 0" class="empty-songs">
          <i class="ri-heart-line empty-icon"></i>
          <div class="empty-text">还没有收藏歌曲</div>
          <button class="empty-btn" @click="goToSongs">去发现音乐</button>
        </div>
        
        <div v-else class="song-list">
          <div class="song-list-header">
            <div class="col-index">#</div>
            <div class="col-title">歌曲</div>
            <div class="col-artist">歌手</div>
            <div class="col-album">专辑</div>
            <div class="col-duration">时长</div>
            <div class="col-actions">操作</div>
          </div>
          
          <div 
            v-for="(song, index) in songs" 
            :key="song.id"
            class="song-item"
            @dblclick="playSong(song)"
          >
            <div class="col-index">{{ index + 1 }}</div>
            <div class="col-title">
              <img :src="getCoverUrl(song)" :alt="song.title" class="song-cover" />
              <span class="song-title">{{ song.title }}</span>
            </div>
            <div class="col-artist">{{ song.artist }}</div>
            <div class="col-album">{{ song.album || '-' }}</div>
            <div class="col-duration">{{ formatDuration(song.duration) }}</div>
            <div class="col-actions">
              <button class="action-btn" @click="playSong(song)" title="播放">
                <i class="ri-play-fill"></i>
              </button>
              <FavoriteButton :song-id="song.id" @update:favorite="handleFavoriteUpdate" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { favoriteAPI } from '../utils/api'
import FavoriteButton from '../components/FavoriteButton.vue'
import daitu1 from '../assets/daitu1.jpg'

const router = useRouter()
const songs = ref([])
const loading = ref(true)

// 获取用户信息
const getUserInfo = () => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      return JSON.parse(userStr)
    } catch (e) {
      return null
    }
  }
  return null
}

const currentUser = getUserInfo()

const userInfo = reactive({
  name: currentUser?.username || '游客'
})

// 加载收藏歌曲
async function loadFavoriteSongs() {
  if (!currentUser) {
    router.push('/login')
    return
  }
  
  loading.value = true
  try {
    const response = await favoriteAPI.getFavoriteSongs()
    songs.value = response.songs || []
  } catch (error) {
    console.error('加载收藏歌曲失败:', error)
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

// 播放全部
function playAll() {
  if (songs.value.length === 0) {
    alert('还没有收藏歌曲')
    return
  }
  playSong(songs.value[0])
}

// 去发现音乐
function goToSongs() {
  router.push('/songs')
}

// 获取封面URL
function getCoverUrl(song) {
  if (!song || !song.cover_image) {
    return daitu1
  }
  if (song.cover_image.startsWith('http')) {
    return song.cover_image
  }
  return song.cover_image
}

// 格式化时长
function formatDuration(seconds) {
  if (!seconds) return '--:--'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 处理收藏状态更新
function handleFavoriteUpdate(isFavorite) {
  if (!isFavorite) {
    // 取消收藏后重新加载列表
    loadFavoriteSongs()
  }
}

onMounted(() => {
  loadFavoriteSongs()
})
</script>

<style scoped>
.favorite-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 100px 20px;
  font-size: 16px;
  color: #999;
}

/* 页面头部 */
.favorite-header {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
  padding: 30px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  border-radius: 16px;
  color: white;
}

.cover-section {
  flex-shrink: 0;
}

.favorite-cover {
  width: 200px;
  height: 200px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.heart-icon {
  font-size: 80px;
}

.info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.playlist-tag {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 12px;
  margin-bottom: 12px;
  width: fit-content;
}

.playlist-name {
  font-size: 32px;
  font-weight: bold;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.playlist-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
  opacity: 0.9;
}

.creator {
  display: flex;
  align-items: center;
  gap: 6px;
}

.creator-avatar {
  font-size: 16px;
}

.playlist-stats {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  font-size: 14px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-icon {
  font-size: 12px;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.btn-primary {
  padding: 12px 24px;
  border: none;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  background: white;
  color: #ff6b6b;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
}

.btn-icon {
  font-size: 14px;
}

/* 歌曲列表区域 */
.songs-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.song-count {
  color: #999;
  font-size: 14px;
}

/* 空状态 */
.empty-songs {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.3;
}

.empty-text {
  color: #999;
  font-size: 15px;
  margin-bottom: 20px;
}

.empty-btn {
  background: #ff6b6b;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.empty-btn:hover {
  background: #ff5252;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
}

/* 歌曲列表 */
.song-list {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.song-list-header,
.song-item {
  display: grid;
  grid-template-columns: 50px 1fr 150px 150px 80px 100px;
  gap: 16px;
  align-items: center;
  padding: 12px 16px;
}

.song-list-header {
  background: #f5f5f5;
  font-size: 13px;
  font-weight: 600;
  color: #666;
  border-bottom: 1px solid #e0e0e0;
}

.song-item {
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.2s;
  cursor: pointer;
}

.song-item:last-child {
  border-bottom: none;
}

.song-item:hover {
  background: #f8f9fa;
}

.col-index {
  text-align: center;
  color: #999;
  font-size: 14px;
}

.col-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.song-cover {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  object-fit: cover;
}

.song-title {
  font-weight: 500;
  color: #333;
}

.col-artist,
.col-album {
  color: #666;
  font-size: 14px;
}

.col-duration {
  color: #999;
  font-size: 14px;
}

.col-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: transparent;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #e0e0e0;
}

/* 响应式 */
@media (max-width: 768px) {
  .favorite-header {
    flex-direction: column;
    text-align: center;
  }
  
  .favorite-cover {
    margin: 0 auto;
  }
  
  .song-list-header,
  .song-item {
    grid-template-columns: 40px 1fr 80px 80px;
  }
  
  .col-album,
  .col-actions {
    display: none;
  }
}
</style>
