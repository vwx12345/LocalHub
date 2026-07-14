<script setup>
import { ref } from 'vue'

const message = ref('')

async function sendMessage() {
  console.log('요청 시작:', message.value)

  try {
    const response = await fetch('/api/chatbot/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message.value,
        previous_response_id: null,
      }),
    })

    console.log('status:', response.status)

    const data = await response.json()

    console.log('응답:', data)
  } catch (error) {
    console.error('요청 실패:', error)
  }
}
</script>

<template>
  <div>
    <h2>🤖 ChatBot 테스트</h2>

    <input v-model="message" placeholder="메시지 입력" />

    <button @click="sendMessage">전송</button>
  </div>
</template>
