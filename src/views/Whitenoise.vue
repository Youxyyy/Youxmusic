<template>
  <div class="whitenoise">
    <div class="container">
      <h1 class="page-title">白噪音</h1>
      <p class="page-description">自定义混合多种自然环境声音，助你沉静专注</p>
      <div class="whitenoise-grid">
        <div v-for="sound in soundList" :key="sound.key" class="whitenoise-card">
          <div class="whitenoise-icon">{{ sound.icon }}</div>
          <h3>{{ sound.name }}</h3>
          <audio :src="sound.src" ref="audioRefs[sound.key]" loop></audio>
          <div class="whitenoise-control">
            <button class="btn-whitenoise" @click="toggleSound(sound.key)">
              {{ sound.isPlaying ? '暂停' : '播放' }}
            </button>
            <input type="range" min="0" max="1" step="0.01" v-model.number="sound.volume" @input="setVolume(sound.key, sound.volume)">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
const audioRefs = reactive({})

const soundList = reactive([
  {
    key: 'rain',
    name: '雨声',
    icon: '🌧️',
    src: 'https://cdn.pixabay.com/audio/2022/10/16/audio_12cd9e6b53.mp3',
    volume: 0.7, isPlaying: false
  },
  {
    key: 'thunder',
    name: '雷声',
    icon: '⛈️',
    src: 'https://cdn.pixabay.com/audio/2022/11/16/audio_12ae9852b3.mp3',
    volume: 0.5, isPlaying: false
  },
  {
    key: 'wind',
    name: '风声',
    icon: '🌬️',
    src: 'https://cdn.pixabay.com/audio/2022/11/16/audio_12ae98582b.mp3',
    volume: 0.5, isPlaying: false
  },
  {
    key: 'fire',
    name: '篝火',
    icon: '🔥',
    src: 'https://cdn.pixabay.com/audio/2022/03/15/audio_115b5b9bdd.mp3',
    volume: 0.4, isPlaying: false
  },
  {
    key: 'sea',
    name: '海浪',
    icon: '🌊',
    src: 'https://cdn.pixabay.com/audio/2022/07/26/audio_121b440b2e.mp3',
    volume: 0.6, isPlaying: false
  },
  {
    key: 'forest',
    name: '森林',
    icon: '🌲',
    src: 'https://cdn.pixabay.com/audio/2022/10/16/audio_12cc6c84a2.mp3',
    volume: 0.5, isPlaying: false
  },
  {
    key: 'bird',
    name: '鸟鸣',
    icon: '🐦',
    src: 'https://cdn.pixabay.com/audio/2022/10/16/audio_12cc118b71.mp3',
    volume: 0.45, isPlaying: false
  },
  {
    key: 'river',
    name: '溪流',
    icon: '🏞️',
    src: 'https://cdn.pixabay.com/audio/2022/08/20/audio_123e6db501.mp3',
    volume: 0.45, isPlaying: false
  },
  {
    key: 'night',
    name: '虫鸣',
    icon: '🦗',
    src: 'https://cdn.pixabay.com/audio/2022/10/16/audio_12cc388a85.mp3',
    volume: 0.4, isPlaying: false
  }
])

function toggleSound(key) {
  const sound = soundList.find(s => s.key === key)
  const audio = audioRefs[key]
  if (!audio) return
  if (!sound.isPlaying) {
    audio.volume = sound.volume
    audio.play()
    sound.isPlaying = true
  } else {
    audio.pause()
    sound.isPlaying = false
  }
}
function setVolume(key, volume) {
  const audio = audioRefs[key]
  if (audio) audio.volume = volume
}
</script>

<style scoped>
.whitenoise-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.whitenoise-card {
  background: white;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}
.whitenoise-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(100,174,194,0.17);
  border-color: #a7c5fb;
}
.whitenoise-icon {
  font-size: 50px;
  margin-bottom: 20px;
}
.whitenoise-card h3 {
  margin-bottom: 15px;
  color: #64aec2;
}
.whitenoise-control {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-top: 18px;
}
.btn-whitenoise {
  background: linear-gradient(135deg,#64AEC2 0%, #a7c5fb 100%);
  color: #fff;
  border: none;
  padding: 10px 28px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  box-shadow: 0 2px 8px rgba(167,197,251,0.13);
}
.btn-whitenoise:hover {
  background: linear-gradient(135deg, #a7c5fb 0%, #64aec2 100%);
  color: #222;
  box-shadow: 0 5px 20px rgba(100,174,194,0.19);
}
input[type=range] {
  width: 140px;
  accent-color: #64AEC2;
}
</style>