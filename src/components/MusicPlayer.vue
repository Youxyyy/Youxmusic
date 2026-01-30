<template>
  <div class="music-player" v-if="currentSong">
    <div class="player-container">
      <!-- 歌曲信息 -->
      <div class="song-info">
        <img 
          :src="getCoverUrl(currentSong.cover_image)" 
          :alt="currentSong.title"
          class="song-cover"
          @error="handleImageError"
        />
        <div class="song-details">
          <div class="song-title">{{ currentSong.title }}</div>
          <div class="song-artist">{{ currentSong.artist }}</div>
        </div>
      </div>

      <!-- 播放控制 -->
      <div class="player-controls">
        <button class="control-btn" @click="previousSong" title="上一首">
          <span>⏮</span>
        </button>
        <button class="control-btn play-btn" @click.stop="togglePlay" :title="isPlaying ? '暂停' : '播放'">
          <i :class="isPlaying ? 'ri-pause-fill' : 'ri-play-fill'"></i>
        </button>
        <button class="control-btn" @click="nextSong" title="下一首">
          <span>⏭</span>
        </button>
      </div>

      <!-- 进度条 -->
      <div class="progress-section">
        <span class="time">{{ formatTime(currentTime) }}</span>
        <div class="progress-bar" @click="seek">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <span class="time">{{ formatTime(duration) }}</span>
      </div>

      <!-- 音量控制 -->
      <div class="volume-section">
        <button class="control-btn" @click="toggleMute">
          <span>{{ isMuted ? '🔇' : '🔊' }}</span>
        </button>
        <input 
          type="range" 
          min="0" 
          max="100" 
          v-model="volume" 
          @input="changeVolume"
          class="volume-slider"
        />
      </div>

      <!-- 关闭按钮 -->
      <button class="close-btn" @click="closePlayer" title="关闭播放器">
        <i class="ri-close-line"></i>
      </button>
    </div>

    <!-- 隐藏的音频元素 -->
    <audio 
      ref="audioPlayer"
      @timeupdate="updateTime"
      @loadedmetadata="updateDuration"
      @ended="onSongEnd"
      @error="onError"
      @canplay="onCanPlay"
      @playing="isPlaying = true"
      @pause="isPlaying = false"
    ></audio>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

// 响应式数据
const currentSong = ref(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(80)
const isMuted = ref(false)
const audioPlayer = ref(null)

// 计算进度百分比
const progress = ref(0)

// API 基础 URL
const API_BASE = '/api'
// 静态文件也通过代理访问，避免跨域问题
const STATIC_BASE = ''

// 格式化时间
function formatTime(seconds) {
  if (!seconds || isNaN(seconds)) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 获取封面 URL
function getCoverUrl(coverPath) {
  if (!coverPath) return '/default-cover.jpg'
  if (coverPath.startsWith('http')) return coverPath
  return `${STATIC_BASE}${coverPath}`
}

// 获取音频 URL
function getAudioUrl(filePath) {
  if (!filePath) return ''
  if (filePath.startsWith('http')) return filePath
  return `${STATIC_BASE}${filePath}`
}

// 图片加载失败处理
function handleImageError(e) {
  e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="%23ddd" width="100" height="100"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="%23999" font-size="40">🎵</text></svg>'
}

// 播放歌曲
const playSong = (song) => {
  currentSong.value = song
  
  if (audioPlayer.value) {
    const audioUrl = getAudioUrl(song.file_path)
    console.log('加载歌曲:', song.title, '音频URL:', audioUrl)
    
    audioPlayer.value.src = audioUrl
    audioPlayer.value.volume = volume.value / 100
    
    // 加载音频
    audioPlayer.value.load()
    
    // 尝试自动播放（可能会被浏览器阻止）
    audioPlayer.value.play().then(() => {
      console.log('自动播放成功')
      // 增加播放次数
      fetch(`${API_BASE}/songs/${song.id}/play`, { method: 'POST' })
        .catch(err => console.error('更新播放次数失败:', err))
    }).catch(error => {
      if (error.name === 'NotAllowedError') {
        console.log('浏览器阻止了自动播放，请点击播放按钮')
      } else {
        console.error('播放失败:', error.name, error.message)
      }
    })
  }
}

// 防抖标志 - 使用 ref 确保响应式
const isToggling = ref(false)

// 切换播放/暂停
const togglePlay = () => {
  if (!audioPlayer.value) {
    console.error('音频播放器未初始化')
    return
  }
  
  // 防止重复点击
  if (isToggling.value) {
    console.log('操作进行中，请稍候')
    return
  }
  
  isToggling.value = true
  console.log('togglePlay 被调用, paused:', audioPlayer.value.paused)
  
  // 使用 audio 元素的 paused 属性来判断状态
  if (audioPlayer.value.paused) {
    console.log('开始播放')
    audioPlayer.value.play()
      .then(() => {
        console.log('播放成功')
        setTimeout(() => { isToggling.value = false }, 300)
      })
      .catch(error => {
        console.error('播放失败:', error.name, error.message)
        isToggling.value = false
      })
  } else {
    console.log('暂停播放')
    audioPlayer.value.pause()
    setTimeout(() => { isToggling.value = false }, 300)
  }
}

// 更新播放时间
function updateTime() {
  if (audioPlayer.value) {
    currentTime.value = audioPlayer.value.currentTime
    if (duration.value > 0) {
      progress.value = (currentTime.value / duration.value) * 100
    }
  }
}

// 更新总时长
function updateDuration() {
  if (audioPlayer.value) {
    duration.value = audioPlayer.value.duration
  }
}

// 拖动进度条
function seek(e) {
  if (!audioPlayer.value || !duration.value) return
  
  const progressBar = e.currentTarget
  const rect = progressBar.getBoundingClientRect()
  const percent = (e.clientX - rect.left) / rect.width
  const newTime = percent * duration.value
  
  audioPlayer.value.currentTime = newTime
}

// 改变音量
function changeVolume() {
  if (audioPlayer.value) {
    audioPlayer.value.volume = volume.value / 100
    if (volume.value > 0) {
      isMuted.value = false
    }
  }
}

// 切换静音
function toggleMute() {
  if (audioPlayer.value) {
    isMuted.value = !isMuted.value
    audioPlayer.value.muted = isMuted.value
  }
}

// 上一首
function previousSong() {
  // TODO: 实现播放列表功能
  console.log('上一首')
}

// 下一首
function nextSong() {
  // TODO: 实现播放列表功能
  console.log('下一首')
}

// 歌曲播放结束
function onSongEnd() {
  // TODO: 自动播放下一首
  console.log('歌曲播放结束')
  isPlaying.value = false
}

// 音频错误事件
function onError(e) {
  console.error('音频加载错误:', e)
  if (audioPlayer.value && audioPlayer.value.error) {
    console.error('错误代码:', audioPlayer.value.error.code)
    console.error('错误信息:', audioPlayer.value.error.message)
  }
}

// 音频可以播放事件
function onCanPlay() {
  console.log('音频已加载，可以播放')
}

// 关闭播放器
function closePlayer() {
  if (audioPlayer.value) {
    audioPlayer.value.pause()
  }
  currentSong.value = null
}

// 暴露方法给父组件
defineExpose({
  playSong
})

// 监听音量变化
watch(volume, (newVolume) => {
  if (audioPlayer.value) {
    audioPlayer.value.volume = newVolume / 100
  }
})

// 组件卸载时清理
onUnmounted(() => {
  if (audioPlayer.value) {
    audioPlayer.value.pause()
  }
})
</script>

<style scoped>
.music-player {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.95), rgba(0, 0, 0, 0.9));
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 1000;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.3);
}

.player-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
}

/* 歌曲信息 */
.song-info {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 250px;
}

.song-cover {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.song-details {
  flex: 1;
  min-width: 0;
}

.song-title {
  font-size: 15px;
  font-weight: 600;
  color: white;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-artist {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 播放控制 */
.player-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.control-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.play-btn {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  font-size: 20px;
}

.play-btn:hover {
  background: linear-gradient(135deg, #7c8ff0, #8a5bb5);
  transform: scale(1.1);
}

/* 进度条 */
.progress-section {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.time {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  min-width: 40px;
  text-align: center;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.1s;
}

.progress-bar:hover .progress-fill {
  background: linear-gradient(90deg, #7c8ff0, #8a5bb5);
}

/* 音量控制 */
.volume-section {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 150px;
}

.volume-slider {
  flex: 1;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.volume-slider::-moz-range-thumb {
  width: 14px;
  height: 14px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* 关闭按钮 */
.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

/* 响应式 */
@media (max-width: 768px) {
  .player-container {
    flex-wrap: wrap;
    gap: 12px;
    padding: 12px 16px;
  }

  .song-info {
    min-width: auto;
    flex: 1;
  }

  .volume-section {
    display: none;
  }

  .progress-section {
    order: 3;
    width: 100%;
  }
}
</style>
