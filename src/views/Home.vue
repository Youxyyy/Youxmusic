<template>
  <div class="home">
    <div class="container">
      <h1 class="page-title">欢迎来到 YouxMusic</h1>
      <p class="page-description">这是一个供位景阳学习 Vue3 + Flask + MySQL 的网站...让我们一起加油！</p>

      <!-- 歌单推荐轮播 -->
      <div class="playlist-recommendation">
        <div class="section-header">
          <h2 class="section-title">歌单推荐</h2>
          <div class="category-tabs">
            <span 
              v-for="category in categories" 
              :key="category"
              :class="['category-tab', { active: activeCategory === category }]"
              @click="activeCategory = category"
            >
              {{ category }}
            </span>
          </div>
        </div>

        <div class="carousel-container">
          <div class="carousel-wrapper">
                        <div 
              class="carousel-track" 
              :style="{ 
                transform: `translateX(-${(currentIndex - slidesPerView) * (100 / slidesPerView)}%)`,
                transition: isTransitioning ? 'transform 0.5s ease-in-out' : 'none'
              }"
              ref="carouselTrackRef"
            >
              <div 
                v-for="(playlist, index) in visiblePlaylists" 
                :key="`${playlist.id}-${index}`"
                class="carousel-slide"
              >
                <div class="playlist-card" @click="goToPlaylist(playlist)">
                  <div class="playlist-cover">
                    <img :src="playlist.cover" :alt="playlist.title" />
                    <div class="play-count">
                      <i class="ri-play-fill"></i> {{ formatPlayCount(playlist.playCount) }}
                    </div>
                  </div>
                  <div class="playlist-info">
                    <h3 class="playlist-title">{{ playlist.title }}</h3>
                    <p class="playlist-desc">{{ playlist.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 导航按钮 -->
          <button class="carousel-btn prev" @click="prevSlide">‹</button>
          <button class="carousel-btn next" @click="nextSlide">›</button>
          
          <!-- 指示器 -->
          <div class="carousel-indicators">
            <span 
              v-for="index in totalSlides" 
              :key="index"
              :class="['indicator', { active: (currentIndex - slidesPerView) === index - 1 }]"
              @click="goToSlide(index - 1)"
            ></span>
          </div>
        </div>
      </div>

      <!-- 推荐歌曲 -->
      <div class="recommended-songs">
        <h2 class="section-title">推荐歌曲</h2>
        <div class="songs-list">
          <div v-for="song in recommendedSongs" :key="song.id" class="song-card" @click="playSong(song)">
            <div class="song-cover">
              <img :src="getCoverUrl(song)" :alt="song.title" />
              <div class="play-overlay">
                <i class="ri-play-fill play-icon"></i>
              </div>
            </div>
            <div class="song-info">
              <p class="song-name">{{ song.title }}</p>
              <p class="song-artist">{{ song.artist }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 歌单 -->
      <div class="playlists-section">
        <h2 class="section-title">更多歌单</h2>
        <div class="playlists-grid">
          <div 
            v-for="playlist in originalPlaylists.slice(0, 9)" 
            :key="playlist.id" 
            class="playlist-item"
            @click="goToPlaylist(playlist)"
          >
            <img :src="playlist.cover" :alt="playlist.title" class="playlist-cover-img" />
            <p class="playlist-title-text">{{ playlist.title }}</p>
            <p class="playlist-meta">{{ playlist.song_count || 0 }} 首歌曲</p>
          </div>
        </div>
      </div>

      <!-- 大家都在听 -->
      <div class="popular-listens">
        <h2 class="section-title">大家都在听</h2>
        <div class="hot-songs-grid">
          <div v-for="(song, index) in hotSongs" :key="song.id" class="hot-song-item" @click="playSong(song)">
            <span class="hot-number">{{ index + 1 }}</span>
            <div class="hot-song-cover">
              <img :src="getCoverUrl(song)" :alt="song.title" />
            </div>
            <div class="hot-song-info">
              <p class="hot-song-name">{{ song.title }}</p>
              <p class="hot-song-artist">{{ song.artist }}</p>
            </div>
            <span class="hot-tag">HOT</span>
          </div>
        </div>
      </div>

      <!-- 新歌推荐 -->
      <div class="new-songs">
        <h2 class="section-title">新歌推荐</h2>
        <div class="new-songs-list">
          <div v-for="song in newSongs" :key="song.id" class="new-song-card" @click="playSong(song)">
            <img :src="getCoverUrl(song)" :alt="song.title" class="new-song-cover" />
            <div class="new-song-content">
              <p class="new-song-name">{{ song.title }}</p>
              <p class="new-song-artist">{{ song.artist }}</p>
              <p class="new-song-time">{{ getTimeAgo(song.created_at) }}</p>
            </div>
            <button class="new-song-btn" @click.stop="playSong(song)">
              <i class="ri-play-fill"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, inject } from 'vue'
import { useRouter } from 'vue-router'
import { songAPI, playlistAPI } from '../utils/api'
import ban1 from '../assets/ban1.jpg'
import chutian1 from '../assets/chutian1.jpg'
import daitu1 from '../assets/daitu1.jpg'
import feijian1 from '../assets/feijian1.jpg'
import kakaxi1 from '../assets/kakaxi1.jpg'
import mingren1 from '../assets/mingren1.jpg'
import you1 from '../assets/you1.jpg'
import zuozhu1 from '../assets/zuozhu1.jpg' 
import zuozhu2 from '../assets/zuozhu2.jpg'

const router = useRouter()
const toast = inject('toast')

// 推荐歌曲数据
const recommendedSongs = ref([])

// 大家都在听数据
const hotSongs = ref([])

// 新歌推荐数据
const newSongs = ref([])

// 加载推荐歌曲
const loadRecommendedSongs = async () => {
  try {
    const response = await songAPI.getSongs(1, 6)
    if (response.code === 200 && response.data.songs) {
      recommendedSongs.value = response.data.songs
    }
  } catch (error) {
    console.error('加载推荐歌曲失败:', error)
  }
}

// 加载热门歌曲
const loadHotSongs = async () => {
  try {
    const response = await songAPI.getHotSongs(6)
    if (response.code === 200 && response.data) {
      hotSongs.value = response.data
    }
  } catch (error) {
    console.error('加载热门歌曲失败:', error)
  }
}

// 加载新歌推荐
const loadNewSongs = async () => {
  try {
    const response = await songAPI.getLatestSongs(6)
    if (response.code === 200 && response.data) {
      newSongs.value = response.data
    }
  } catch (error) {
    console.error('加载新歌失败:', error)
  }
}

// 播放歌曲
const playSong = (song) => {
  console.log('首页点击播放:', song)
  if (window.playSong) {
    window.playSong(song)
  } else {
    console.error('播放器未初始化，window.playSong 不存在')
  }
}

// 获取封面图片URL
const getCoverUrl = (song) => {
  if (!song || !song.cover_image) {
    return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%23ddd" width="100" height="100"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="30">🎵</text></svg>'
  }
  
  // 如果是完整URL，直接返回
  if (song.cover_image.startsWith('http')) {
    return song.cover_image
  }
  
  // 如果是本地导入的图片对象，直接返回
  if (typeof song.cover_image === 'object') {
    return song.cover_image
  }
  
  // 如果是相对路径（如 /covers/xxx.jpg），通过代理访问
  if (song.cover_image.startsWith('/')) {
    return song.cover_image
  }
  
  // 默认封面
  return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%23ddd" width="100" height="100"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="30">🎵</text></svg>'
}

// 格式化时间
const getTimeAgo = (dateString) => {
  if (!dateString) return '最近'
  
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days === 2) return '前天'
  return `${days}天前`
}

// 歌单数据 - 从数据库加载
const playlists = ref([])

// 响应式数据
const activeCategory = ref('为你推荐')
const currentIndex = ref(0)
const autoPlay = ref(true)
const autoPlayInterval = ref(null)
const isTransitioning = ref(true)
const carouselTrackRef = ref(null)

// 分类数据
const categories = ['为你推荐',  '情歌', '网络歌曲', '官方歌单', '经典']

// 原始歌单数据 - 从数据库加载
const originalPlaylists = ref([])

// 加载公共歌单
const loadPublicPlaylists = async () => {
  try {
    const params = {
      per_page: 20
    }
    
    // 如果不是"为你推荐"，则按分类筛选
    if (activeCategory.value !== '为你推荐') {
      params.category = activeCategory.value
    }
    
    const response = await playlistAPI.getPublicPlaylists(params)
    if (response.code === 200 && response.data) {
      originalPlaylists.value = response.data.map(playlist => ({
        id: playlist.id,
        title: playlist.name,
        description: playlist.description || '',
        cover: getPlaylistCover(playlist),
        playCount: playlist.play_count || 0,
        category: playlist.category || '为你推荐',
        song_count: playlist.song_count || 0,
        creator: playlist.creator || '未知'
      }))
    }
  } catch (error) {
    console.error('加载歌单失败:', error)
    toast.error('加载歌单失败')
  }
}

// 获取歌单封面
const getPlaylistCover = (playlist) => {
  if (!playlist.cover_image && !playlist.cover) {
    return daitu1 // 默认封面
  }
  
  const cover = playlist.cover_image || playlist.cover
  
  // 如果是完整URL，直接返回
  if (cover.startsWith('http')) {
    return cover
  }
  
  // 如果是相对路径，通过代理访问
  if (cover.startsWith('/')) {
    return cover
  }
  
  // 根据文件名匹配本地图片
  const coverMap = {
    'daitu1.jpg': daitu1,
    'zuozhu2.jpg': zuozhu2,
    'mingren1.jpg': mingren1,
    'you1.jpg': you1,
    'kakaxi1.jpg': kakaxi1,
    'feijian1.jpg': feijian1,
    'ban1.jpg': ban1,
    'zuozhu1.jpg': zuozhu1,
    'chutian1.jpg': chutian1
  }
  
  const fileName = cover.split('/').pop()
  return coverMap[fileName] || daitu1
}

// 监听分类变化，重新加载歌单
watch(activeCategory, () => {
  loadPublicPlaylists()
})

// 计算属性 - 创建无限循环的数据
const filteredPlaylists = computed(() => {
  let filtered = []
  if (activeCategory.value === '为你推荐') {
    filtered = [...originalPlaylists.value]
  } else {
    filtered = originalPlaylists.value.filter(playlist => playlist.category === activeCategory.value)
  }
  
  // 如果数据不够，直接返回
  if (filtered.length <= 1) return filtered
  
  // 创建无限循环数据：在首尾添加克隆项
  // 为了平滑过渡，我们在开头添加最后几个元素，在结尾添加最前几个元素
  const lastItems = filtered.slice(-slidesPerView.value)
  const firstItems = filtered.slice(0, slidesPerView.value)
  
  return [...lastItems, ...filtered, ...firstItems]
})

const slidesPerView = computed(() => {
  const width = window.innerWidth
  if (width < 768) return 2
  if (width < 1024) return 3
  return 4
})

const visiblePlaylists = computed(() => {
  return filteredPlaylists.value
})

// 计算实际显示的歌单数量（不包括克隆的）
const actualPlaylistCount = computed(() => {
  let filtered = []
  if (activeCategory.value === '为你推荐') {
    filtered = [...originalPlaylists.value]
  } else {
    filtered = originalPlaylists.value.filter(playlist => playlist.category === activeCategory.value)
  }
  return filtered.length
})

const totalSlides = computed(() => {
  return Math.max(1, actualPlaylistCount.value)
})

const maxRealIndex = computed(() => {
  return actualPlaylistCount.value - 1
})

// 辅助索引边界（允许到达两侧各 1 张克隆）
const minAllowedIndex = computed(() => Math.max(0, slidesPerView.value - 1))
const maxAllowedIndex = computed(() => slidesPerView.value + actualPlaylistCount.value)

// 方法
const formatPlayCount = (count) => {
  if (count >= 100000000) {
    return (count / 100000000).toFixed(1) + '亿'
  } else if (count >= 10000) {
    return (count / 10000).toFixed(1) + '万'
  }
  return count.toString()
}

const nextSlide = () => {
  const nextIndex = currentIndex.value + 1
  if (nextIndex <= maxAllowedIndex.value) {
    currentIndex.value = nextIndex
  }
}

const prevSlide = () => {
  const prevIndex = currentIndex.value - 1
  if (prevIndex >= minAllowedIndex.value) {
    currentIndex.value = prevIndex
  }
}

const goToSlide = (index) => {
  // 跳转到指定位置，需要加上克隆区域的前缀长度
  currentIndex.value = index + slidesPerView.value
}

const startAutoPlay = () => {
  if (autoPlay.value) {
    autoPlayInterval.value = setInterval(() => {
      nextSlide()
    }, 3000) // 改为3秒切换一次
  }
}

const stopAutoPlay = () => {
  if (autoPlayInterval.value) {
    clearInterval(autoPlayInterval.value)
    autoPlayInterval.value = null
  }
}

// 边界过渡结束后无感复位
const handleTransitionEnd = () => {
  const k = slidesPerView.value
  const n = actualPlaylistCount.value
  if (n <= 1) return
  // 右侧：已到达右侧首个克隆（k + n）时，瞬间复位到真实首项 k
  if (currentIndex.value === k + n) {
    isTransitioning.value = false
    currentIndex.value = k
    // 双 rAF 确保样式应用后再恢复过渡
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        isTransitioning.value = true
      })
    })
  }
  // 左侧：已到达左侧最后一个克隆（k - 1）时，瞬间复位到真实末项 k + n - 1
  if (currentIndex.value === k - 1) {
    isTransitioning.value = false
    currentIndex.value = k + n - 1
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        isTransitioning.value = true
      })
    })
  }
}

// 跳转到歌单详情
const goToPlaylist = (playlist) => {
  // 增加播放次数
  playlistAPI.incrementPlayCount(playlist.id).catch(err => {
    console.error('更新播放次数失败:', err)
  })
  
  // 跳转到详情页
  router.push(`/playlist/${playlist.id}`)
}

// 初始化与销毁
onMounted(() => {
  currentIndex.value = slidesPerView.value
  if (carouselTrackRef.value) {
    carouselTrackRef.value.addEventListener('transitionend', handleTransitionEnd)
  }
  startAutoPlay()
  
  // 加载数据
  loadPublicPlaylists()  // 加载歌单
  loadRecommendedSongs()
  loadHotSongs()
  loadNewSongs()
})

onUnmounted(() => {
  if (carouselTrackRef.value) {
    carouselTrackRef.value.removeEventListener('transitionend', handleTransitionEnd)
  }
  stopAutoPlay()
})
</script>
<style scoped>
/* 保持你原来的样式不变 */
.playlist-recommendation {
  padding: 30px 0;
  background:#f5f7fa;
  width: 100%;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 0 20px;
}

.section-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.category-tabs {
  display: flex;
  gap: 20px;
}

.category-tab {
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  color: #666;
}

.category-tab.active {
  background: #64AEC2;
  color: white;
}

.category-tab:hover {
  background: #e0e0e0;
}

.carousel-container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  overflow: hidden;
}

.carousel-wrapper {
  overflow: hidden;
  border-radius: 12px;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.carousel-slide {
  flex: 0 0 25%;
  padding: 0 10px;
  box-sizing: border-box;
}

.playlist-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.playlist-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.playlist-cover {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.playlist-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-count {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.playlist-info {
  padding: 16px;
}

.playlist-title {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 8px 0;
  color: #333;
  line-height: 1.3;
}

.playlist-desc {
  font-size: 12px;
  color: #666;
  margin: 0;
  line-height: 1.4;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  background: white;
  border: none;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  font-size: 20px;
  color: #333;
  transition: all 0.3s ease;
  z-index: 10;
  opacity: 0; /* 默认隐藏 */
  visibility: hidden; /* 默认隐藏 */
}

.carousel-btn:hover:not(:disabled) {
  background: #64AEC2;
  color: white;
}

.carousel-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.carousel-btn.prev {
  left: 20px;
}

.carousel-btn.next {
  right: 20px;
}

.carousel-indicators {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 20px;
}

/* 鼠标悬停在轮播容器时显示按钮 */
.carousel-container:hover .carousel-btn {
  opacity: 1;
  visibility: visible;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ccc;
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator.active {
  background: #64AEC2;
  transform: scale(1.2);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .carousel-slide {
    flex: 0 0 33.333%;
  }
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .category-tabs {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .carousel-slide {
    flex: 0 0 50%;
  }
  
 .carousel-btn {
    width: 36px;
    height: 36px;
    font-size: 16px;
    opacity: 1;
    visibility: visible;
  }
}

@media (max-width: 480px) {
  .carousel-slide {
    flex: 0 0 100%;
  }
  
  .section-title {
    font-size: 20px;
  }
  
  .category-tab {
    padding: 6px 12px;
    font-size: 12px;
  }
}

/* 推荐歌曲样式 */
.recommended-songs {
  margin-top: 20px;
  padding: 30px 0;
}

.recommended-songs .section-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.songs-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.song-card {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.song-card:hover {
  transform: translateY(-5px);
}

.song-cover {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 10px;
}

.song-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-overlay {
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
  transition: opacity 0.3s ease;
}

.song-card:hover .play-overlay {
  opacity: 1;
}

.play-icon {
  color: white;
  font-size: 30px;
}

.song-info {
  text-align: center;
}

.song-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin: 0 0 5px 0;
}

.song-artist {
  font-size: 12px;
  color: #8f9ab7;
  margin: 0;
}

/* 歌单样式 */
.playlists-section {
  margin-top: 20px;
  padding: 30px 0;
}

.playlists-section .section-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.playlists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.playlist-item {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.playlist-item:hover {
  transform: translateY(-5px);
}

.playlist-cover-img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.playlist-title-text {
  font-size: 14px;
  color: #333;
  margin: 0;
  text-align: center;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.playlist-meta {
  font-size: 12px;
  color: #999;
  margin: 5px 0 0 0;
  text-align: center;
}

/* 大家都在听样式 */
.popular-listens {
  margin-top: 20px;
  padding: 30px 0;
}

.popular-listens .section-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.hot-songs-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hot-song-item {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
}

.hot-song-item:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.hot-number {
  width: 30px;
  text-align: center;
  font-weight: bold;
  color: #64AEC2;
  font-size: 16px;
}

.hot-song-cover {
  width: 80px;
  height: 80px;
  border-radius: 6px;
  overflow: hidden;
  margin-right: 15px;
}

.hot-song-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hot-song-info {
  flex: 1;
}

.hot-song-name {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  margin: 0 0 5px 0;
}

.hot-song-artist {
  font-size: 13px;
  color: #8f9ab7;
  margin: 0;
}

.hot-tag {
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
  color: white;
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: bold;
}

/* 新歌推荐样式 */
.new-songs {
  margin-top: 20px;
  padding: 30px 0;
}

.new-songs .section-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.new-songs-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.new-song-card {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
}

.new-song-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.new-song-cover {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
  margin-right: 15px;
}

.new-song-content {
  flex: 1;
}

.new-song-name {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  margin: 0 0 5px 0;
}

.new-song-artist {
  font-size: 13px;
  color: #8f9ab7;
  margin: 0 0 3px 0;
}

.new-song-time {
  font-size: 12px;
  color: #64AEC2;
  margin: 0;
}

.new-song-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #64AEC2, #a7c5fb);
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.new-song-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(100, 174, 194, 0.3);
}

/* 响应式样式 */
@media (max-width: 768px) {
  .songs-list {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 15px;
  }
  
  .playlists-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 15px;
  }
  
  .new-songs-list {
    grid-template-columns: 1fr;
  }
}
.page-title {
  font-size: 3rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 20px;
  color: #2c3e50;
  /* 动画效果 */
  animation: fadeInUp 2s ease;
}

.page-description {
  font-size: 1.2rem;
  text-align: center;
  color: #2c3e50;
  margin-bottom: 40px;
  /* 动画效果 */
  animation: fadeInUp 1s ease;
}
/* 淡入上升动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>