<template>
  <button 
    :class="['favorite-btn', { active: isFavorite, loading: isLoading }]"
    @click.stop="toggleFavorite"
    :disabled="isLoading"
    :title="isFavorite ? '取消收藏' : '收藏'"
  >
    <i :class="['ri-heart-' + (isFavorite ? 'fill' : 'line'), 'heart-icon']"></i>
  </button>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { favoriteAPI } from '../utils/api'

const props = defineProps({
  songId: {
    type: Number,
    required: true
  },
  initialFavorite: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:favorite'])

const isFavorite = ref(props.initialFavorite)
const isLoading = ref(false)

// 切换收藏状态
async function toggleFavorite() {
  // 检查是否登录
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('请先登录')
    return
  }
  
  isLoading.value = true
  
  try {
    if (isFavorite.value) {
      // 取消收藏
      await favoriteAPI.removeFavorite(props.songId)
      isFavorite.value = false
      emit('update:favorite', false)
    } else {
      // 收藏
      await favoriteAPI.addFavorite(props.songId)
      isFavorite.value = true
      emit('update:favorite', true)
    }
  } catch (error) {
    console.error('收藏操作失败:', error)
    alert(error.message || '操作失败')
  } finally {
    isLoading.value = false
  }
}

// 检查收藏状态
async function checkFavoriteStatus() {
  const token = localStorage.getItem('access_token')
  if (!token) return
  
  try {
    const response = await favoriteAPI.checkFavorite(props.songId)
    isFavorite.value = response.is_favorite
  } catch (error) {
    console.error('检查收藏状态失败:', error)
  }
}

// 监听 songId 变化
watch(() => props.songId, () => {
  checkFavoriteStatus()
})

onMounted(() => {
  checkFavoriteStatus()
})
</script>

<style scoped>
.favorite-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.favorite-btn:hover:not(:disabled) {
  background: rgba(255, 68, 68, 0.1);
  transform: scale(1.1);
}

.favorite-btn.active {
  animation: heartBeat 0.3s ease;
  color: #ff4444;
}

.favorite-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.favorite-btn.loading {
  animation: pulse 1s infinite;
}

.heart-icon {
  display: block;
  line-height: 1;
  font-size: 18px;
  transition: all 0.3s;
}

@keyframes heartBeat {
  0%, 100% {
    transform: scale(1);
  }
  25% {
    transform: scale(1.3);
  }
  50% {
    transform: scale(1.1);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
