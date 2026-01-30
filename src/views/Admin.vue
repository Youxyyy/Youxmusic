<template>
  <div class="admin-page">
    <!-- 权限检查 -->
    <div v-if="loading" class="loading">检查权限中...</div>
    
    <div v-else-if="!isAdmin" class="no-permission">
      <div class="no-permission-icon">🔒</div>
      <h2>无权限访问</h2>
      <p>此页面仅限管理员访问</p>
      <button @click="goHome" class="btn-back">返回首页</button>
    </div>
    
    <!-- 管理员界面 -->
    <div v-else class="admin-content">
      <!-- 头部 -->
      <div class="admin-header">
        <h1>管理员后台</h1>
        <div class="admin-user">
          <span><i class="ri-user-line"></i> {{ username }}</span>
          <span class="admin-badge">管理员</span>
        </div>
      </div>
      
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="ri-music-2-line"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.songs_count }}</div>
            <div class="stat-label">歌曲总数</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">👥</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.users_count }}</div>
            <div class="stat-label">用户总数</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <i class="ri-user-voice-line"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_singers || 0 }}</div>
            <div class="stat-label">歌手总数</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📁</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.playlists_count }}</div>
            <div class="stat-label">歌单总数</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <i class="ri-play-circle-line"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ formatNumber(stats.total_plays) }}</div>
            <div class="stat-label">总播放次数</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <i class="ri-heart-line"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_favorites || 0 }}</div>
            <div class="stat-label">总收藏数</div>
          </div>
        </div>
      </div>

      <!-- 标签页 -->
      <div class="tabs">
        <button 
          :class="['tab-btn', { active: currentTab === 'upload' }]"
          @click="currentTab = 'upload'"
        >
          <i class="ri-add-line"></i> 上传歌曲
        </button>
        <button 
          :class="['tab-btn', { active: currentTab === 'manage' }]"
          @click="currentTab = 'manage'"
        >
          <i class="ri-music-line"></i> 管理歌曲
        </button>
        <button 
          :class="['tab-btn', { active: currentTab === 'singers' }]"
          @click="switchToSingersTab"
        >
          <i class="ri-user-voice-line"></i> 歌手管理
        </button>
        <button 
          :class="['tab-btn', { active: currentTab === 'users' }]"
          @click="switchToUsersTab"
        >
          <i class="ri-user-line"></i> 用户管理
        </button>
        <button 
          :class="['tab-btn', { active: currentTab === 'playlists' }]"
          @click="currentTab = 'playlists'"
        >
          <i class="ri-list-check"></i> 管理歌单
        </button>
      </div>
      
      <!-- 上传歌曲 -->
      <div v-if="currentTab === 'upload'" class="upload-section">
        <div class="upload-card">
          <h2>上传新歌曲</h2>
          
          <form @submit.prevent="uploadSong" class="upload-form">
            <div class="form-row">
              <div class="form-group">
                <label>歌曲名称 *</label>
                <input v-model="uploadForm.title" type="text" required placeholder="请输入歌曲名称" />
              </div>
              <div class="form-group">
                <label>歌手 *</label>
                <input v-model="uploadForm.artist" type="text" required placeholder="请输入歌手名称" />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>专辑</label>
                <input v-model="uploadForm.album" type="text" placeholder="请输入专辑名称" />
              </div>
              <div class="form-group">
                <label>时长（秒）</label>
                <input v-model="uploadForm.duration" type="number" placeholder="例如：180" />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>音乐类型</label>
                <input v-model="uploadForm.genre" type="text" placeholder="例如：流行、摇滚" />
              </div>
              <div class="form-group">
                <label>发行年份</label>
                <input v-model="uploadForm.release_year" type="number" placeholder="例如：2024" />
              </div>
            </div>
            
            <div class="form-group">
              <label>音频文件 *</label>
              <input type="file" @change="handleAudioFile" accept=".mp3,.wav,.flac,.m4a" required />
              <div v-if="uploadForm.audioFile" class="file-info">
                ✓ {{ uploadForm.audioFile.name }}
              </div>
            </div>
            
            <div class="form-group">
              <label>封面图片</label>
              <input type="file" @change="handleCoverFile" accept="image/*" />
              <div v-if="uploadForm.coverFile" class="file-info">
                ✓ {{ uploadForm.coverFile.name }}
              </div>
            </div>
            
            <button type="submit" class="btn-upload" :disabled="uploading">
              {{ uploading ? '上传中...' : '上传歌曲' }}
            </button>
          </form>
        </div>
      </div>

      <!-- 管理歌曲 -->
      <div v-if="currentTab === 'manage'" class="manage-section">
        <div class="manage-header">
          <h2>歌曲列表</h2>
          <div class="search-box">
            <input v-model="searchKeyword" type="text" placeholder="搜索歌曲..." />
          </div>
        </div>
        
        <div v-if="loadingSongs" class="loading">加载中...</div>
        
        <div v-else class="songs-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>封面</th>
                <th>歌曲名</th>
                <th>歌手</th>
                <th>专辑</th>
                <th>时长</th>
                <th>播放次数</th>
                <th>推荐歌曲</th>
                <th>大家都在听</th>
                <th>新歌</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="song in filteredSongs" :key="song.id">
                <td>{{ song.id }}</td>
                <td>
                  <img :src="getCoverUrl(song)" class="song-thumb" />
                </td>
                <td>{{ song.title }}</td>
                <td>{{ song.artist }}</td>
                <td>{{ song.album || '-' }}</td>
                <td>{{ formatDuration(song.duration) }}</td>
                <td>{{ song.play_count || 0 }}</td>
                <td>
                  <button 
                    @click="toggleSongRecommended(song)" 
                    :class="['btn-recommended', { active: song.is_recommended }]"
                  >
                    {{ song.is_recommended ? '✓' : '推荐' }}
                  </button>
                </td>
                <td>
                  <button 
                    @click="toggleSongFeatured(song)" 
                    :class="['btn-feature', { active: song.is_featured }]"
                  >
                    {{ song.is_featured ? '✓' : '推荐' }}
                  </button>
                </td>
                <td>
                  <button 
                    @click="toggleSongNew(song)" 
                    :class="['btn-new', { active: song.is_new }]"
                  >
                    {{ song.is_new ? '✓' : '新歌' }}
                  </button>
                </td>
                <td>
                  <button @click="editSong(song)" class="btn-edit">编辑</button>
                  <button @click="deleteSongConfirm(song)" class="btn-delete">删除</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- 分页 -->
        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
          <span>第 {{ currentPage }} 页</span>
          <button @click="nextPage">下一页</button>
        </div>
      </div>
      
      <!-- 管理歌单 -->
      <div v-if="currentTab === 'playlists'" class="manage-section">
        <div class="manage-header">
          <h2>歌单管理</h2>
          <div class="search-box">
            <input v-model="playlistSearchKeyword" type="text" placeholder="搜索歌单..." />
          </div>
        </div>
        
        <div v-if="loadingPlaylists" class="loading">加载中...</div>
        
        <div v-else class="playlists-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>封面</th>
                <th>歌单名</th>
                <th>创建者</th>
                <th>分类</th>
                <th>歌曲数</th>
                <th>播放次数</th>
                <th>公开</th>
                <th>首页推荐</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="playlist in filteredPlaylists" :key="playlist.id">
                <td>{{ playlist.id }}</td>
                <td>
                  <img :src="getPlaylistCover(playlist)" class="song-thumb" />
                </td>
                <td>{{ playlist.name }}</td>
                <td>{{ playlist.creator }}</td>
                <td>
                  <span class="category-badge">{{ playlist.category || '未分类' }}</span>
                </td>
                <td>{{ playlist.song_count || 0 }}</td>
                <td>{{ playlist.play_count || 0 }}</td>
                <td>
                  <span :class="['status-badge', playlist.is_public ? 'public' : 'private']">
                    {{ playlist.is_public ? '公开' : '私密' }}
                  </span>
                </td>
                <td>
                  <button 
                    @click="toggleFeatured(playlist)" 
                    :class="['btn-featured', { active: playlist.is_featured }]"
                  >
                    {{ playlist.is_featured ? '✓ 已推荐' : '推荐到首页' }}
                  </button>
                </td>
                <td>
                  <button @click="viewPlaylist(playlist)" class="btn-view">查看</button>
                  <button @click="deletePlaylistConfirm(playlist)" class="btn-delete">删除</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="!loadingPlaylists && filteredPlaylists.length === 0" class="empty-state">
          <i class="ri-folder-music-line empty-icon"></i>
          <p>暂无歌单</p>
        </div>
        
        <!-- 歌单分页 -->
        <div v-if="!loadingPlaylists && allPlaylists.length > 0" class="pagination">
          <button @click="playlistPrevPage" :disabled="playlistCurrentPage === 1">上一页</button>
          <span>第 {{ playlistCurrentPage }} / {{ playlistTotalPages }} 页</span>
          <button @click="playlistNextPage" :disabled="playlistCurrentPage >= playlistTotalPages">下一页</button>
        </div>
      </div>

      <!-- 歌手管理 -->
      <div v-if="currentTab === 'singers'" class="manage-section">
        <div class="manage-header">
          <h2>歌手管理</h2>
          <div class="header-actions">
            <input v-model="singerSearchKeyword" type="text" placeholder="搜索歌手..." class="search-input" />
            <button @click="showAddSingerModal = true" class="btn-add">
              <i class="ri-add-line"></i> 添加歌手
            </button>
          </div>
        </div>

        <div v-if="loadingSingers" class="loading">加载中...</div>
        
        <div v-else-if="filteredSingers.length === 0" class="empty-state">
          <i class="ri-user-voice-line empty-icon"></i>
          <p>暂无歌手数据</p>
        </div>
        
        <div v-else class="singers-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>头像</th>
                <th>歌手名称</th>
                <th>国家/地区</th>
                <th>流派</th>
                <th>歌曲数量</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="singer in filteredSingers" :key="singer.id">
                <td>{{ singer.id }}</td>
                <td>
                  <img :src="getSingerAvatar(singer.avatar)" class="singer-avatar-small" @error="handleSingerImageError" />
                </td>
                <td class="singer-name">{{ singer.name }}</td>
                <td>{{ singer.country }}</td>
                <td>{{ singer.genre }}</td>
                <td>{{ singer.song_count || 0 }} 首</td>
                <td class="actions">
                  <button @click="editSingerAction(singer)" class="btn-edit" title="编辑">
                    <i class="ri-edit-line"></i>
                  </button>
                  <button @click="deleteSingerAction(singer)" class="btn-delete" title="删除">
                    <i class="ri-delete-bin-line"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 用户管理 -->
      <div v-if="currentTab === 'users'" class="manage-section">
        <div class="manage-header">
          <h2>用户管理</h2>
          <div class="header-actions">
            <input v-model="userSearchKeyword" type="text" placeholder="搜索用户..." class="search-input" />
          </div>
        </div>

        <div v-if="loadingUsers" class="loading">加载中...</div>
        
        <div v-else-if="filteredUsers.length === 0" class="empty-state">
          <i class="ri-user-line empty-icon"></i>
          <p>暂无用户数据</p>
        </div>
        
        <div v-else class="users-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>用户名</th>
                <th>邮箱</th>
                <th>权限</th>
                <th>歌单数</th>
                <th>收藏数</th>
                <th>注册时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td>{{ user.id }}</td>
                <td class="username">{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span :class="['user-role', { admin: user.is_admin }]">
                    {{ user.is_admin ? '管理员' : '普通用户' }}
                  </span>
                </td>
                <td>{{ user.playlist_count || 0 }}</td>
                <td>{{ user.favorite_count || 0 }}</td>
                <td>{{ formatDate(user.created_at) }}</td>
                <td class="actions">
                  <button @click="toggleUserAdminAction(user)" class="btn-admin" :title="user.is_admin ? '取消管理员' : '设为管理员'">
                    <i :class="user.is_admin ? 'ri-admin-line' : 'ri-user-add-line'"></i>
                  </button>
                  <button @click="deleteUserAction(user)" class="btn-delete" title="删除用户">
                    <i class="ri-delete-bin-line"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    
    <!-- 编辑歌曲弹窗 -->
    <div v-if="showEditModal" class="modal" @click="showEditModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>编辑歌曲</h3>
          <button class="close-btn" @click="showEditModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <form @submit.prevent="updateSong" class="edit-form">
          <div class="form-group">
            <label>歌曲名称</label>
            <input v-model="editForm.title" type="text" required />
          </div>
          <div class="form-group">
            <label>歌手</label>
            <input v-model="editForm.artist" type="text" required />
          </div>
          <div class="form-group">
            <label>专辑</label>
            <input v-model="editForm.album" type="text" />
          </div>
          <div class="form-group">
            <label>时长（秒）</label>
            <input v-model="editForm.duration" type="number" />
          </div>
          <div class="modal-actions">
            <button type="button" @click="showEditModal = false" class="btn-cancel">取消</button>
            <button type="submit" class="btn-save">保存</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 添加/编辑歌手模态框 -->
    <div v-if="showAddSingerModal || showEditSingerModal" class="modal" @click="closeSingerModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ showEditSingerModal ? '编辑歌手' : '添加歌手' }}</h3>
          <button class="close-btn" @click="closeSingerModal">
            <i class="ri-close-line"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="saveSinger">
            <div class="form-group">
              <label>歌手名称 *</label>
              <input v-model="singerForm.name" type="text" required placeholder="请输入歌手名称" />
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>国家/地区</label>
                <select v-model="singerForm.country">
                  <option value="中国">中国</option>
                  <option value="美国">美国</option>
                  <option value="英国">英国</option>
                  <option value="日本">日本</option>
                  <option value="韩国">韩国</option>
                  <option value="新加坡">新加坡</option>
                  <option value="其他">其他</option>
                </select>
              </div>
              
              <div class="form-group">
                <label>音乐流派</label>
                <select v-model="singerForm.genre">
                  <option value="流行">流行</option>
                  <option value="摇滚">摇滚</option>
                  <option value="民谣">民谣</option>
                  <option value="电子">电子</option>
                  <option value="R&B">R&B</option>
                  <option value="嘻哈">嘻哈</option>
                  <option value="古典">古典</option>
                  <option value="爵士">爵士</option>
                </select>
              </div>
            </div>
            
            <div class="form-group">
              <label>简介</label>
              <textarea v-model="singerForm.bio" rows="4" placeholder="请输入歌手简介"></textarea>
            </div>
            
            <div class="form-group">
              <label>头像URL</label>
              <input v-model="singerForm.avatar" type="text" placeholder="请输入头像图片URL" />
            </div>
            
            <div class="modal-actions">
              <button type="button" @click="closeSingerModal" class="btn-cancel">取消</button>
              <button type="submit" class="btn-save">{{ showEditSingerModal ? '保存' : '添加' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, reactive, computed, onMounted, inject, watch } from 'vue'
import { useRouter } from 'vue-router'
import { adminAPI, playlistAPI } from '../utils/api'
import daitu1 from '../assets/daitu1.jpg'

const router = useRouter()
const toast = inject('toast')
const loading = ref(true)
const isAdmin = ref(false)
const username = ref('')
const currentTab = ref('upload')
const uploading = ref(false)
const loadingSongs = ref(false)
const searchKeyword = ref('')
const currentPage = ref(1)
const showEditModal = ref(false)

// 歌单管理相关
const loadingPlaylists = ref(false)
const playlistSearchKeyword = ref('')
const allPlaylists = ref([])
const playlistCurrentPage = ref(1)
const playlistPerPage = 10

// 歌手管理相关
const loadingSingers = ref(false)
const singerSearchKeyword = ref('')
const singers = ref([])
const showAddSingerModal = ref(false)
const showEditSingerModal = ref(false)

// 用户管理相关
const loadingUsers = ref(false)
const userSearchKeyword = ref('')
const users = ref([])

const stats = reactive({
  songs_count: 0,
  users_count: 0,
  playlists_count: 0,
  total_plays: 0,
  total_singers: 0,
  total_favorites: 0
})

const uploadForm = reactive({
  title: '',
  artist: '',
  album: '',
  duration: '',
  genre: '',
  release_year: '',
  audioFile: null,
  coverFile: null
})

const editForm = reactive({
  id: null,
  title: '',
  artist: '',
  album: '',
  duration: ''
})

const singerForm = reactive({
  id: null,
  name: '',
  country: '中国',
  genre: '流行',
  bio: '',
  avatar: ''
})

const songs = ref([])

// 检查管理员权限
async function checkAdminPermission() {
  loading.value = true
  try {
    const response = await adminAPI.checkAdmin()
    isAdmin.value = response.is_admin
    username.value = response.username
    
    if (isAdmin.value) {
      await loadStats()
      await loadSongs()
    }
  } catch (error) {
    console.error('检查权限失败:', error)
    isAdmin.value = false
  } finally {
    loading.value = false
  }
}

// 加载统计信息
async function loadStats() {
  try {
    const response = await adminAPI.getStats()
    Object.assign(stats, response)
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

// 加载歌曲列表
async function loadSongs() {
  loadingSongs.value = true
  try {
    const response = await adminAPI.getAllSongs(currentPage.value, 10)
    songs.value = response.songs || []
  } catch (error) {
    console.error('加载歌曲失败:', error)
  } finally {
    loadingSongs.value = false
  }
}

// 处理音频文件
function handleAudioFile(event) {
  uploadForm.audioFile = event.target.files[0]
}

// 处理封面文件
function handleCoverFile(event) {
  uploadForm.coverFile = event.target.files[0]
}

// 上传歌曲
async function uploadSong() {
  if (!uploadForm.audioFile) {
    alert('请选择音频文件')
    return
  }
  
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('title', uploadForm.title)
    formData.append('artist', uploadForm.artist)
    formData.append('album', uploadForm.album)
    formData.append('duration', uploadForm.duration || 0)
    formData.append('genre', uploadForm.genre)
    formData.append('release_year', uploadForm.release_year || '')
    formData.append('audio_file', uploadForm.audioFile)
    if (uploadForm.coverFile) {
      formData.append('cover_file', uploadForm.coverFile)
    }
    
    const response = await adminAPI.uploadSong(formData)
    
    if (response.message) {
      alert('上传成功！')
      // 重置表单
      Object.assign(uploadForm, {
        title: '',
        artist: '',
        album: '',
        duration: '',
        genre: '',
        release_year: '',
        audioFile: null,
        coverFile: null
      })
      // 重新加载
      await loadStats()
      await loadSongs()
    } else {
      alert('上传失败：' + (response.error || '未知错误'))
    }
  } catch (error) {
    console.error('上传失败:', error)
    alert('上传失败：' + error.message)
  } finally {
    uploading.value = false
  }
}

// 编辑歌曲
function editSong(song) {
  editForm.id = song.id
  editForm.title = song.title
  editForm.artist = song.artist
  editForm.album = song.album || ''
  editForm.duration = song.duration || ''
  showEditModal.value = true
}

// 更新歌曲
async function updateSong() {
  try {
    const response = await adminAPI.updateSong(editForm.id, {
      title: editForm.title,
      artist: editForm.artist,
      album: editForm.album,
      duration: editForm.duration
    })
    
    if (response.message) {
      alert('更新成功！')
      showEditModal.value = false
      await loadSongs()
    }
  } catch (error) {
    alert('更新失败：' + error.message)
  }
}

// 删除歌曲
async function deleteSongConfirm(song) {
  if (!confirm(`确定要删除歌曲《${song.title}》吗？`)) {
    return
  }
  
  try {
    await adminAPI.deleteSong(song.id)
    alert('删除成功！')
    await loadStats()
    await loadSongs()
  } catch (error) {
    alert('删除失败：' + error.message)
  }
}

// 切换歌曲首页推荐状态
async function toggleSongFeatured(song) {
  try {
    const newStatus = !song.is_featured
    await adminAPI.toggleSongFeatured(song.id, newStatus)
    song.is_featured = newStatus
    toast.success(newStatus ? '已设为首页推荐' : '已取消首页推荐')
  } catch (error) {
    console.error('更新失败:', error)
    toast.error('更新失败：' + error.message)
  }
}

// 切换歌曲新歌状态
async function toggleSongNew(song) {
  try {
    const newStatus = !song.is_new
    await adminAPI.toggleSongNew(song.id, newStatus)
    song.is_new = newStatus
    toast.success(newStatus ? '已标记为新歌' : '已取消新歌标记')
  } catch (error) {
    console.error('更新失败:', error)
    toast.error('更新失败：' + error.message)
  }
}

// 切换歌曲推荐状态（首页推荐歌曲板块）
async function toggleSongRecommended(song) {
  try {
    const newStatus = !song.is_recommended
    await adminAPI.toggleSongRecommended(song.id, newStatus)
    song.is_recommended = newStatus
    toast.success(newStatus ? '已设为推荐歌曲' : '已取消推荐歌曲')
  } catch (error) {
    console.error('更新失败:', error)
    toast.error('更新失败：' + error.message)
  }
}

// 过滤歌曲
const filteredSongs = computed(() => {
  if (!searchKeyword.value) return songs.value
  const keyword = searchKeyword.value.toLowerCase()
  return songs.value.filter(song => 
    song.title.toLowerCase().includes(keyword) ||
    song.artist.toLowerCase().includes(keyword)
  )
})

// 过滤歌单
const filteredPlaylists = computed(() => {
  let filtered = allPlaylists.value
  
  // 搜索过滤
  if (playlistSearchKeyword.value) {
    const keyword = playlistSearchKeyword.value.toLowerCase()
    filtered = filtered.filter(playlist => 
      playlist.name.toLowerCase().includes(keyword) ||
      (playlist.creator && playlist.creator.toLowerCase().includes(keyword))
    )
  }
  
  // 分页
  const start = (playlistCurrentPage.value - 1) * playlistPerPage
  const end = start + playlistPerPage
  return filtered.slice(start, end)
})

// 歌单总页数
const playlistTotalPages = computed(() => {
  let filtered = allPlaylists.value
  if (playlistSearchKeyword.value) {
    const keyword = playlistSearchKeyword.value.toLowerCase()
    filtered = filtered.filter(playlist => 
      playlist.name.toLowerCase().includes(keyword) ||
      (playlist.creator && playlist.creator.toLowerCase().includes(keyword))
    )
  }
  return Math.ceil(filtered.length / playlistPerPage)
})

// 过滤歌手
const filteredSingers = computed(() => {
  if (!singerSearchKeyword.value) return singers.value
  const keyword = singerSearchKeyword.value.toLowerCase()
  return singers.value.filter(singer => 
    singer.name.toLowerCase().includes(keyword) ||
    singer.country.toLowerCase().includes(keyword) ||
    singer.genre.toLowerCase().includes(keyword)
  )
})

// 过滤用户
const filteredUsers = computed(() => {
  if (!userSearchKeyword.value) return users.value
  const keyword = userSearchKeyword.value.toLowerCase()
  return users.value.filter(user => 
    user.username.toLowerCase().includes(keyword) ||
    user.email.toLowerCase().includes(keyword)
  )
})

// 分页
function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    loadSongs()
  }
}

function nextPage() {
  currentPage.value++
  loadSongs()
}

// 工具函数
function getCoverUrl(song) {
  return song.cover_image || daitu1
}

function formatDuration(seconds) {
  if (!seconds) return '--:--'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

function goHome() {
  router.push('/')
}

// ==================== 歌单管理功能 ====================

// 加载所有歌单
async function loadAllPlaylists() {
  loadingPlaylists.value = true
  try {
    const response = await playlistAPI.getPublicPlaylists({ per_page: 1000 })
    if (response.code === 200 && response.data) {
      allPlaylists.value = response.data
      playlistCurrentPage.value = 1
    }
  } catch (error) {
    console.error('加载歌单失败:', error)
    toast.error('加载歌单失败')
  } finally {
    loadingPlaylists.value = false
  }
}

// 歌单分页
function playlistPrevPage() {
  if (playlistCurrentPage.value > 1) {
    playlistCurrentPage.value--
  }
}

function playlistNextPage() {
  if (playlistCurrentPage.value < playlistTotalPages.value) {
    playlistCurrentPage.value++
  }
}

// 获取歌单封面
function getPlaylistCover(playlist) {
  if (playlist.cover_image || playlist.cover) {
    const cover = playlist.cover_image || playlist.cover
    if (cover.startsWith('http') || cover.startsWith('/')) {
      return cover
    }
  }
  return daitu1
}

// 切换首页推荐状态
async function toggleFeatured(playlist) {
  try {
    const newStatus = !playlist.is_featured
    await playlistAPI.updateSettings(playlist.id, {
      is_featured: newStatus
    })
    
    playlist.is_featured = newStatus
    toast.success(newStatus ? '已设为首页推荐' : '已取消首页推荐')
  } catch (error) {
    console.error('更新失败:', error)
    toast.error('更新失败：' + error.message)
  }
}

// 查看歌单
function viewPlaylist(playlist) {
  router.push(`/playlist/${playlist.id}`)
}

// 删除歌单确认
async function deletePlaylistConfirm(playlist) {
  if (confirm(`确定要删除歌单"${playlist.name}"吗？此操作不可恢复！`)) {
    try {
      await playlistAPI.deletePlaylist(playlist.id)
      toast.success('删除成功')
      await loadAllPlaylists()
    } catch (error) {
      console.error('删除失败:', error)
      toast.error('删除失败：' + error.message)
    }
  }
}

// ==================== 歌手管理功能 ====================

// 加载歌手列表
async function loadSingers() {
  loadingSingers.value = true
  try {
    const response = await adminAPI.getAllSingers()
    if (response.code === 200) {
      singers.value = response.data.singers || []
    }
  } catch (error) {
    console.error('加载歌手失败:', error)
    toast.error('加载歌手失败')
  } finally {
    loadingSingers.value = false
  }
}

// Tab切换到歌手管理
async function switchToSingersTab() {
  currentTab.value = 'singers'
  await loadSingers()
}

// 编辑歌手
function editSingerAction(singer) {
  singerForm.id = singer.id
  singerForm.name = singer.name
  singerForm.country = singer.country
  singerForm.genre = singer.genre
  singerForm.bio = singer.bio || ''
  singerForm.avatar = singer.avatar || ''
  showEditSingerModal.value = true
}

// 保存歌手
async function saveSinger() {
  try {
    const data = {
      name: singerForm.name,
      country: singerForm.country,
      genre: singerForm.genre,
      bio: singerForm.bio,
      avatar: singerForm.avatar
    }
    
    if (showEditSingerModal.value) {
      await adminAPI.updateSinger(singerForm.id, data)
      toast.success('更新成功')
    } else {
      await adminAPI.createSinger(data)
      toast.success('添加成功')
    }
    
    closeSingerModal()
    await loadSingers()
    await loadStats()
  } catch (error) {
    console.error('保存歌手失败:', error)
    toast.error(error.message || '操作失败')
  }
}

// 删除歌手
async function deleteSingerAction(singer) {
  if (!confirm(`确定要删除歌手"${singer.name}"吗？\n注意：这将同时删除该歌手与歌曲的关联关系。`)) {
    return
  }
  
  try {
    await adminAPI.deleteSinger(singer.id)
    toast.success('删除成功')
    await loadSingers()
    await loadStats()
  } catch (error) {
    console.error('删除歌手失败:', error)
    toast.error(error.message || '删除失败')
  }
}

// 关闭歌手模态框
function closeSingerModal() {
  showAddSingerModal.value = false
  showEditSingerModal.value = false
  singerForm.id = null
  singerForm.name = ''
  singerForm.country = '中国'
  singerForm.genre = '流行'
  singerForm.bio = ''
  singerForm.avatar = ''
}

// 获取歌手头像
function getSingerAvatar(avatar) {
  if (!avatar) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50"><rect fill="%23ddd" width="50" height="50"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="20">🎤</text></svg>'
  if (avatar.startsWith('http')) return avatar
  return avatar
}

// 歌手头像错误处理
function handleSingerImageError(e) {
  e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50"><rect fill="%23ddd" width="50" height="50"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="20">🎤</text></svg>'
}

// ==================== 用户管理功能 ====================

// 加载用户列表
async function loadUsers() {
  loadingUsers.value = true
  try {
    const response = await adminAPI.getAllUsers()
    if (response.code === 200) {
      users.value = response.data.users || []
    }
  } catch (error) {
    console.error('加载用户失败:', error)
    toast.error('加载用户失败')
  } finally {
    loadingUsers.value = false
  }
}

// Tab切换到用户管理
async function switchToUsersTab() {
  currentTab.value = 'users'
  await loadUsers()
}

// 切换用户管理员权限
async function toggleUserAdminAction(user) {
  const newStatus = !user.is_admin
  const action = newStatus ? '设为管理员' : '取消管理员权限'
  
  if (!confirm(`确定要${action}"${user.username}"吗？`)) {
    return
  }
  
  try {
    await adminAPI.toggleUserAdmin(user.id, newStatus)
    toast.success(`${action}成功`)
    await loadUsers()
    await loadStats()
  } catch (error) {
    console.error('权限更新失败:', error)
    toast.error(error.message || '操作失败')
  }
}

// 删除用户
async function deleteUserAction(user) {
  if (!confirm(`确定要删除用户"${user.username}"吗？\n注意：这将删除该用户的所有数据，包括歌单、收藏等。`)) {
    return
  }
  
  try {
    await adminAPI.deleteUser(user.id)
    toast.success('删除成功')
    await loadUsers()
    await loadStats()
  } catch (error) {
    console.error('删除用户失败:', error)
    toast.error(error.message || '删除失败')
  }
}

// 格式化日期
function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 格式化数字
function formatNumber(num) {
  if (!num) return '0'
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toString()
}

// 监听标签页切换
watch(currentTab, (newTab) => {
  if (newTab === 'playlists' && allPlaylists.value.length === 0) {
    loadAllPlaylists()
  }
})

onMounted(() => {
  checkAdminPermission()
})
</script>


<style scoped>
.admin-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 100px 20px;
  font-size: 16px;
  color: #999;
}

/* 无权限 */
.no-permission {
  text-align: center;
  padding: 100px 20px;
}

.no-permission-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.no-permission h2 {
  color: #333;
  margin-bottom: 10px;
}

.no-permission p {
  color: #999;
  margin-bottom: 30px;
}

.btn-back {
  padding: 12px 30px;
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.btn-back:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.3);
}

/* 管理员内容 */
.admin-content {
  max-width: 1400px;
  margin: 0 auto;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.admin-header h1 {
  font-size: 28px;
  color: #333;
  margin: 0;
}

.admin-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.admin-badge {
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  display: flex;
  align-items: center;
  gap: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  border-color: #64AEC2;
}

.stat-icon {
  font-size: 48px;
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.3);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 15px;
  color: #666;
  font-weight: 500;
}

/* 标签页 */
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-btn {
  padding: 14px 28px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  color: #666;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.tab-btn:hover {
  border-color: #64AEC2;
  color: #64AEC2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.2);
}

.tab-btn.active {
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 16px rgba(100, 174, 194, 0.4);
  transform: translateY(-2px);
}

/* 上传区域 */
.upload-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.upload-card h2 {
  font-size: 20px;
  color: #333;
  margin: 0 0 24px 0;
}

.upload-form {
  max-width: 800px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  color: #333;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #64AEC2;
}

.file-info {
  margin-top: 8px;
  color: #4CAF50;
  font-size: 13px;
}

.btn-upload {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-upload:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.3);
}

.btn-upload:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 管理区域 */
.manage-section {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-top: 20px;
}

.manage-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.manage-header h2 {
  font-size: 24px;
  color: #333;
  margin: 0;
  font-weight: 700;
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.search-box input {
  padding: 12px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  width: 350px;
  font-size: 14px;
  transition: all 0.3s;
}

.search-box input:focus {
  outline: none;
  border-color: #64AEC2;
  box-shadow: 0 0 0 3px rgba(100, 174, 194, 0.1);
}

.songs-table {
}

.songs-table table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.songs-table th,
.songs-table td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.songs-table th {
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.songs-table th:first-child {
  border-top-left-radius: 8px;
}

.songs-table th:last-child {
  border-top-right-radius: 8px;
}

.songs-table tbody tr {
  transition: all 0.3s;
}

.songs-table tbody tr:hover {
  background: #f8f9ff;
  transform: translateX(2px);
}

.song-thumb {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-edit,
.btn-delete {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  margin-right: 8px;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-edit {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);
}

.btn-edit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.4);
}

.btn-delete {
  background: linear-gradient(135deg, #f44336, #e53935);
  color: white;
  box-shadow: 0 2px 4px rgba(244, 67, 54, 0.3);
}

.btn-delete:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(244, 67, 54, 0.4);
}

.btn-view {
  background: linear-gradient(135deg, #2196F3, #1976D2);
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  margin-right: 8px;
  transition: all 0.3s;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(33, 150, 243, 0.3);
}

.btn-view:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(33, 150, 243, 0.4);
}

.btn-featured {
  padding: 8px 16px;
  border: 2px solid #FF9800;
  background: white;
  color: #FF9800;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-featured.active {
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  border-color: #FF9800;
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
}

.btn-featured:hover {
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 152, 0, 0.4);
}

.btn-feature {
  padding: 6px 14px;
  border: 2px solid #FF9800;
  background: white;
  color: #FF9800;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.btn-feature.active {
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
}

.btn-feature:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 152, 0, 0.4);
}

.btn-feature:not(.active):hover {
  background: #FFF3E0;
  border-color: #F57C00;
}

.btn-new {
  padding: 6px 14px;
  border: 2px solid #4CAF50;
  background: white;
  color: #4CAF50;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.btn-new.active {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.btn-new:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.4);
}

.btn-new:not(.active):hover {
  background: #E8F5E9;
  border-color: #45a049;
}

.btn-recommended {
  padding: 6px 14px;
  border: 2px solid #2196F3;
  background: white;
  color: #2196F3;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.btn-recommended.active {
  background: linear-gradient(135deg, #2196F3, #1976D2);
  color: white;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.3);
}

.btn-recommended:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(33, 150, 243, 0.4);
}

.btn-recommended:not(.active):hover {
  background: #E3F2FD;
  border-color: #1976D2;
}

.category-badge {
  display: inline-block;
  padding: 6px 14px;
  background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
  color: #1976D2;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(25, 118, 210, 0.1);
}

.status-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.status-badge.public {
  background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
  color: #2E7D32;
}

.status-badge.private {
  background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
  color: #E65100;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #999;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
  border-radius: 12px;
  margin-top: 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.4;
  filter: grayscale(0.5);
}

.empty-state p {
  font-size: 16px;
  color: #666;
}

.playlists-table {
  margin-top: 20px;
}

.playlists-table table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.playlists-table th,
.playlists-table td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.playlists-table th {
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.playlists-table th:first-child {
  border-top-left-radius: 8px;
}

.playlists-table th:last-child {
  border-top-right-radius: 8px;
}

.playlists-table tbody tr {
  transition: all 0.3s;
}

.playlists-table tbody tr:hover {
  background: #f8f9ff;
  transform: translateX(2px);
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 16px;
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.3);
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 弹窗 */
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
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 24px;
  max-width: 500px;
  width: 90%;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-cancel,
.btn-save {
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.btn-cancel {
  background: #f5f5f5;
  color: #666;
}

.btn-save {
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  transition: all 0.3s;
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.3);
}

/* 歌手管理样式 */
.singers-table {
  margin-top: 20px;
}

.singers-table table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.singers-table th,
.singers-table td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.singers-table th {
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.singers-table th:first-child {
  border-top-left-radius: 8px;
}

.singers-table th:last-child {
  border-top-right-radius: 8px;
}

.singers-table tbody tr {
  transition: all 0.3s;
}

.singers-table tbody tr:hover {
  background: #f8f9ff;
  transform: translateX(2px);
}

.singer-avatar-small {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.singer-name {
  font-weight: 600;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input {
  padding: 10px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  width: 250px;
  transition: all 0.3s;
}

.search-input:focus {
  border-color: #64AEC2;
  outline: none;
  box-shadow: 0 0 0 3px rgba(100, 174, 194, 0.1);
}

.btn-add {
  padding: 10px 20px;
  background: linear-gradient(135deg, #64AEC2, #5a9fb0);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.3);
}

/* 用户管理样式 */
.users-table {
  margin-top: 20px;
}

.users-table table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.users-table th,
.users-table td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.users-table th {
  background: linear-gradient(135deg, #64AEC2 0%, #4a9fb0 100%);
  color: white;
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.users-table th:first-child {
  border-top-left-radius: 8px;
}

.users-table th:last-child {
  border-top-right-radius: 8px;
}

.users-table tbody tr {
  transition: all 0.3s;
}

.users-table tbody tr:hover {
  background: #f8f9ff;
  transform: translateX(2px);
}

.username {
  font-weight: 600;
  color: #333;
}

.user-role {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  background: #f0f0f0;
  color: #666;
}

.user-role.admin {
  background: #64AEC2;
  color: white;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-admin {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  background: #f3e5f5;
  color: #7b1fa2;
}

.btn-admin:hover {
  background: #7b1fa2;
  color: white;
}

/* 模态框body */
.modal-body {
  padding: 24px;
}

.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
  transition: all 0.3s;
}

.form-group select:focus,
.form-group textarea:focus {
  border-color: #64AEC2;
  outline: none;
  box-shadow: 0 0 0 3px rgba(100, 174, 194, 0.1);
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 24px;
  }
  
  .stat-value {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
