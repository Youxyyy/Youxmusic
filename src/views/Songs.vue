<template>
  <div class="songs-page">
    <div class="container">
      <div class="page-header">
        <div class="header-left">
          <h1 class="page-title">{{ searchKeyword ? '搜索结果' : '全部歌曲' }}</h1>
          <p v-if="searchKeyword" class="search-info">
            搜索 "{{ searchKeyword }}" 找到 {{ songs.length }} 首歌曲
            <button @click="clearSearch" class="clear-search-btn">
              <i class="ri-close-line"></i> 清空搜索
            </button>
          </p>
        </div>
        <div class="search-box">
          <div class="search-input-wrapper">
            <input 
              type="text" 
              v-model="searchKeyword" 
              @keyup.enter="searchSongs"
              @focus="showHistory = searchHistory.length > 0"
              @blur="setTimeout(() => showHistory = false, 200)"
              placeholder="搜索歌曲、歌手..."
              class="search-input"
            />
            <button @click="searchSongs" class="search-btn">
              <i class="ri-search-line"></i>
            </button>
            
            <!-- 搜索历史下拉 -->
            <div v-if="showHistory && searchHistory.length > 0" class="search-history-dropdown">
              <div class="history-header">
                <span>搜索历史</span>
                <button @click="clearSearchHistory" class="clear-history-btn">
                  <i class="ri-delete-bin-line"></i>
                </button>
              </div>
              <div class="history-list">
                <div 
                  v-for="(item, index) in searchHistory" 
                  :key="index"
                  class="history-item"
                  @click="useHistorySearch(item)"
                >
                  <i class="ri-time-line"></i>
                  <span>{{ item }}</span>
                  <button 
                    @click.stop="deleteHistoryItem(item)" 
                    class="delete-item-btn"
                  >
                    <i class="ri-close-line"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
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

      <!-- 歌曲列表 -->
      <div v-else class="songs-list">
        <div 
          v-for="song in songs" 
          :key="song.id"
          class="song-item"
          @click="playSong(song)"
        >
          <div class="song-number">{{ song.id }}</div>
          <img 
            :src="getCoverUrl(song.cover_image)" 
            :alt="song.title"
            class="song-cover"
            @error="handleImageError"
          />
          <div class="song-info">
            <div class="song-title">{{ song.title }}</div>
            <div class="song-artist">
              <span v-if="song.singers && song.singers.length > 0">
                <span 
                  v-for="(singer, idx) in song.singers" 
                  :key="singer.id"
                  class="singer-link"
                  @click.stop="goToSinger(singer.id)"
                >
                  {{ singer.name }}<span v-if="idx < song.singers.length - 1"> / </span>
                </span>
              </span>
              <span v-else>{{ song.artist }}</span>
            </div>
          </div>
          <div class="song-album">{{ song.album || '-' }}</div>
          <div class="song-duration">{{ formatDuration(song.duration) }}</div>
          <div class="song-actions">
            <FavoriteButton :song-id="song.id" />
            <div class="add-menu-wrapper" @mouseenter="showAddMenu(song)" @mouseleave="hideAddMenu">
              <button class="action-btn" title="添加">
                <i class="ri-add-line"></i>
              </button>
              <div v-if="activeMenuSongId === song.id" class="add-menu" @click.stop>
                <div class="menu-item" @click.stop="addToQueue(song)">
                  <i class="ri-play-list-add-line"></i>
                  <span>添加到播放列表</span>
                </div>
                <div class="menu-item" @click.stop="addToPlaylist(song)">
                  <i class="ri-folder-music-line"></i>
                  <span>添加到歌单</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="!loading && songs.length > 0" class="pagination">
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
    
    <!-- 添加到歌单弹窗 -->
    <div v-if="showPlaylistModal" class="modal" @click="showPlaylistModal = false">
      <div class="modal-content playlist-modal" @click.stop>
        <div class="modal-header">
          <h3>添加到歌单</h3>
          <button class="close-btn" @click="showPlaylistModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div v-if="selectedSong" class="selected-song">
            <img :src="getCoverUrl(selectedSong.cover_image)" class="song-thumb" />
            <div class="song-info">
              <div class="song-title">{{ selectedSong.title }}</div>
              <div class="song-artist">{{ selectedSong.artist }}</div>
            </div>
          </div>
          
          <div class="playlist-list">
            <div v-if="loadingPlaylists" class="loading-text">加载中...</div>
            
            <div v-else-if="myPlaylists.length === 0" class="empty-playlists">
              <i class="ri-folder-music-line empty-icon"></i>
              <p>还没有歌单</p>
              <p class="empty-hint">去"我的"页面创建歌单吧</p>
            </div>
            
            <div v-else class="playlists-grid">
              <div 
                v-for="playlist in myPlaylists" 
                :key="playlist.id"
                class="playlist-item"
                @click="addSongToPlaylist(playlist.id)"
              >
                <img :src="playlist.cover || '/static/playlist_covers/daitu1.jpg'" class="playlist-cover" />
                <div class="playlist-info">
                  <div class="playlist-name">{{ playlist.name }}</div>
                  <div class="playlist-count">{{ playlist.song_count || 0 }} 首歌曲</div>
                </div>
                <i class="ri-add-line add-icon"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { songAPI, playlistAPI, singerAPI } from '../utils/api.js'
import FavoriteButton from '../components/FavoriteButton.vue'

const route = useRoute()
const router = useRouter()
const toast = inject('toast')

// 响应式数据
const songs = ref([])
const loading = ref(false)
const error = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const perPage = 20
const searchHistory = ref([])
const showHistory = ref(false)

// 静态文件也通过代理访问，避免跨域问题
const STATIC_BASE = ''

// 获取歌曲列表
async function fetchSongs() {
  loading.value = true
  error.value = ''
  
  try {
    const data = await songAPI.getSongs(currentPage.value, perPage)
    
    // 检查返回数据格式
    if (data && data.data && data.data.songs) {
      songs.value = data.data.songs
      totalPages.value = Math.ceil(data.data.total / perPage)
    } else {
      throw new Error('数据格式错误')
    }
  } catch (err) {
    console.error('获取歌曲失败:', err)
    error.value = err.message || '加载失败，请确保后端服务正在运行 (http://localhost:5000)'
  } finally {
    loading.value = false
  }
}

// 搜索歌曲
async function searchSongs() {
  if (!searchKeyword.value.trim()) {
    fetchSongs()
    return
  }
  
  // 保存搜索历史
  saveSearchHistory(searchKeyword.value)
  showHistory.value = false
  
  loading.value = true
  error.value = ''
  
  try {
    const data = await songAPI.searchSongs(searchKeyword.value, currentPage.value, perPage)
    songs.value = data.data.songs || []
    totalPages.value = Math.ceil((data.data.total || 0) / perPage)
    
    // 如果没有搜索结果
    if (songs.value.length === 0) {
      error.value = `没有找到与 "${searchKeyword.value}" 相关的歌曲`
    }
  } catch (err) {
    error.value = err.message || '搜索失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 保存搜索历史
function saveSearchHistory(keyword) {
  const history = getSearchHistory()
  // 移除重复项
  const filtered = history.filter(item => item !== keyword)
  // 添加到开头
  filtered.unshift(keyword)
  // 只保留最近10条
  const limited = filtered.slice(0, 10)
  localStorage.setItem('searchHistory', JSON.stringify(limited))
  searchHistory.value = limited
}

// 获取搜索历史
function getSearchHistory() {
  try {
    const history = localStorage.getItem('searchHistory')
    return history ? JSON.parse(history) : []
  } catch {
    return []
  }
}

// 使用历史搜索
function useHistorySearch(keyword) {
  searchKeyword.value = keyword
  searchSongs()
}

// 删除单条历史
function deleteHistoryItem(keyword) {
  const history = getSearchHistory()
  const filtered = history.filter(item => item !== keyword)
  localStorage.setItem('searchHistory', JSON.stringify(filtered))
  searchHistory.value = filtered
}

// 清空搜索历史
function clearSearchHistory() {
  localStorage.removeItem('searchHistory')
  searchHistory.value = []
}

// 清空搜索
function clearSearch() {
  searchKeyword.value = ''
  currentPage.value = 1
  fetchSongs()
  // 清除URL参数
  window.history.pushState({}, '', '/songs')
}

// 播放歌曲
function playSong(song) {
  if (window.playSong) {
    window.playSong(song)
  }
}

// 获取封面 URL
function getCoverUrl(coverPath) {
  if (!coverPath) return '/default-cover.jpg'
  if (coverPath.startsWith('http')) return coverPath
  return `${STATIC_BASE}${coverPath}`
}

// 图片加载失败处理
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

// 添加到歌单相关
const showPlaylistModal = ref(false)
const selectedSong = ref(null)
const myPlaylists = ref([])
const loadingPlaylists = ref(false)
const activeMenuSongId = ref(null)
let menuTimer = null

// 显示添加菜单
function showAddMenu(song) {
  if (menuTimer) {
    clearTimeout(menuTimer)
  }
  activeMenuSongId.value = song.id
}

// 隐藏添加菜单
function hideAddMenu() {
  menuTimer = setTimeout(() => {
    activeMenuSongId.value = null
  }, 200)
}

// 添加到播放列表
function addToQueue(song) {
  activeMenuSongId.value = null
  if (window.addToQueue) {
    window.addToQueue(song)
    toast.success('已添加到播放列表')
  } else {
    toast.warning('播放器未就绪')
  }
}

// 打开添加到歌单弹窗
async function addToPlaylist(song) {
  activeMenuSongId.value = null
  
  // 检查是否登录
  const token = localStorage.getItem('access_token')
  if (!token) {
    toast.warning('请先登录')
    return
  }
  
  selectedSong.value = song
  showPlaylistModal.value = true
  
  // 加载用户的歌单
  await loadMyPlaylists()
}

// 加载我的歌单
async function loadMyPlaylists() {
  loadingPlaylists.value = true
  try {
    const response = await playlistAPI.getMyPlaylists()
    myPlaylists.value = response.playlists || []
  } catch (error) {
    console.error('加载歌单失败:', error)
    toast.error('加载歌单失败')
  } finally {
    loadingPlaylists.value = false
  }
}

// 添加歌曲到指定歌单
async function addSongToPlaylist(playlistId) {
  try {
    await playlistAPI.addSongToPlaylist(playlistId, selectedSong.value.id)
    
    // 更新歌单的歌曲数量
    const playlist = myPlaylists.value.find(p => p.id === playlistId)
    if (playlist) {
      playlist.song_count = (playlist.song_count || 0) + 1
      toast.success(`已添加到《${playlist.name}》`)
    } else {
      toast.success(`已添加到歌单`)
    }
    
    showPlaylistModal.value = false
  } catch (error) {
    console.error('添加失败:', error)
    toast.error(error.message || '添加失败')
  }
}

// 上一页
function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    if (searchKeyword.value) {
      searchSongs()
    } else {
      fetchSongs()
    }
  }
}

// 下一页
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    if (searchKeyword.value) {
      searchSongs()
    } else {
      fetchSongs()
    }
  }
}

// 监听路由变化
watch(() => route.query.keyword, (newKeyword) => {
  if (newKeyword) {
    searchKeyword.value = newKeyword
    currentPage.value = 1
    searchSongs()
  }
})

// 页面加载时获取歌曲
onMounted(() => {
  // 加载搜索历史
  searchHistory.value = getSearchHistory()
  
  // 检查URL参数中是否有搜索关键词
  if (route.query.keyword) {
    searchKeyword.value = route.query.keyword
    searchSongs()
  } else {
    fetchSongs()
  }
})
</script>

<style scoped>
.songs-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: grid;
  grid-template-columns: 1fr auto 1fr; /* 三列布局 */
  align-items: center;
  margin-bottom: 32px;
  gap: 20px;
}

.header-left {
  grid-column: 2; /* 标题区域在中间列 */
  justify-self: center; /* 自身居中 */
  text-align: center; /* 文字居中 */
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px 0;
}

.search-info {
  font-size: 14px;
  color: #666;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.clear-search-btn {
  padding: 4px 12px;
  background: #f5f5f5;
  border: none;
  border-radius: 16px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 4px;
}

.clear-search-btn:hover {
  background: #e0e0e0;
  color: #333;
}

.search-box {
  grid-column: 3; /* 搜索框在第三列 */
  justify-self: end; /* 自身右对齐 */
}

.search-input-wrapper {
  display: flex;
  gap: 8px;
  position: relative;
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
  border-color: #667eea;
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
  flex-shrink: 0;
}

.search-btn:hover {
  transform: scale(1.05);
}

/* 搜索历史下拉 */
.search-history-dropdown {
  position: absolute;
  top: 52px;
  left: 0;
  width: 300px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 100;
  animation: slideDown 0.2s ease;
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

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 13px;
  color: #666;
  font-weight: 600;
}

.clear-history-btn {
  background: transparent;
  border: none;
  color: #999;
  font-size: 14px;
  cursor: pointer;
  padding: 4px;
  transition: all 0.3s;
}

.clear-history-btn:hover {
  color: #ff4444;
}

.history-list {
  max-height: 300px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  color: #333;
}

.history-item:hover {
  background: #f8f9fa;
}

.history-item i:first-child {
  color: #999;
  font-size: 16px;
}

.history-item span {
  flex: 1;
}

.delete-item-btn {
  background: transparent;
  border: none;
  color: #999;
  font-size: 14px;
  cursor: pointer;
  padding: 4px;
  opacity: 0;
  transition: all 0.3s;
}

.history-item:hover .delete-item-btn {
  opacity: 1;
}

.delete-item-btn:hover {
  color: #ff4444;
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

/* 歌曲列表 */
.songs-list {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.song-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  gap: 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s;
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
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: transparent;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background: #f0f0f0;
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

  .search-input {
    width: 100%;
  }

  .song-album {
    display: none;
  }

  .song-actions {
    display: none;
  }
}

/* 添加到歌单弹窗 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
  max-width: 90%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.playlist-modal {
  width: 600px;
  max-width: 90vw;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: #999;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #333;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  max-height: calc(90vh - 80px);
}

.selected-song {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.selected-song .song-thumb {
  width: 50px;
  height: 50px;
  border-radius: 6px;
  object-fit: cover;
}

.selected-song .song-info {
  flex: 1;
}

.selected-song .song-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.selected-song .song-artist {
  font-size: 13px;
  color: #666;
}

.playlist-list {
  min-height: 200px;
}

.loading-text {
  text-align: center;
  padding: 40px;
  color: #999;
}

.empty-playlists {
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 64px;
  color: #ddd;
  margin-bottom: 16px;
}

.empty-playlists p {
  color: #999;
  margin: 8px 0;
}

.empty-hint {
  font-size: 13px;
  color: #bbb;
}

.playlists-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.playlist-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 2px solid #f0f0f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.playlist-item:hover {
  border-color: #64AEC2;
  background: #f8fdff;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(100, 174, 194, 0.15);
}

.playlist-cover {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.playlist-item .playlist-info {
  flex: 1;
  min-width: 0;
}

.playlist-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.playlist-count {
  font-size: 13px;
  color: #999;
}

.add-icon {
  font-size: 24px;
  color: #64AEC2;
  flex-shrink: 0;
  transition: all 0.3s;
}

.playlist-item:hover .add-icon {
  transform: scale(1.2) rotate(90deg);
  color: #4a9eb0;
}

/* 歌曲操作按钮 */
.song-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.add-menu-wrapper {
  position: relative;
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

/* 添加菜单 */
.add-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 100;
  min-width: 180px;
  animation: menuSlideIn 0.2s ease;
}

@keyframes menuSlideIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  color: #333;
  white-space: nowrap;
}

.menu-item:hover {
  background: #f8f9fa;
}

.menu-item i {
  font-size: 18px;
  color: #64AEC2;
  flex-shrink: 0;
}

.menu-item span {
  flex: 1;
}

.menu-item:first-child {
  border-bottom: 1px solid #f0f0f0;
}
</style>
