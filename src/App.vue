<template>
  <div id="app">
    <!-- 组件 -->
    <Header v-if="!$route.meta.hideLayout" />
    <Navigation 
      v-if="!$route.meta.hideLayout"
      @search="handleSearch" 
    />
    <main :class="{ 'with-player': hasCurrentSong }">
      <router-view />
    </main>
    <Footer v-if="!$route.meta.hideLayout" />
    
    <!-- 全局音乐播放器 -->
    <MusicPlayer ref="musicPlayer" />
  </div>
</template>

<script>
// 导入组件
import Header from './components/Header.vue'
import Navigation from './components/Navigation.vue'
import Footer from './components/Footer.vue'
// import MusicPlayer from './components/MusicPlayer.vue'
// import MusicPlayer from './components/MusicPlayerSimple.vue'
import MusicPlayer from './components/MusicPlayerEnhanced.vue'

// 选项式API
export default {
  name: 'App',
  components: {
    // 注册组件
    Header,
    Navigation,
    Footer,
    MusicPlayer
  },
  data() {
    return {
      hasCurrentSong: false
    }
  },
  methods: {
    handleSearch(query) {
      // 跳转到歌曲页面并传递搜索关键词
      this.$router.push({
        path: '/songs',
        query: { keyword: query }
      })
    }
  },
  mounted() {
    // 全局播放歌曲方法
    window.playSong = (song) => {
      if (this.$refs.musicPlayer) {
        this.$refs.musicPlayer.playSong(song)
        this.hasCurrentSong = true
      }
    }
    
    // 全局添加到播放队列方法
    window.addToQueue = (song) => {
      if (this.$refs.musicPlayer) {
        const success = this.$refs.musicPlayer.addToQueue(song)
        if (success) {
          this.hasCurrentSong = true
          return true
        }
        return false
      }
      return false
    }
  }
}
</script>

<style>
main.with-player {
  padding-bottom: 100px;
}
</style>