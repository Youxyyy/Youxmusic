<template>
  <div class="contact">
    <div class="container">
      <h1 class="page-title">联系我们</h1>
      <div class="contact-content">
        <div class="contact-info">
          <h2>获取联系</h2>
          <div class="contact-item">
            <span class="contact-icon">📧</span>
            <div>
              <h3>邮箱</h3>
              <p>contact@techsite.com</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">📞</span>
            <div>
              <h3>电话</h3>
              <p>+86 400-123-4567</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">📍</span>
            <div>
              <h3>地址</h3>
              <p>北京市朝阳区科技园区创新大厦</p>
            </div>
          </div>
        </div>
        
        <div class="contact-form">
          <h2>发送消息</h2>
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label for="name">姓名</label>
              <input type="text" id="name" v-model="form.name" required>
            </div>
            <div class="form-group">
              <label for="email">邮箱</label>
              <input type="email" id="email" v-model="form.email" required>
            </div>
            <div class="form-group">
              <label for="subject">主题</label>
              <input type="text" id="subject" v-model="form.subject" required>
            </div>
            <div class="form-group">
              <label for="message">消息</label>
              <textarea id="message" v-model="form.message" rows="5" required></textarea>
            </div>
            <button type="submit" class="btn-submit">发送消息</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const submitForm = () => {
  alert('消息已发送！我们会尽快回复您。')
  // 在实际应用中，这里应该发送到后端API
  form.value = {
    name: '',
    email: '',
    subject: '',
    message: ''
  }
}
</script>

<style scoped>
.contact-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 50px;
  max-width: 1000px;
  margin: 0 auto;
}

.contact-info h2,
.contact-form h2 {
  margin-bottom: 30px;
  color: #2c3e50;
}

.contact-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 25px;
}

.contact-icon {
  font-size: 24px;
  margin-right: 15px;
  margin-top: 5px;
}

.contact-item h3 {
  margin-bottom: 5px;
  color: #2c3e50;
}

.contact-item p {
  color: #666;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #a7c5fb;
}

.btn-submit {
  background: linear-gradient(135deg, #64AEC2 0%, #a7c5fb 100%);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(106, 17, 203, 0.3);
}

@media (max-width: 768px) {
  .contact-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }
}
</style>