import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    // 通过代理的形式，处理跨域问题
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Flask后端服务器地址
        changeOrigin: true, // 改变请求源
        rewrite: (path) => path.replace(/^\/api/, '/api') // 保持/api前缀
      },
      // 代理音乐文件
      '/music_files': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      // 代理封面图片
      '/covers': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      // 代理用户头像
      '/avatars': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      // 代理歌单封面
      '/static': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      // 代理背景图片
      '/backgrounds': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})