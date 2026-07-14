<script setup>
import { ref } from 'vue'

import ChatBotButton from './components/chatbot/ChatBotButton.vue'

import ChatBotWindow from './components/chatbot/ChatBotWindow.vue'

const isOpen = ref(false)
</script>

<template>
  <div>
    <h1>게시판 페이지</h1>

    <p>게시판 영역</p>

    <ChatBotWindow v-if="isOpen" />

    <ChatBotButton @toggle="isOpen = !isOpen" />
  </div>
</template>
