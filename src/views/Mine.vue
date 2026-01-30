<template>
  <div class="mine-container" @click="showMenu = false">
    <div class="mine-card">
      <!-- 上半部分：背景图区域 -->
      <div class="header-section" :style="{ backgroundImage: `url(${currentBg})` }" @click.stop>
        <!-- 顶部工具栏 -->
        <div class="top-bar">
          <button class="icon-btn" @click="showMenu = !showMenu">
            <i class="ri-menu-line"></i>
            <span class="badge" v-if="notifications > 0">{{ notifications }}</span>
          </button>
          <div class="top-right">
            <button class="icon-btn" @click="showSearch = true">
              <i class="ri-search-line"></i>
            </button>
            <button class="icon-btn" @click="showMore = true">
              <i class="ri-more-2-line"></i>
            </button>
          </div>
        </div>

        <!-- 左上角菜单 -->
        <div class="menu-dropdown" v-if="showMenu" @click.stop>
          <div class="menu-item" @click="showBgModal = true; showMenu = false">
            <i class="ri-palette-line menu-icon"></i>
            <span class="menu-text">更换背景</span>
          </div>
          <div class="menu-item" @click="openCreateModal(); showMenu = false">
            <i class="ri-add-line menu-icon"></i>
            <span class="menu-text">创建歌单</span>
          </div>
          <div class="menu-divider"></div>
          <div class="menu-item" @click="changeAvatar(); showMenu = false">
            <i class="ri-user-line menu-icon"></i>
            <span class="menu-text">更换头像</span>
          </div>
        </div>

        <!-- 用户信息区域 -->
        <div class="user-info-section">
          <!-- 圆形头像 -->
          <div class="user-avatar" @click="triggerAvatarUpload">
            <img :src="getAvatarUrl()" alt="avatar" />
            <div class="avatar-overlay">
              <i class="ri-camera-line camera-icon"></i>
            </div>
          </div>
          <input 
            ref="avatarInput" 
            type="file" 
            accept="image/*" 
            @change="handleAvatarUpload" 
            style="display: none"
          />
          
          <!-- 用户名和VIP -->
          <div class="user-name-row">
            <span class="user-name">{{ userInfo.name }}</span>
            <span class="vip-badge" v-if="userInfo.isVip">
              <i class="ri-vip-crown-line vip-icon"></i>
              <span class="vip-text">VIP·圣</span>
            </span>
          </div>

          <!-- 性别和徽章 -->
          <div class="user-meta">
            <i :class="[userInfo.gender === 'male' ? 'ri-men-line' : 'ri-women-line', 'gender-icon']"></i>
            <span class="divider">·</span>
            <i class="ri-medal-line badge-icon"></i>
            <span class="badge-text">{{ userInfo.id }}</span>
          </div>

          <!-- 统计数据 -->
          <div class="user-stats">
            <div class="stat-item" @click="goToPage('关注')">
              <span class="stat-number">{{ userStats.following }}</span>
              <span class="stat-label">关注</span>
            </div>
            <div class="stat-item" @click="goToPage('粉丝')">
              <span class="stat-number">{{ userStats.followers }}</span>
              <span class="stat-label">粉丝</span>
            </div>
            <div class="stat-item" @click="goToPage('等级')">
              <span class="stat-number">Lv.{{ userStats.level }}</span>
              <span class="stat-label">等级</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">{{ userStats.listenTime }}</span>
              <span class="stat-label">小时</span>
            </div>
          </div>

          <!-- 功能按钮组 -->
          <div class="action-buttons">
            <button class="action-btn" @click="goToHistory">
              <i class="ri-time-line btn-icon"></i>
              <span class="btn-text">最近</span>
            </button>
            <button class="action-btn" @click="goToPage('本地')">
              <i class="ri-download-line btn-icon"></i>
              <span class="btn-text">本地</span>
            </button>
            <button class="action-btn" @click="goToPage('网盘')">
              <i class="ri-cloud-line btn-icon"></i>
              <span class="btn-text">网盘</span>
            </button>
            <button class="action-btn" @click="goToPage('装扮')">
              <i class="ri-t-shirt-line btn-icon"></i>
              <span class="btn-text">装扮</span>
            </button>
            <button class="action-btn" @click="showMoreActions = true">
              <i class="ri-more-2-line btn-icon"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- 下半部分：白色内容区域 -->
      <div class="content-section">
        <!-- 标签页 -->
        <div class="tabs">
          <div 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['tab-item', { active: currentTab === tab.id }]"
            @click="currentTab = tab.id"
          >
            {{ tab.name }}
          </div>
        </div>

        <!-- 子标签 -->
        <div class="sub-tabs">
          <div 
            v-for="subTab in subTabs" 
            :key="subTab.id"
            :class="['sub-tab-item', { active: currentSubTab === subTab.id }]"
            @click="currentSubTab = subTab.id"
          >
            {{ subTab.name }}
            <span class="sub-tab-badge" v-if="subTab.badge">{{ subTab.badge }}</span>
          </div>
          <button class="icon-btn-small">
            <i class="ri-chat-3-line"></i>
          </button>
          <button class="icon-btn-small">
            <i class="ri-more-2-line"></i>
          </button>
        </div>

        <!-- 我喜欢的音乐 -->
        <div class="playlist-list">
          <div 
            class="playlist-item"
            @click="openPlaylist(favoriteSongs)"
          >
            <img :src="favoriteSongs.cover" :alt="favoriteSongs.name" class="playlist-cover playlist-cover-large" />
            <div class="playlist-info">
              <div class="playlist-name">{{ favoriteSongs.name }}</div>
              <div class="playlist-meta">
                <span class="playlist-icon">{{ favoriteSongs.icon }}</span>
                <span class="playlist-count">{{ favoriteSongs.count }}首</span>
                <span class="playlist-divider">·</span>
                <span class="playlist-creator">{{ favoriteSongs.creator }}</span>
              </div>
            </div>
            <button class="playlist-action" @click.stop="showPlaylistMenu(favoriteSongs)">
              <i class="ri-heart-fill liked-icon"></i>
            </button>
          </div>
        </div>

        <!-- 创建的歌单 -->
        <div class="section-block">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-music-2-line"></i> 我创建的歌单 ({{ createdPlaylists.length }})
            </h3>
            <button class="section-more" @click="openCreateModal">
              <i class="ri-add-line"></i> 创建歌单
            </button>
          </div>
          <div v-if="loading" class="loading-text">加载中...</div>
          <div v-else-if="createdPlaylists.length === 0" class="empty-state">
            <i class="ri-music-2-line empty-icon"></i>
            <div class="empty-text">还没有创建歌单</div>
            <button class="empty-btn" @click="openCreateModal">创建第一个歌单</button>
          </div>
          <div v-else class="playlist-grid">
            <div 
              v-for="playlist in createdPlaylists.slice(0, 6)" 
              :key="playlist.id"
              class="grid-item"
            >
              <div class="grid-cover-wrapper" @click="openPlaylist(playlist)">
                <img :src="playlist.cover" :alt="playlist.name" class="grid-cover" />
                <div class="playlist-actions">
                  <button class="action-icon-btn" @click.stop="editPlaylist(playlist)" title="编辑">
                    <i class="ri-edit-line"></i>
                  </button>
                  <button class="action-icon-btn" @click.stop="deletePlaylistConfirm(playlist)" title="删除">
                    <i class="ri-delete-bin-line"></i>
                  </button>
                </div>
              </div>
              <div class="grid-name" @click="openPlaylist(playlist)">{{ playlist.name }}</div>
              <div class="grid-count" @click="openPlaylist(playlist)">{{ playlist.count }}首</div>
            </div>
          </div>
        </div>

        <!-- 收藏的歌单 -->
        <div class="section-block">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-star-line"></i> 我收藏的歌单
            </h3>
            <button class="section-more" @click="goToPage('收藏歌单')">查看全部 ›</button>
          </div>
          <div class="playlist-grid">
            <div 
              v-for="playlist in collectedPlaylists" 
              :key="playlist.id"
              class="grid-item"
              @click="openPlaylist(playlist)"
            >
              <img :src="playlist.cover" :alt="playlist.name" class="grid-cover" />
              <div class="grid-name">{{ playlist.name }}</div>
              <div class="grid-count">{{ playlist.count }}首</div>
            </div>
          </div>
        </div>

        <!-- 听歌排行 -->
        <div class="section-block">
          <div class="section-header">
            <h3 class="section-title">
              <i class="ri-bar-chart-line"></i> 听歌排行
            </h3>
            <button class="section-more" @click="goToPage('听歌排行')">查看详情 ›</button>
          </div>
          <div class="ranking-list">
            <div 
              v-for="ranking in rankingList" 
              :key="ranking.id"
              class="ranking-item"
              @click="openPlaylist(ranking)"
            >
              <div class="ranking-icon">{{ ranking.icon }}</div>
              <div class="ranking-info">
                <div class="ranking-name">{{ ranking.name }}</div>
                <div class="ranking-desc">{{ ranking.creator }}</div>
              </div>
              <div class="ranking-count">{{ ranking.count }}首</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 背景设置弹窗 -->
    <div class="modal" v-if="showBgModal" @click="showBgModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>选择背景</h3>
          <button class="close-btn" @click="showBgModal = false">
            <i class="ri-close-line"></i>
          </button>
        </div>
        <div class="bg-grid">
          <div 
            v-for="bg in backgrounds" 
            :key="bg.id"
            :class="['bg-item', { active: currentBg === bg.url }]"
            @click="changeBg(bg.url)"
          >
            <img :src="bg.url" :alt="bg.name" />
            <div class="bg-name">{{ bg.name }}</div>
          </div>
          <div class="bg-item upload-bg" @click="uploadCustomBg">
            <i class="ri-folder-image-line upload-icon"></i>
            <div class="bg-name">自定义</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建/编辑歌单弹窗 -->
    <div class="modal" v-if="showCreateModal || showEditModal" @click="closePlaylistModal">
      <div class="modal-content create-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ showEditModal ? '编辑歌单' : '创建歌单' }}</h3>
          <button class="close-btn" @click="closePlaylistModal">
            <i class="ri-close-line"></i>
          </button>
        </div>
        
        <!-- 封面上传 -->
        <div class="form-group">
          <label>歌单封面</label>
          <div class="cover-upload-area" @click="triggerCoverUpload">
            <img v-if="newPlaylist.cover" :src="newPlaylist.cover" class="cover-preview" />
            <div v-else class="cover-placeholder">
              <i class="ri-image-add-line"></i>
              <span>点击上传封面</span>
            </div>
          </div>
          <input 
            ref="coverInput" 
            type="file" 
            accept="image/*" 
            @change="handleCoverUpload" 
            style="display: none"
          />
          <div class="form-hint">支持 JPG、PNG 格式，建议尺寸 300x300</div>
        </div>
        
        <div class="form-group">
          <label>歌单名称</label>
          <input 
            v-model="newPlaylist.name" 
            type="text" 
            placeholder="给你的歌单起个名字"
            maxlength="50"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>歌单描述</label>
          <textarea 
            v-model="newPlaylist.description" 
            placeholder="介绍一下这个歌单吧（可选）"
            maxlength="200"
            rows="4"
            class="form-textarea"
          ></textarea>
        </div>
        <div class="modal-actions">
          <button class="btn-cancel" @click="closePlaylistModal">取消</button>
          <button class="btn-create" @click="showEditModal ? updatePlaylist() : createPlaylist()" :disabled="loading">
            {{ loading ? (showEditModal ? '保存中...' : '创建中...') : (showEditModal ? '保存' : '创建') }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { playlistAPI, favoriteAPI, authAPI } from '../utils/api'
import daitu1 from '../assets/daitu1.jpg'
import zuozhu2 from '../assets/zuozhu2.jpg'
import mingren1 from '../assets/mingren1.jpg'
import you1 from '../assets/you1.jpg'
import kakaxi1 from '../assets/kakaxi1.jpg'
import feijian1 from '../assets/feijian1.jpg'

const router = useRouter()
const notifications = ref(4)
const showMenu = ref(false)
const showSearch = ref(false)
const showMore = ref(false)
const showBgModal = ref(false)
const showMoreActions = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const loading = ref(false)
const avatarInput = ref(null)
const coverInput = ref(null)
const uploadingAvatar = ref(false)

// 从localStorage获取用户信息
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
  name: currentUser?.username || '游客',
  email: currentUser?.email || '',
  avatar: currentUser?.avatar || null,
  id: '9枚徽章',
  gender: 'male',
  isVip: false
})

const userStats = reactive({
  following: 0,
  followers: 0,
  level: 1,
  listenTime: 0
})

const currentTab = ref('music')
const tabs = [
  { id: 'music', name: '音乐' },
  { id: 'podcast', name: '播客' },
  { id: 'notes', name: '笔记' }
]

const currentSubTab = ref('favorite')
const subTabs = [
  { id: 'favorite', name: '我的', badge: null },
  { id: 'created', name: '创建歌单', badge: '6' },
  { id: 'collected', name: '收藏歌单', badge: '3' },
  { id: 'ranking', name: '听歌排行', badge: null }
]

// 我喜欢的音乐
const favoriteSongs = ref({
  id: 'favorite',
  name: '我喜欢的音乐',
  cover: daitu1,
  count: 0,
  creator: userInfo.name,
  icon: 'heart',
  isLiked: true,
  type: 'favorite'
})

// 创建的歌单 - 从后端获取
const createdPlaylists = ref([])

// 默认封面图片列表
const defaultCovers = [daitu1, zuozhu2, mingren1, you1, kakaxi1, feijian1]

// 获取随机默认封面
const getRandomCover = () => {
  return defaultCovers[Math.floor(Math.random() * defaultCovers.length)]
}

// 收藏的歌单
const collectedPlaylists = ref([])

// 听歌排行
const rankingList = ref([
  {
    id: 201,
    name: '最近一周',
    cover: kakaxi1,
    count: 45,
    creator: '累计听歌时长 12小时',
    icon: 'chart',
    isLiked: false,
    type: 'ranking'
  },
  {
    id: 202,
    name: '最近一月',
    cover: feijian1,
    count: 189,
    creator: '累计听歌时长 56小时',
    icon: 'chart',
    isLiked: false,
    type: 'ranking'
  },
  {
    id: 203,
    name: '所有时间',
    cover: daitu1,
    count: 1247,
    creator: '累计听歌时长 695小时',
    icon: 'chart',
    isLiked: false,
    type: 'ranking'
  }
])

// 根据当前选中的子标签显示对应的歌单
const displayPlaylists = computed(() => {
  switch (currentSubTab.value) {
    case 'favorite':
      return favoriteSongs.value
    case 'created':
      return createdPlaylists.value
    case 'collected':
      return collectedPlaylists.value
    case 'ranking':
      return rankingList.value
    default:
      return []
  }
})

const backgrounds = ref([
  { id: 1, name: '默认', url: 'https://images.unsplash.com/photo-1557683316-973673baf926?w=800' },
  { id: 2, name: '夜景', url: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800' },
  { id: 3, name: '森林', url: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800' },
  { id: 4, name: '海洋', url: 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800' },
  { id: 5, name: '城市', url: 'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800' },
  { id: 6, name: '星空', url: 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=800' }
])

const currentBg = ref('https://images.unsplash.com/photo-1557683316-973673baf926?w=800')

async function changeBg(url) {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  loading.value = true
  try {
    
    // 找到对应的背景ID
    const bg = backgrounds.value.find(b => b.url === url)
    if (!bg) return
    
    // 保存到数据库
    const response = await fetch('/api/auth/background', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        background_type: 'preset',
        background_image: String(bg.id)
      })
    })
    
    if (response.ok) {
      currentBg.value = url
      localStorage.setItem('mine-bg', url)
      showBgModal.value = false
      alert('背景设置成功！')
    } else {
      const errorData = await response.json()
      alert('设置失败：' + (errorData.error || '未知错误'))
    }
  } catch (error) {
    console.error('设置背景失败:', error)
    alert('设置失败：' + error.message)
  } finally {
    loading.value = false
  }
}

// 触发自定义背景上传
const bgInput = ref(null)

function uploadCustomBg() {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('请先登录')
    router.push('/login')
    return
  }
  // 创建文件输入元素
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = handleBgUpload
  input.click()
}

// 处理背景图片上传
async function handleBgUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  // 检查文件类型
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }
  
  // 检查文件大小（限制5MB）
  if (file.size > 5 * 1024 * 1024) {
    alert('图片大小不能超过5MB')
    return
  }
  
  loading.value = true
  try {
    
    // 创建FormData
    const formData = new FormData()
    formData.append('background', file)
    
    // 上传背景图片
    const response = await fetch('/api/auth/background/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.background_url) {
        // 更新背景
        currentBg.value = data.background_url + '?t=' + Date.now()
        localStorage.setItem('mine-bg', currentBg.value)
        showBgModal.value = false
        alert('背景上传成功！')
      } else {
        alert('上传失败：' + (data.error || '未知错误'))
      }
    } else {
      const errorData = await response.json()
      alert('上传失败：' + (errorData.error || '未知错误'))
    }
  } catch (error) {
    console.error('上传背景失败:', error)
    alert('上传失败：' + error.message)
  } finally {
    loading.value = false
  }
}

// 触发文件选择
function triggerAvatarUpload() {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('请先登录')
    router.push('/login')
    return
  }
  avatarInput.value.click()
}

// 处理头像上传
async function handleAvatarUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  
  // 检查文件类型
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }
  
  // 检查文件大小（限制5MB）
  if (file.size > 5 * 1024 * 1024) {
    alert('图片大小不能超过5MB')
    return
  }
  
  uploadingAvatar.value = true
  try {
    const response = await authAPI.uploadAvatar(file)
    
    if (response.avatar) {
      // 添加时间戳防止缓存
      const avatarUrl = response.avatar + '?t=' + Date.now()
      
      // 更新头像
      userInfo.avatar = avatarUrl
      
      // 更新 localStorage
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      user.avatar = response.avatar
      localStorage.setItem('user', JSON.stringify(user))
      
      alert('头像上传成功！')
    } else {
      alert('上传失败：' + (response.error || '未知错误'))
    }
  } catch (error) {
    console.error('上传头像失败:', error)
    alert('上传失败：' + error.message)
  } finally {
    uploadingAvatar.value = false
    // 清空input，允许重复上传同一文件
    event.target.value = ''
  }
}

// 获取头像URL
function getAvatarUrl() {
  console.log('当前头像路径:', userInfo.avatar)
  
  if (userInfo.avatar) {
    // 如果是完整URL，直接返回
    if (userInfo.avatar.startsWith('http')) {
      return userInfo.avatar
    }
    // 如果是相对路径，确保格式正确
    const avatarPath = userInfo.avatar.startsWith('/') ? userInfo.avatar : '/' + userInfo.avatar
    console.log('处理后的头像路径:', avatarPath)
    return avatarPath
  }
  
  return 'https://cdn.jsdelivr.net/gh/Nikaple/avatar/default-boy.png'
}

function goToPage(page) {
  alert(`跳转到${page}页面`)
}

function goToHistory() {
  router.push('/history')
}

function openPlaylist(playlist) {
  if (playlist.id === 'favorite') {
    // 跳转到收藏页面
    router.push('/favorite')
  } else if (playlist.id) {
    router.push(`/playlist/${playlist.id}`)
  } else {
    alert('歌单详情页面开发中...')
  }
}

function showPlaylistMenu(playlist) {
  alert(`歌单操作：${playlist.name}`)
}

// 创建歌单表单
const newPlaylist = reactive({
  id: null,
  name: '',
  description: '',
  cover: ''
})

// 加载我的歌单
async function loadMyPlaylists() {
  if (!currentUser) {
    console.log('用户未登录')
    return
  }
  
  loading.value = true
  try {
    const response = await playlistAPI.getMyPlaylists()
    if (response.playlists) {
      // 为每个歌单设置默认封面（如果没有封面）
      createdPlaylists.value = response.playlists.map(playlist => ({
        ...playlist,
        cover: playlist.cover || getRandomCover(),
        count: playlist.song_count || 0,
        icon: 'music',
        type: 'created'
      }))
      
      // 更新子标签的徽章数量
      const createdTab = subTabs.find(tab => tab.id === 'created')
      if (createdTab) {
        createdTab.badge = response.total > 0 ? String(response.total) : null
      }
    }
  } catch (error) {
    console.error('加载歌单失败:', error)
    if (error.message.includes('未登录')) {
      alert('请先登录')
      router.push('/login')
    }
  } finally {
    loading.value = false
  }
}

// 加载收藏的歌单
async function loadCollectedPlaylists() {
  if (!currentUser) {
    console.log('用户未登录')
    return
  }
  
  try {
    const response = await playlistAPI.getCollectedPlaylists()
    if (response.playlists) {
      collectedPlaylists.value = response.playlists.map(playlist => ({
        ...playlist,
        cover: playlist.cover || getRandomCover(),
        count: playlist.song_count || 0,
        icon: 'star',
        type: 'collected'
      }))
      
      // 更新子标签的徽章数量
      const collectedTab = subTabs.find(tab => tab.id === 'collected')
      if (collectedTab) {
        collectedTab.badge = response.total > 0 ? String(response.total) : null
      }
    }
  } catch (error) {
    console.error('加载收藏歌单失败:', error)
  }
}

// 创建新歌单
async function createPlaylist() {
  if (!newPlaylist.name.trim()) {
    alert('请输入歌单名称')
    return
  }
  
  loading.value = true
  try {
    const response = await playlistAPI.createPlaylist({
      name: newPlaylist.name,
      description: newPlaylist.description,
      cover: newPlaylist.cover || getRandomCover()
    })
    
    if (response.playlist) {
      alert('创建成功！')
      showCreateModal.value = false
      // 重置表单
      newPlaylist.name = ''
      newPlaylist.description = ''
      newPlaylist.cover = ''
      // 重新加载歌单列表
      await loadMyPlaylists()
    }
  } catch (error) {
    console.error('创建歌单失败:', error)
    alert('创建失败：' + error.message)
  } finally {
    loading.value = false
  }
}

// 打开创建歌单弹窗
function openCreateModal() {
  if (!currentUser) {
    alert('请先登录')
    router.push('/login')
    return
  }
  // 重置表单
  newPlaylist.name = ''
  newPlaylist.description = ''
  newPlaylist.cover = ''
  newPlaylist.id = null
  showCreateModal.value = true
  showEditModal.value = false
}

// 编辑歌单
function editPlaylist(playlist) {
  newPlaylist.id = playlist.id
  newPlaylist.name = playlist.name
  newPlaylist.description = playlist.description || ''
  newPlaylist.cover = playlist.cover || ''
  showEditModal.value = true
  showCreateModal.value = false
}

// 更新歌单
async function updatePlaylist() {
  if (!newPlaylist.name.trim()) {
    alert('请输入歌单名称')
    return
  }
  
  loading.value = true
  try {
    const response = await playlistAPI.updatePlaylist(newPlaylist.id, {
      name: newPlaylist.name,
      description: newPlaylist.description,
      cover: newPlaylist.cover
    })
    
    if (response.playlist) {
      alert('更新成功！')
      closePlaylistModal()
      // 重新加载歌单列表
      await loadMyPlaylists()
    }
  } catch (error) {
    console.error('更新歌单失败:', error)
    alert('更新失败：' + error.message)
  } finally {
    loading.value = false
  }
}

// 删除歌单确认
async function deletePlaylistConfirm(playlist) {
  if (!confirm(`确定要删除歌单"${playlist.name}"吗？此操作不可恢复！`)) {
    return
  }
  
  try {
    await playlistAPI.deletePlaylist(playlist.id)
    alert('删除成功！')
    // 重新加载歌单列表
    await loadMyPlaylists()
  } catch (error) {
    console.error('删除歌单失败:', error)
    alert('删除失败：' + error.message)
  }
}

// 关闭歌单弹窗
function closePlaylistModal() {
  showCreateModal.value = false
  showEditModal.value = false
  newPlaylist.name = ''
  newPlaylist.description = ''
  newPlaylist.cover = ''
  newPlaylist.id = null
}

// 触发封面上传
function triggerCoverUpload() {
  coverInput.value?.click()
}

// 处理封面上传
function handleCoverUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  
  // 检查文件类型
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }
  
  // 检查文件大小（限制5MB）
  if (file.size > 5 * 1024 * 1024) {
    alert('图片大小不能超过5MB')
    return
  }
  
  // 读取文件并转换为Base64
  const reader = new FileReader()
  reader.onload = (e) => {
    newPlaylist.cover = e.target.result
  }
  reader.readAsDataURL(file)
}

// 加载收藏歌曲数量
async function loadFavoriteCount() {
  if (!currentUser) return
  
  try {
    const response = await favoriteAPI.getFavoriteSongs()
    if (response.songs) {
      favoriteSongs.value.count = response.total || response.songs.length
    }
  } catch (error) {
    console.error('加载收藏数量失败:', error)
  }
}

// 加载用户信息
async function loadUserInfo() {
  if (!currentUser) return
  
  try {
    const response = await authAPI.getCurrentUser()
    if (response.user) {
      // 更新用户信息
      userInfo.name = response.user.username
      userInfo.email = response.user.email
      if (response.user.avatar) {
        userInfo.avatar = response.user.avatar + '?t=' + Date.now()
      }
      
      // 加载用户的背景设置
      if (response.user.background_type === 'custom' && response.user.background_image) {
        currentBg.value = response.user.background_image + '?t=' + Date.now()
        localStorage.setItem('mine-bg', currentBg.value)
      } else if (response.user.background_type === 'preset' && response.user.background_image) {
        // 如果是预设背景，从backgrounds数组中查找
        const presetBg = backgrounds.value.find(bg => bg.id === parseInt(response.user.background_image))
        if (presetBg) {
          currentBg.value = presetBg.url
          localStorage.setItem('mine-bg', currentBg.value)
        }
      }
      
      // 更新 localStorage
      localStorage.setItem('user', JSON.stringify(response.user))
    }
  } catch (error) {
    console.error('加载用户信息失败:', error)
  }
}

// 页面加载时获取数据
onMounted(() => {
  loadUserInfo()
  loadMyPlaylists()
  loadCollectedPlaylists()
  loadFavoriteCount()
})

const savedBg = localStorage.getItem('mine-bg')
if (savedBg) {
  currentBg.value = savedBg
}
</script>

<style scoped>
/* 外层容器 - 左右留白 */
.mine-container {
  min-height: 100vh;
  background: #f5f5f5;
  display: flex;
  justify-content: center;
}

/* 中间卡片 - 固定最大宽度 */
.mine-card {
  width: 100%;
  max-width: 1150px;
  background: white;
  min-height: 100vh;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

/* 上半部分：背景图区域 */
.header-section {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  padding: 16px 20px 30px;
}

.header-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, 
    rgba(0, 0, 0, 0.3) 0%,
    rgba(0, 0, 0, 0.6) 100%
  );
  z-index: 0;
}

.header-section > * {
  position: relative;
  z-index: 1;
}

/* 顶部工具栏 */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.top-right {
  display: flex;
  gap: 12px;
}

.icon-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  font-size: 18px;
  position: relative;
  backdrop-filter: blur(10px);
  transition: all 0.3s;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.menu-icon {
  font-size: 18px;
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ff4444;
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 10px;
  font-weight: bold;
}

/* 用户信息区域 - 居中 */
.user-info-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

/* 圆形头像 */
.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid rgba(255, 255, 255, 0.9);
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.user-avatar:hover {
  transform: scale(1.05);
}

.user-avatar:hover .avatar-overlay {
  opacity: 1;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.camera-icon {
  font-size: 28px;
  color: white;
}

/* 用户名和VIP */
.user-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.user-name {
  font-size: 22px;
  font-weight: bold;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.vip-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(255, 255, 255, 0.25);
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  color: white;
  backdrop-filter: blur(10px);
}

.vip-icon {
  font-size: 12px;
  color: #ff4444;
}

/* 性别和徽章 */
.user-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  margin-bottom: 16px;
}

.gender-icon {
  color: #4a9eff;
  font-size: 14px;
}

.divider {
  opacity: 0.6;
}

/* 统计数据 */
.user-stats {
  display: flex;
  gap: 28px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.stat-number {
  font-size: 16px;
  font-weight: bold;
  color: white;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.stat-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
}

/* 功能按钮组 */
.action-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-btn {
  background: rgba(0, 0, 0, 0.4);
  border: none;
  border-radius: 18px;
  padding: 10px 18px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: white;
  font-size: 13px;
  backdrop-filter: blur(10px);
  transition: all 0.3s;
}

.action-btn:hover {
  background: rgba(0, 0, 0, 0.5);
}

.btn-icon {
  font-size: 14px;
}

.btn-text {
  font-size: 13px;
}

/* 下半部分：白色内容区域 */
.content-section {
  background: white;
  padding: 20px;
  min-height: 400px;
}

/* 标签页 */
.tabs {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.tab-item {
  padding: 12px 4px;
  color: #666;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.tab-item.active {
  color: #333;
  border-bottom-color: #ff4444;
}

.tab-item:hover {
  color: #333;
}

/* 子标签 */
.sub-tabs {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 20px;
}

.sub-tab-item {
  padding: 6px 12px;
  background: #f5f5f5;
  border-radius: 16px;
  color: #666;
  cursor: pointer;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.3s;
}

.sub-tab-item.active {
  background: #333;
  color: white;
}

.sub-tab-item:hover {
  background: #e0e0e0;
}

.sub-tab-item.active:hover {
  background: #333;
}

.sub-tab-badge {
  font-size: 11px;
}

.icon-btn-small {
  background: transparent;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 16px;
  padding: 4px;
  transition: all 0.3s;
}

.icon-btn-small:hover {
  color: #333;
}

/* 歌单列表 */
.playlist-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.playlist-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.playlist-item:hover {
  background: #f5f5f5;
}

.playlist-cover {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
}

.playlist-info {
  flex: 1;
  min-width: 0;
}

.playlist-name {
  color: #333;
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.playlist-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #999;
  font-size: 12px;
}

.playlist-icon {
  font-size: 12px;
}

.playlist-divider {
  opacity: 0.5;
}

.playlist-action {
  background: transparent;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 18px;
  padding: 8px;
  transition: all 0.3s;
}

.playlist-action:hover {
  color: #333;
}

.liked-icon {
  font-size: 16px;
  color: #ff4444;
}

/* 我喜欢的音乐 - 稍大的封面 */
.playlist-cover-large {
  width: 90px !important;
  height: 90px !important;
}

/* 背景设置弹窗 */
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
  overflow-y: auto;
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

.bg-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
}

.bg-item {
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.bg-item:hover {
  transform: translateY(-4px);
  border-color: #ddd;
}

.bg-item.active {
  border-color: #ff4444;
}

.bg-item img {
  width: 100%;
  height: 100px;
  object-fit: cover;
  display: block;
}

.bg-name {
  padding: 8px;
  text-align: center;
  color: #666;
  font-size: 13px;
  background: #f5f5f5;
}

.upload-bg {
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 128px;
}

.upload-icon {
  font-size: 36px;
  margin-bottom: 8px;
  color: #999;
}

/* 左上角菜单下拉框 */
.menu-dropdown {
  position: absolute;
  top: 60px;
  left: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  min-width: 180px;
  overflow: hidden;
  z-index: 10;
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

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  transition: all 0.2s;
  color: #333;
}

.menu-item:hover {
  background: #f5f5f5;
}

.menu-item .menu-icon {
  font-size: 16px;
  width: 24px;
  text-align: center;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.menu-item .menu-text {
  font-size: 14px;
  font-weight: 500;
}

.menu-divider {
  height: 1px;
  background: #e0e0e0;
  margin: 4px 0;
}

/* 创建歌单弹窗 */
.create-modal {
  max-width: 500px;
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

.form-hint {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
}

/* 封面上传区域 */
.cover-upload-area {
  width: 200px;
  height: 200px;
  border: 2px dashed #e0e0e0;
  border-radius: 12px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-upload-area:hover {
  border-color: #64AEC2;
  background: #f8f9fa;
}

.cover-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #999;
}

.cover-placeholder i {
  font-size: 48px;
}

.cover-placeholder span {
  font-size: 14px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  color: #333;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #ff4444;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-cancel,
.btn-create {
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.btn-cancel {
  background: #f5f5f5;
  color: #666;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

.btn-create {
  background: #ff4444;
  color: white;
}

.btn-create:hover:not(:disabled) {
  background: #ff2222;
}

.btn-create:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 加载和空状态 */
.loading-text {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 14px;
}

.empty-state {
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
  background: #ff4444;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.empty-btn:hover {
  background: #ff2222;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 68, 68, 0.3);
}

/* 新增功能模块样式 */
.section-block {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 17px;
  font-weight: 600;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.section-title i {
  font-size: 18px;
}

.section-more {
  background: transparent;
  border: none;
  color: #999;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 4px;
}

.section-more:hover {
  color: #333;
}

/* 歌单网格 */
.playlist-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

@media (min-width: 480px) {
  .playlist-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
  }
}

@media (min-width: 640px) {
  .playlist-grid {
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
  }
}

.grid-item {
  transition: all 0.3s;
}

.grid-item:hover {
  transform: translateY(-3px);
}

.grid-cover-wrapper {
  position: relative;
  cursor: pointer;
}

.grid-cover {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 6px;
  transition: all 0.3s;
  display: block;
}

.grid-item:hover .grid-cover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

/* 歌单操作按钮 */
.playlist-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 6px;
  opacity: 0;
  transition: opacity 0.3s;
}

.grid-cover-wrapper:hover .playlist-actions {
  opacity: 1;
}

.action-icon-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.action-icon-btn:hover {
  background: white;
  transform: scale(1.1);
}

.action-icon-btn i {
  font-size: 16px;
  color: #333;
}

.action-icon-btn:hover i {
  color: #64AEC2;
}

.grid-name {
  font-size: 13px;
  font-weight: 500;
  color: #333;
  margin-bottom: 3px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.3;
}

.grid-count {
  font-size: 11px;
  color: #999;
}

/* 听歌排行列表 */
.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.ranking-item:hover {
  background: #e9ecef;
  transform: translateX(4px);
}

.ranking-icon {
  font-size: 32px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 8px;
}

.ranking-info {
  flex: 1;
  min-width: 0;
}

.ranking-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.ranking-desc {
  font-size: 12px;
  color: #999;
}

.ranking-count {
  font-size: 14px;
  font-weight: 600;
  color: #666;
}
</style>
