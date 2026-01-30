<template>
  <div class="playlist-detail-container">
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else-if="playlist" class="playlist-detail">
      <!-- 歌单头部 -->
      <div class="playlist-header">
        <div class="cover-section">
          <img :src="playlist.cover || defaultCover" :alt="playlist.name" class="playlist-cover" />
        </div>
        
        <div class="info-section">
          <h1 class="playlist-name">{{ playlist.name }}</h1>
          
          <div class="playlist-meta">
            <span class="creator">
              <i class="ri-user-line creator-avatar"></i>
              {{ playlist.creator }}
            </span>
            <span class="divider">·</span>
            <span class="create-time">{{ formatDate(playlist.created_at) }}</span>
          </div>
          
          <div class="playlist-stats">
            <span class="stat-item">
              <i class="ri-music-2-line stat-icon"></i>
              {{ playlist.song_count || 0 }} 首歌曲
            </span>
            <span class="divider">·</span>
            <span class="stat-item">
              <i class="ri-play-circle-line stat-icon"></i>
              {{ playlist.play_count || 0 }} 次播放
            </span>
          </div>
          
          <div class="playlist-description" v-if="playlist.description">
            {{ playlist.description }}
          </div>
          
          <div class="action-buttons">
            <button class="btn-primary" @click="playAll">
              <i class="ri-play-fill btn-icon"></i>
              播放全部
            </button>
            <button class="btn-secondary" @click="collectPlaylist" :class="{ collected: isCollected }">
              <i :class="isCollected ? 'ri-star-fill' : 'ri-star-line'" class="btn-icon"></i>
              {{ isCollected ? '已收藏' : '收藏' }}
            </button>
            <button class="btn-secondary" @click="showAddSongModal = true" v-if="isOwner">
              <i class="ri-add-line btn-icon"></i>
              添加歌曲
            </button>
            <button class="btn-secondary" @click="editPlaylist" v-if="isOwner">
              <i class="ri-edit-line btn-icon"></i>
              编辑
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
          <i class="ri-music-2-line empty-icon"></i>
          <div class="empty-text">歌单还没有歌曲</div>
          <button class="empty-btn" @click="showAddSongModal = true">添加歌曲</button>
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
              <img :src="song.cover_image || defaultCover" :alt="song.title" class="song-cover" />
              <span class="song-title">{{ song.title }}</span>
            </div>
            <div class="col-artist">{{ song.artist }}</div>
            <div class="col-album">{{ song.album || '-' }}</div>
            <div class="col-duration">{{ formatDuration(song.duration) }}</div>
            <div class="col-actions">
              <button class="action-btn" @click="playSong(song)" title="播放">
                <i class="ri-play-fill"></i>
              </button>
              <FavoriteButton :song-id="song.id" />
              <button class="action-btn" @click="removeSong(song.id)" title="移除">
                <i class="ri-delete-bin-line"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 编辑歌单弹窗 -->
    <div class="modal" v-if="showEditModal" @click="showEditModal = false">
      <div class="modal-content edit-modal" @click.stop>
        <div class="modal-header">
          <h3>编辑歌单</h3>
          <button class="close-btn" @click="showEditModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        
        <div class="form-group">
          <label>歌单名称</label>
          <input 
            v-model="editForm.name" 
            type="text" 
            placeholder="歌单名称"
            maxlength="50"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label>歌单描述</label>
          <textarea 
            v-model="editForm.description" 
            placeholder="介绍一下这个歌单吧（可选）"
            maxlength="200"
            rows="4"
            class="form-textarea"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label>封面图片URL（可选）</label>
          <input 
            v-model="editForm.cover" 
            type="text" 
            placeholder="https://..."
            class="form-input"
          />
          <div v-if="editForm.cover" class="cover-preview">
            <img :src="editForm.cover" alt="封面预览" @error="editForm.cover = ''" />
          </div>
        </div>
        
        <!-- 新增：歌单设置 -->
        <div class="form-group">
          <label>歌单分类</label>
          <select v-model="editForm.category" class="form-select">
            <option value="为你推荐">为你推荐</option>
            <option value="情歌">情歌</option>
            <option value="网络歌曲">网络歌曲</option>
            <option value="官方歌单">官方歌单</option>
            <option value="经典">经典</option>
          </select>
        </div>
        
        <div class="form-group">
          <label class="checkbox-label">
            <input 
              type="checkbox" 
              v-model="editForm.is_public"
              class="form-checkbox"
            />
            <span>公开歌单（其他用户可以在主页看到）</span>
          </label>
        </div>
        
        <div class="modal-actions">
          <button class="btn-cancel" @click="showEditModal = false">取消</button>
          <button class="btn-save" @click="saveEdit" :disabled="loading">
            {{ loading ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 添加歌曲弹窗 -->
    <div class="modal" v-if="showAddSongModal" @click="showAddSongModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>添加歌曲到歌单</h3>
          <button class="close-btn" @click="showAddSongModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        
        <div class="search-box">
          <input 
            v-model="searchKeyword" 
            type="text" 
            placeholder="搜索歌曲..."
            class="search-input"
            @input="searchSongs"
          />
        </div>
        
        <div class="available-songs">
          <div v-if="loadingSongs" class="loading-text">搜索中...</div>
          <div v-else-if="availableSongs.length === 0" class="empty-text">
            {{ searchKeyword ? '没有找到相关歌曲' : '输入关键词搜索歌曲' }}
          </div>
          <div v-else class="song-list-modal">
            <div 
              v-for="song in availableSongs" 
              :key="song.id"
              class="song-item-modal"
              @click="addSongToPlaylist(song.id)"
            >
              <img :src="song.cover_image || defaultCover" :alt="song.title" class="song-cover-small" />
              <div class="song-info-modal">
                <div class="song-title-modal">{{ song.title }}</div>
                <div class="song-artist-modal">{{ song.artist }}</div>
              </div>
              <button class="btn-add">
                <i class="ri-add-line"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { playlistAPI, songAPI } from '../utils/api'
import FavoriteButton from '../components/FavoriteButton.vue'
import daitu1 from '../assets/daitu1.jpg'

const route = useRoute()
const router = useRouter()

const playlist = ref(null)
const songs = ref([])
const loading = ref(true)
const showAddSongModal = ref(false)
const showEditModal = ref(false)
const searchKeyword = ref('')
const availableSongs = ref([])
const loadingSongs = ref(false)
const defaultCover = daitu1
const isCollected = ref(false)
const isOwner = ref(false)

// 编辑表单
const editForm = reactive({
  name: '',
  description: '',
  cover: '',
  category: '为你推荐',
  is_public: true
})

// 加载歌单详情
async function loadPlaylistDetail() {
  loading.value = true
  try {
    const playlistId = route.params.id
    const response = await playlistAPI.getPlaylist(playlistId)
    playlist.value = response.playlist
    songs.value = response.songs || []
    
    // 检查是否是歌单所有者
    const currentUser = JSON.parse(localStorage.getItem('user') || '{}')
    isOwner.value = currentUser.id === playlist.value.user_id
    
    // 检查是否已收藏
    await checkCollected()
  } catch (error) {
    console.error('加载歌单失败:', error)
    alert('加载歌单失败：' + error.message)
    router.push('/mine')
  } finally {
    loading.value = false
  }
}

// 检查是否已收藏
async function checkCollected() {
  try {
    const playlistId = route.params.id
    const response = await playlistAPI.checkPlaylistCollected(playlistId)
    isCollected.value = response.is_collected
  } catch (error) {
    console.error('检查收藏状态失败:', error)
  }
}

// 收藏/取消收藏歌单
async function collectPlaylist() {
  try {
    const playlistId = route.params.id
    if (isCollected.value) {
      await playlistAPI.uncollectPlaylist(playlistId)
      isCollected.value = false
      alert('已取消收藏')
    } else {
      await playlistAPI.collectPlaylist(playlistId)
      isCollected.value = true
      alert('收藏成功')
    }
  } catch (error) {
    console.error('收藏操作失败:', error)
    alert('操作失败：' + error.message)
  }
}

// 搜索歌曲
let searchTimer = null
async function searchSongs() {
  if (!searchKeyword.value.trim()) {
    availableSongs.value = []
    return
  }
  
  clearTimeout(searchTimer)
  searchTimer = setTimeout(async () => {
    loadingSongs.value = true
    try {
      const response = await songAPI.searchSongs(searchKeyword.value)
      availableSongs.value = response.songs || []
    } catch (error) {
      console.error('搜索歌曲失败:', error)
    } finally {
      loadingSongs.value = false
    }
  }, 500)
}

// 添加歌曲到歌单
async function addSongToPlaylist(songId) {
  try {
    await playlistAPI.addSongToPlaylist(playlist.value.id, songId)
    alert('添加成功！')
    showAddSongModal.value = false
    searchKeyword.value = ''
    availableSongs.value = []
    // 重新加载歌单
    await loadPlaylistDetail()
  } catch (error) {
    console.error('添加歌曲失败:', error)
    alert('添加失败：' + error.message)
  }
}

// 移除歌曲
async function removeSong(songId) {
  if (!confirm('确定要从歌单中移除这首歌吗？')) {
    return
  }
  
  try {
    await playlistAPI.removeSongFromPlaylist(playlist.value.id, songId)
    alert('移除成功！')
    // 重新加载歌单
    await loadPlaylistDetail()
  } catch (error) {
    console.error('移除歌曲失败:', error)
    alert('移除失败：' + error.message)
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
    toast.warning('歌单中还没有歌曲')
    return
  }
  
  // 先播放第一首
  if (window.playSong) {
    window.playSong(songs.value[0])
  }
  
  // 将剩余歌曲添加到播放队列
  if (window.addToQueue && songs.value.length > 1) {
    let addedCount = 0
    for (let i = 1; i < songs.value.length; i++) {
      const success = window.addToQueue(songs.value[i])
      if (success) addedCount++
    }
    toast.success(`已添加 ${songs.value.length} 首歌曲到播放列表`)
  } else if (songs.value.length === 1) {
    toast.success('正在播放')
  }
}

// 编辑歌单
function editPlaylist() {
  editForm.name = playlist.value.name
  editForm.description = playlist.value.description || ''
  editForm.cover = playlist.value.cover || ''
  editForm.category = playlist.value.category || '为你推荐'
  editForm.is_public = playlist.value.is_public !== false // 默认为 true
  showEditModal.value = true
}

// 格式化时长
function formatDuration(seconds) {
  if (!seconds) return '--:--'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 格式化日期
function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

// 保存编辑
async function saveEdit() {
  if (!editForm.name.trim()) {
    toast.warning('歌单名称不能为空')
    return
  }
  
  loading.value = true
  try {
    // 更新基本信息
    const response = await playlistAPI.updatePlaylist(playlist.value.id, {
      name: editForm.name,
      description: editForm.description,
      cover: editForm.cover
    })
    
    // 更新设置（分类和公开状态）
    await playlistAPI.updateSettings(playlist.value.id, {
      category: editForm.category,
      is_public: editForm.is_public
    })
    
    if (response.playlist) {
      toast.success('更新成功！')
      showEditModal.value = false
      // 重新加载歌单
      await loadPlaylistDetail()
    }
  } catch (error) {
    console.error('更新歌单失败:', error)
    toast.error('更新失败：' + error.message)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPlaylistDetail()
})
</script>

<style scoped>
.playlist-detail-container {
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

/* 歌单头部 */
.playlist-header {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
  padding: 30px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.cover-section {
  flex-shrink: 0;
}

.playlist-cover {
  width: 200px;
  height: 200px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
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
  background: #64AEC2;
  color: white;
  border-radius: 12px;
  font-size: 12px;
  margin-bottom: 12px;
  width: fit-content;
}

.playlist-name {
  font-size: 32px;
  font-weight: bold;
  margin: 0 0 16px 0;
  color: #333;
}

.playlist-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #666;
}

.creator {
  display: flex;
  align-items: center;
  gap: 6px;
}

.creator-avatar {
  font-size: 16px;
}

.divider {
  opacity: 0.5;
}

.playlist-stats {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #666;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-icon {
  font-size: 12px;
  color: #64AEC2;
}

.playlist-description {
  margin-bottom: 20px;
  color: #666;
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.btn-primary,
.btn-secondary {
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
}

.btn-primary {
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: white;
  color: #333;
  border: 1px solid #e0e0e0;
}

.btn-secondary:hover {
  background: #f5f5f5;
  border-color: #64AEC2;
  color: #64AEC2;
}

.btn-secondary.collected {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: white;
}

.btn-secondary.collected:hover {
  background: linear-gradient(135deg, #FFA500, #FF8C00);
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
  font-size: 72px;
  margin-bottom: 16px;
  opacity: 0.2;
  color: #999;
}

.empty-text {
  color: #999;
  font-size: 15px;
  margin-bottom: 20px;
}

.empty-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.empty-btn:hover {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
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

/* 添加歌曲弹窗 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 24px;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  color: #333;
  font-size: 18px;
  margin: 0;
}

.close-btn {
  background: transparent;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 24px;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #333;
}

.search-box {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.available-songs {
  flex: 1;
  overflow-y: auto;
  min-height: 300px;
}

.loading-text,
.empty-text {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-size: 14px;
}

.song-list-modal {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.song-item-modal {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.song-item-modal:hover {
  background: #f5f5f5;
}

.song-cover-small {
  width: 48px;
  height: 48px;
  border-radius: 4px;
  object-fit: cover;
}

.song-info-modal {
  flex: 1;
}

.song-title-modal {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.song-artist-modal {
  font-size: 13px;
  color: #999;
}

.btn-add {
  background: #667eea;
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-add:hover {
  background: #5568d3;
  transform: scale(1.1);
}

/* 编辑歌单弹窗 */
.edit-modal {
  max-width: 520px;
  padding: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group:last-of-type {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  color: #333;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 6px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
  color: #333;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-textarea {
  resize: vertical;
  min-height: 70px;
  font-family: inherit;
}

.form-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
  color: #333;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-select:focus {
  outline: none;
  border-color: #667eea;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.form-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-label span {
  font-size: 14px;
  color: #666;
}

.cover-preview {
  margin-top: 8px;
  border-radius: 6px;
  overflow: hidden;
  max-width: 150px;
}

.cover-preview img {
  width: 100%;
  height: auto;
  display: block;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.btn-cancel,
.btn-save {
  flex: 0 0 auto;
  min-width: 90px;
  padding: 10px 24px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.btn-cancel {
  background: #f5f5f5;
  color: #666;
  border: 2px solid #e0e0e0;
}

.btn-cancel:hover {
  background: #e8e8e8;
  border-color: #d0d0d0;
  transform: translateY(-1px);
}

.btn-save {
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(100, 174, 194, 0.3);
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.4);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
</style>
