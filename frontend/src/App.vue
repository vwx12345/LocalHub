<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import ChatBotButton from './components/chatbot/ChatBotButton.vue'
import ChatBotWindow from './components/chatbot/ChatBotWindow.vue'

const isOpen = ref(false)
</script>

<template>
  <div>
    <header>
      <h1>게시판 페이지</h1>
      <p>게시판 영역</p>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/map">Map</RouterLink>
      </nav>
    </header>

    <main style="padding: 20px 0">
      <RouterView />
    </main>

    <ChatBotWindow v-if="isOpen" />
    <ChatBotButton @toggle="isOpen = !isOpen" />
  </div>
</template>
