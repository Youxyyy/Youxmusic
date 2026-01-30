<template>
  <div class="about">
    <!-- 头部横幅 -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">关于 YouxMusic</h1>
        <p class="hero-subtitle">用音乐连接世界，让每一刻都充满旋律</p>
      </div>
    </div>

    <div class="container">
      <!-- 简介卡片 -->
      <div class="intro-section">
        <div class="intro-card">
          <div class="intro-icon">🎵</div>
          <h2>我们的使命</h2>
          <p>为用户提供最优质的音乐体验，让每个人都能轻松发现和分享喜爱的音乐。我们致力于打造一个简洁、美观、易用的音乐平台。</p>
        </div>
      </div>

      <!-- 特色功能卡片 -->
      <div class="features-section">
        <h2 class="section-title">平台特色</h2>
        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.id">
            <div class="feature-icon">{{ feature.icon }}</div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-desc">{{ feature.description }}</p>
          </div>
        </div>
      </div>

      <!-- 团队介绍 -->
      <div class="team-section">
        <h2 class="section-title">团队成员</h2>
        <div class="team-grid">
          <div class="team-card" v-for="member in team" :key="member.id">
            <div class="team-avatar">
              <img :src="member.avatar" :alt="member.name" />
            </div>
            <div class="team-info">
              <h3 class="team-name">{{ member.name }}</h3>
              <p class="team-role">{{ member.role }}</p>
              <p class="team-desc">{{ member.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 联系方式 -->
      <!-- <div class="contact-section">
        <div class="contact-card">
          <h2>联系我们</h2>
          <div class="contact-info">
            <div class="contact-item">
              <span class="contact-icon">📧</span>
              <span>contact@youxmusic.com</span>
            </div>
            <div class="contact-item">
              <span class="contact-icon">🌐</span>
              <span>www.youxmusic.com</span>
            </div>
            <div class="contact-item">
              <span class="contact-icon">📱</span>
              <span>关注我们的社交媒体</span>
            </div>
          </div>
        </div>
      </div> -->
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const features = ref([
  {
    id: 1,
    icon: '🎧',
    title: '海量曲库',
    description: '涵盖各种风格的音乐，满足不同用户的听歌需求'
  },
  {
    id: 2,
    icon: '📱',
    title: '跨平台支持',
    description: '支持Web、移动端等多平台，随时随地享受音乐'
  },
  {
    id: 3,
    icon: '🎨',
    title: '精美设计',
    description: '简洁优雅的界面设计，带来极致的视觉体验'
  },
  {
    id: 4,
    icon: '💝',
    title: '个性推荐',
    description: '智能推荐算法，为你发现更多喜欢的音乐'
  },
  {
    id: 5,
    icon: '🎵',
    title: '歌单管理',
    description: '创建和管理个人歌单，收藏喜爱的音乐'
  },
  {
    id: 6,
    icon: '🔊',
    title: '高品质音质',
    description: '提供高品质音频，享受纯净的音乐体验'
  }
])

const team = ref([
  {
    id: 1,
    name: '下次见Youx',
    role: '创始人 & 产品经理',
    avatar: 'https://cdn.jsdelivr.net/gh/Nikaple/avatar/default-boy.png',
    description: '热爱音乐，致力于打造最好的音乐平台'
  },
  {
    id: 2,
    name: '技术团队',
    role: '全栈开发工程师',
    avatar: 'https://cdn.jsdelivr.net/gh/Nikaple/avatar/default-girl.png',
    description: '精通Vue3、Flask等技术栈，追求极致的用户体验'
  },
  {
    id: 3,
    name: '设计团队',
    role: 'UI/UX设计师',
    avatar: 'https://cdn.jsdelivr.net/gh/Nikaple/avatar/default-boy.png',
    description: '专注于界面设计和交互体验，让产品更美观易用'
  }
])
</script>

<style scoped>
.about {
  background: #f8f9fa;
  min-height: 100vh;
}

/* 头部横幅 */
.hero-section {
  color: #2c3e50;
  padding: 50px 20px;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 20px;
  animation: fadeInUp 2s ease;
}

.hero-subtitle {
  font-size: 20px;
  opacity: 0.95;
  animation: fadeInUp 1s ease;
}

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

/* 简介卡片 */
.intro-section {
  padding: 60px 20px;
  max-width: 800px;
  margin: 0 auto;
}

.intro-card {
  background: white;
  padding: 50px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.intro-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.intro-card h2 {
  font-size: 32px;
  color: #333;
  margin-bottom: 20px;
}

.intro-card p {
  font-size: 16px;
  line-height: 1.8;
  color: #666;
}

/* 特色功能 */
.features-section {
  padding: 60px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 36px;
  color: #333;
  margin-bottom: 50px;
  font-weight: 700;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.feature-card {
  background: white;
  padding: 40px 30px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.feature-title {
  font-size: 20px;
  color: #333;
  margin-bottom: 12px;
  font-weight: 600;
}

.feature-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

/* 团队介绍 */
.team-section {
  padding: 60px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.team-card {
  background: white;
  padding: 30px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
}

.team-avatar {
  flex-shrink: 0;
}

.team-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f0f0f0;
}

.team-info {
  flex: 1;
}

.team-name {
  font-size: 20px;
  color: #333;
  margin-bottom: 8px;
  font-weight: 600;
}

.team-role {
  font-size: 14px;
  color: #667eea;
  margin-bottom: 10px;
  font-weight: 500;
}

.team-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

/* 联系方式 */
.contact-section {
  padding: 60px 20px 80px;
  max-width: 800px;
  margin: 0 auto;
}

.contact-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 50px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
}

.contact-card h2 {
  font-size: 32px;
  margin-bottom: 30px;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.contact-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 16px;
}

.contact-icon {
  font-size: 24px;
}

/* 响应式 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .intro-card {
    padding: 30px 20px;
  }

  .section-title {
    font-size: 28px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .team-card {
    flex-direction: column;
    text-align: center;
  }

  .contact-card {
    padding: 30px 20px;
  }
}
</style>