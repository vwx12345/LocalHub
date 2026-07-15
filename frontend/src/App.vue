<script setup>
import { ref } from 'vue'
import ChatBotButton from './components/chatbot/ChatBotButton.vue'
import ChatBotWindow from './components/chatbot/ChatBotWindow.vue'
import { RouterLink, RouterView } from 'vue-router'

const isOpen = ref(false)
</script>

<template>
  <div class="app-wrapper">
    <header class="top-nav">
      <div class="logo">
        <h2>LocalHub</h2>
      </div>
      <nav class="nav-links">
        <RouterLink to="/">게시판(Home)</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/map">지도(Map)</RouterLink>
      </nav>
    </header>

    <main class="main-content">
      <RouterView />
    </main>

    <ChatBotWindow v-if="isOpen" />
    <ChatBotButton @toggle="isOpen = !isOpen" />
  </div>
</template>

<style scoped>
/* 앱 전체를 감싸는 래퍼 */
.app-wrapper {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh; /* 화면 전체 높이 사용 */
  overflow: hidden;
}

/* 상단 헤더 디자인 */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px; /* 헤더 높이 고정 */
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  z-index: 1000; /* 지도보다 무조건 위에 있도록 설정 */
}

.logo h2 {
  margin: 0;
  color: #1e88e5;
  font-weight: 900;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-weight: 600;
  font-size: 15px;
  transition: color 0.2s ease;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #1e88e5; /* 클릭된 메뉴는 파란색으로 표시 */
}

/* 메인 뷰포트 영역 (헤더 60px을 제외한 나머지 공간 전체 차지) */
.main-content {
  flex-grow: 1;
  width: 100%;
  position: relative;
  overflow: hidden; /* 추가: 자식이 넘칠 경우 스크롤/밀림 방지 */
}
</style>
