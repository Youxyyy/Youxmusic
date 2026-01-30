<template>
  <div class="music-player-simple" v-if="currentSong">
    <div class="player-container">
      <!-- 歌曲信息 -->
      <div class="song-info">
        <div class="song-cover-placeholder">
          <i class="ri-music-2-line"></i>
        </div>
        <div class="song-details">
          <div class="song-title">{{ currentSong.title }}</div>
          <div class="song-artist">{{ currentSong.artist }}</div>
        </div>
      </div>

      <!-- 原生音频控件 -->
      <audio 
        ref="audioPlayer"
        controls
        :src="currentSong.file_path"
        class="audio-player"
        @error="onAudioError"
      ></audio>

      <!-- 关闭按钮 -->
      <button class="close-btn" @click="closePlayer">
        <i class="ri-close-line"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const currentSong = ref(null)
const audioPlayer = ref(null)

// 播放歌曲
const playSong = (song) => {
  console.log('播放歌曲:', song)
  
  // 确保歌曲有 file_path
  if (!song.file_path) {
    console.warn('歌曲缺少 file_path，尝试使用默认路径')
    // 根据歌曲标题设置路径
    if (song.title === '遇见') {
      song.file_path = '/music_files/yujian.mp3'
    } else if (song.title === '勇气') {
      song.file_path = '/music_files/yongqi.mp3'
    } else {
      console.error('无法确定歌曲文件路径')
      return
    }
  }
  
  console.log('使用文件路径:', song.file_path)
  
  // 停止当前播放
  if (audioPlayer.value && !audioPlayer.value.paused) {
    audioPlayer.value.pause()
  }
  
  // 设置新歌曲
  currentSong.value = song
  
  // 等待 DOM 更新后加载新音频
  setTimeout(() => {
    if (audioPlayer.value) {
      audioPlayer.value.load()
      console.log('音频已加载')
    }
  }, 100)
}

// 音频错误处理
const onAudioError = (e) => {
  console.error('音频加载错误:', e)
  console.error('当前歌曲:', currentSong.value)
  console.error('文件路径:', currentSong.value?.file_path)
}

// 关闭播放器
const closePlayer = () => {
  if (audioPlayer.value) {
    audioPlayer.value.pause()
  }
  currentSong.value = null
}

// 暴露方法给父组件
defineExpose({
  playSong
})
</script>

<style scoped>
.music-player-simple {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #e0e0e0;
  z-index: 1000;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.player-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 歌曲信息 */
.song-info {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 200px;
}

.song-cover-placeholder {
  width: 50px;
  height: 50px;
  border-radius: 6px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
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
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 原生音频控件 */
.audio-player {
  flex: 1;
  height: 40px;
  outline: none;
}

/* 关闭按钮 */
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
  flex-shrink: 0;
}

.close-btn:hover {
  background: #f5f7fa;
  color: #333;
}

/* 响应式 */
@media (max-width: 768px) {
  .player-container {
    flex-wrap: wrap;
    gap: 12px;
    padding: 12px 16px;
  }

  .song-info {
    width: 100%;
  }

  .audio-player {
    width: 100%;
  }
}
</style>
