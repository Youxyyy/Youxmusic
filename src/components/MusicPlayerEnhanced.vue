<template>
  <div class="music-player" v-if="currentSong">
    <div class="player-container">
      <!-- 左侧：歌曲信息 -->
      <div class="song-info">
        <img :src="getCoverUrl(currentSong)" class="song-cover" />
        <div class="song-details">
          <div class="song-title">{{ currentSong.title }}</div>
          <div class="song-artist">{{ currentSong.artist }}</div>
        </div>
      </div>

      <!-- 中间：播放控制 -->
      <div class="player-controls">
        <!-- 控制按钮 -->
        <div class="control-buttons">
          <button @click="togglePlayMode" class="control-btn icon-btn" :title="playModeText">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path v-if="playMode === 'list'" d="M7 7h10v2H7V7zm0 4h10v2H7v-2zm0 4h10v2H7v-2zm12-8v10l-5-5 5-5z"/>
              <path v-else-if="playMode === 'single'" d="M7 7h10v10H7V7zm2 2v6h6V9H9z"/>
              <path v-else d="M10.59 9.17L5.41 4 4 5.41l5.17 5.17 1.42-1.41zM14.5 4l2.04 2.04L4 18.59 5.41 20 17.96 7.46 20 9.5V4h-5.5zm.33 9.41l-1.41 1.41 3.13 3.13L14.5 20H20v-5.5l-2.04 2.04-3.13-3.13z"/>
            </svg>
          </button>
          <button @click="playPrevious" class="control-btn icon-btn" :disabled="!hasPrevious">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
              <path d="M6 6h2v12H6V6zm3.5 6l8.5 6V6l-8.5 6z"/>
            </svg>
          </button>
          <button @click="togglePlay" class="control-btn play-btn">
            <svg v-if="!isPlaying" viewBox="0 0 24 24" width="24" height="24" fill="white">
              <path d="M8 5v14l11-7z"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" width="24" height="24" fill="white">
              <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
            </svg>
          </button>
          <button @click="playNext" class="control-btn icon-btn" :disabled="!hasNext">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
              <path d="M16 18h2V6h-2v12zM6 18l8.5-6L6 6v12z"/>
            </svg>
          </button>
          <button @click="togglePlaylist" class="control-btn icon-btn" :title="'播放列表 (' + playlist.length + ')'">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M15 6H3v2h12V6zm0 4H3v2h12v-2zM3 16h8v-2H3v2zM17 6v8.18c-.31-.11-.65-.18-1-.18-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3V8h3V6h-5z"/>
            </svg>
          </button>
        </div>

        <!-- 进度条 -->
        <div class="progress-bar">
          <span class="time">{{ formatTime(currentTime) }}</span>
          <div class="progress-wrapper">
            <div class="progress-track">
              <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
            </div>
            <input 
              type="range" 
              min="0" 
              :max="duration" 
              v-model="currentTime"
              @input="seek"
              class="progress-slider"
            />
          </div>
          <span class="time">{{ formatTime(duration) }}</span>
        </div>
      </div>

      <!-- 右侧：音量和关闭 -->
      <div class="player-actions">
        <div class="volume-control">
          <span class="volume-icon">🔊</span>
          <input 
            type="range" 
            min="0" 
            max="100" 
            v-model="volume"
            @input="changeVolume"
            class="volume-slider"
          />
        </div>
        <button @click="closePlayer" class="close-btn">
          <i class="ri-close-line"></i>
        </button>
      </div>

      <!-- 音频元素 -->
      <audio 
        ref="audioPlayer"
        :src="currentSong.file_path"
        @timeupdate="updateTime"
        @loadedmetadata="updateDuration"
        @ended="onSongEnded"
        @play="isPlaying = true"
        @pause="isPlaying = false"
      ></audio>
    </div>

    <!-- 播放列表弹窗 -->
    <div v-if="showPlaylist" class="playlist-modal" @click="showPlaylist = false">
      <div class="playlist-content" @click.stop>
        <div class="playlist-header">
          <h3>播放列表 ({{ playlist.length }})</h3>
          <div class="header-actions">
            <button @click="clearPlaylist" class="btn-clear">清空</button>
            <button @click="showPlaylist = false" class="btn-close">
              <i class="ri-close-line"></i>
            </button>
          </div>
        </div>
        <div class="playlist-items">
          <div 
            v-for="(song, index) in playlist" 
            :key="index"
            :class="['playlist-item', { active: index === currentIndex }]"
            @click="playByIndex(index)"
          >
            <span class="item-index">{{ index + 1 }}</span>
            <img :src="getCoverUrl(song)" class="item-cover" />
            <div class="item-info">
              <div class="item-title">{{ song.title }}</div>
              <div class="item-artist">{{ song.artist }}</div>
            </div>
            <button @click.stop="removeFromPlaylist(index)" class="btn-remove">
              <i class="ri-delete-bin-line"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import daitu1 from '../assets/daitu1.jpg'

const audioPlayer = ref(null)
const currentSong = ref(null)
const playlist = ref([])
const currentIndex = ref(0)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(80)
const playMode = ref('list') // list: 列表循环, single: 单曲循环, random: 随机播放
const showPlaylist = ref(false)

// 计算进度百分比
const progressPercent = computed(() => {
  if (!duration.value) return 0
  return (currentTime.value / duration.value) * 100
})

// 播放模式图标和文本
const playModeIcon = computed(() => {
  switch (playMode.value) {
    case 'list': return '🔁'
    case 'single': return '🔂'
    case 'random': return '🔀'
    default: return '🔁'
  }
})

const playModeText = computed(() => {
  switch (playMode.value) {
    case 'list': return '列表循环'
    case 'single': return '单曲循环'
    case 'random': return '随机播放'
    default: return '列表循环'
  }
})

// 是否有上一首/下一首
const hasPrevious = computed(() => currentIndex.value > 0)
const hasNext = computed(() => currentIndex.value < playlist.value.length - 1)

// 播放歌曲
const playSong = (song, addToPlaylist = true) => {
  if (!song.file_path) {
    console.error('歌曲缺少文件路径')
    return
  }
  
  if (addToPlaylist) {
    // 检查是否已在播放列表中
    const existingIndex = playlist.value.findIndex(s => s.id === song.id)
    if (existingIndex >= 0) {
      // 已存在，直接播放
      currentIndex.value = existingIndex
    } else {
      // 添加到播放列表
      playlist.value.push(song)
      currentIndex.value = playlist.value.length - 1
    }
  }
  
  currentSong.value = song
  
  // 记录播放历史
  recordPlayHistory(song.id)
  
  setTimeout(() => {
    if (audioPlayer.value) {
      audioPlayer.value.load()
      audioPlayer.value.play()
    }
  }, 100)
}

// 添加到播放队列（不立即播放）
const addToQueue = (song) => {
  if (!song.file_path) {
    console.error('歌曲缺少文件路径')
    return
  }
  
  // 检查是否已在播放列表中
  const existingIndex = playlist.value.findIndex(s => s.id === song.id)
  if (existingIndex >= 0) {
    return false // 已存在
  }
  
  // 添加到播放列表末尾
  playlist.value.push(song)
  
  // 如果当前没有播放的歌曲，自动播放
  if (!currentSong.value) {
    currentIndex.value = playlist.value.length - 1
    playSong(song, false)
  }
  
  return true // 添加成功
}

// 记录播放历史
const recordPlayHistory = async (songId) => {
  const token = localStorage.getItem('access_token')
  if (!token) return // 未登录不记录
  
  try {
    await fetch('/api/history/record', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ song_id: songId })
    })
  } catch (error) {
    console.error('记录播放历史失败:', error)
  }
}

// 播放/暂停
const togglePlay = () => {
  if (!audioPlayer.value) return
  
  if (isPlaying.value) {
    audioPlayer.value.pause()
  } else {
    audioPlayer.value.play()
  }
}

// 上一首
const playPrevious = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    playSong(playlist.value[currentIndex.value], false)
  }
}

// 下一首
const playNext = () => {
  if (playMode.value === 'random') {
    // 随机播放
    const randomIndex = Math.floor(Math.random() * playlist.value.length)
    currentIndex.value = randomIndex
    playSong(playlist.value[randomIndex], false)
  } else if (currentIndex.value < playlist.value.length - 1) {
    currentIndex.value++
    playSong(playlist.value[currentIndex.value], false)
  } else if (playMode.value === 'list') {
    // 列表循环，回到第一首
    currentIndex.value = 0
    playSong(playlist.value[0], false)
  }
}

// 歌曲播放结束
const onSongEnded = () => {
  if (playMode.value === 'single') {
    // 单曲循环
    audioPlayer.value.currentTime = 0
    audioPlayer.value.play()
  } else {
    // 播放下一首
    playNext()
  }
}

// 切换播放模式
const togglePlayMode = () => {
  const modes = ['list', 'single', 'random']
  const currentModeIndex = modes.indexOf(playMode.value)
  playMode.value = modes[(currentModeIndex + 1) % modes.length]
}

// 更新时间
const updateTime = () => {
  if (audioPlayer.value) {
    currentTime.value = Math.floor(audioPlayer.value.currentTime)
  }
}

// 更新时长
const updateDuration = () => {
  if (audioPlayer.value) {
    duration.value = Math.floor(audioPlayer.value.duration)
  }
}

// 拖动进度条
const seek = () => {
  if (audioPlayer.value) {
    audioPlayer.value.currentTime = currentTime.value
  }
}

// 改变音量
const changeVolume = () => {
  if (audioPlayer.value) {
    audioPlayer.value.volume = volume.value / 100
  }
}

// 格式化时间
const formatTime = (seconds) => {
  if (!seconds || isNaN(seconds)) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 获取封面
const getCoverUrl = (song) => {
  return song.cover_image || daitu1
}

// 切换播放列表显示
const togglePlaylist = () => {
  showPlaylist.value = !showPlaylist.value
}

// 通过索引播放
const playByIndex = (index) => {
  currentIndex.value = index
  playSong(playlist.value[index], false)
  showPlaylist.value = false
}

// 从播放列表移除
const removeFromPlaylist = (index) => {
  if (index === currentIndex.value) {
    // 如果移除的是当前播放的歌曲
    if (playlist.value.length > 1) {
      playNext()
    } else {
      closePlayer()
    }
  } else if (index < currentIndex.value) {
    currentIndex.value--
  }
  playlist.value.splice(index, 1)
}

// 清空播放列表
const clearPlaylist = () => {
  if (confirm('确定要清空播放列表吗？')) {
    playlist.value = []
    closePlayer()
  }
}

// 关闭播放器
const closePlayer = () => {
  if (audioPlayer.value) {
    audioPlayer.value.pause()
  }
  currentSong.value = null
  showPlaylist.value = false
}

// 初始化音量
watch(audioPlayer, (newPlayer) => {
  if (newPlayer) {
    newPlayer.volume = volume.value / 100
  }
})

// 暴露方法
defineExpose({
  playSong,
  addToQueue
})
</script>


<style scoped>
.music-player {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #e0e0e0;
  z-index: 1000;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.player-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
}

/* 歌曲信息 */
.song-info {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 200px;
  flex-shrink: 0;
}

.song-cover {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.song-details {
  flex: 1;
  min-width: 0;
}

.song-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-artist {
  font-size: 12px;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 播放控制 */
.player-controls {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.control-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.control-btn {
  border-radius: 50%;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  color: #5f6368;
}

.icon-btn {
  width: 40px;
  height: 40px;
}

.icon-btn:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.05);
  transform: scale(1.05);
}

.icon-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.play-btn {
  width: 56px;
  height: 56px;
  background: #45c9e0ff;
  color: white;
  box-shadow: 0 2px 8px rgba(73, 209, 233, 0.3);
}

.play-btn:hover {
  background: #30c5d0ff;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(35, 180, 224, 0.4);
}

/* 进度条 */
.progress-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.time {
  font-size: 12px;
  color: #999;
  min-width: 40px;
  text-align: center;
}

.progress-wrapper {
  flex: 1;
  position: relative;
  height: 20px;
  display: flex;
  align-items: center;
}

.progress-track {
  position: absolute;
  width: 100%;
  height: 5px;
  background: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
  pointer-events: none;
}

.progress-fill {
  height: 100%;
  background: #2daeda;
  border-radius: 3px;
  transition: width 0.1s linear;
}

.progress-slider {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 100%;
  height: 20px;
  outline: none;
  -webkit-appearance: none;
  background: transparent;
  cursor: pointer;
  z-index: 2;
  margin: 0;
}

/* WebKit 浏览器（Chrome, Safari） */
.progress-slider::-webkit-slider-runnable-track {
  width: 100%;
  height: 5px;
  background: transparent;
  border-radius: 3px;
}

.progress-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #1299e1;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
  margin-top: -4.5px;
}

.progress-slider:hover::-webkit-slider-thumb {
  transform: scale(1.2);
  box-shadow: 0 2px 6px rgba(30, 184, 211, 0.4);
}

/* Firefox */
.progress-slider::-moz-range-track {
  width: 100%;
  height: 5px;
  background: transparent;
  border-radius: 3px;
  border: none;
}

.progress-slider::-moz-range-thumb {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #1cc1d3;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
}

.progress-slider:hover::-moz-range-thumb {
  transform: scale(1.2);
  box-shadow: 0 2px 6px rgba(20, 158, 186, 0.4);
}

/* 右侧操作 */
.player-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.volume-icon {
  font-size: 18px;
}

.volume-slider {
  width: 80px;
  height: 4px;
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
  background: #e0e0e0;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #5f6368;
  cursor: pointer;
}

.volume-slider::-moz-range-thumb {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #5f6368;
  cursor: pointer;
  border: none;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: #999;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #333;
}

/* 播放列表弹窗 */
.playlist-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 1001;
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  padding: 24px;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.playlist-content {
  width: 400px;
  max-height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
  display: flex;
  flex-direction: column;
  margin-bottom: 80px;
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



.playlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.playlist-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.btn-clear {
  padding: 6px 12px;
  background: #f5f5f5;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-clear:hover {
  background: #e0e0e0;
}

.btn-close {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: #999;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-close:hover {
  background: #f5f5f5;
  color: #333;
}

.playlist-items {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.playlist-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.playlist-item:hover {
  background: #f8f9fa;
}

.playlist-item.active {
  background: #e8f0fe;
}

.item-index {
  width: 24px;
  text-align: center;
  font-size: 12px;
  color: #999;
  font-weight: 600;
}

.item-cover {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  object-fit: cover;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-size: 13px;
  font-weight: 500;
  color: #333;
  margin-bottom: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-artist {
  font-size: 11px;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-remove {
  background: transparent;
  border: none;
  font-size: 14px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.3s;
}

.playlist-item:hover .btn-remove {
  opacity: 1;
}

.btn-remove:hover {
  transform: scale(1.2);
}

/* 响应式 */
@media (max-width: 1024px) {
  .volume-control {
    display: none;
  }
}

@media (max-width: 768px) {
  .player-container {
    flex-wrap: wrap;
    gap: 12px;
    padding: 12px 16px;
  }

  .song-info {
    width: 100%;
  }

  .player-controls {
    width: 100%;
  }

  .player-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .playlist-modal {
    padding: 0;
    align-items: flex-end;
  }
  
  .playlist-content {
    width: 100%;
    border-radius: 12px 12px 0 0;
    margin-bottom: 80px;
  }
}
</style>
