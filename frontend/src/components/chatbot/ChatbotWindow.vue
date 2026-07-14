<script setup>
import { ref } from 'vue'

const message = ref('')

const messages = ref([
  {
    role: 'bot',
    text: '안녕하세요. 무엇을 도와드릴까요?',
  },
])

const loading = ref(false)

// OpenAI 대화 이어가기용
const previousResponseId = ref(null)

async function sendMessage() {
  const userMessage = message.value.trim()

  if (!userMessage || loading.value) {
    return
  }

  // 사용자 메시지 화면 표시
  messages.value.push({
    role: 'user',
    text: userMessage,
  })

  // 입력창 초기화
  message.value = ''

  loading.value = true

  try {
    const response = await fetch('/api/chatbot/chat', {
      method: 'POST',

      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify({
        message: userMessage,

        previous_response_id: previousResponseId.value,
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail ?? '챗봇 요청 실패')
    }

    // 챗봇 응답 추가

    messages.value.push({
      role: 'bot',

      text: data.answer,
    })

    // 다음 질문에서 이전 대화 연결

    previousResponseId.value = data.response_id
  } catch (error) {
    messages.value.push({
      role: 'bot',

      text: '죄송합니다. 현재 답변을 생성할 수 없습니다.',
    })

    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="chat-window">
    <!-- Header -->
    <div class="header">
      <div>
        <h3>🤖 AI 상담 챗봇</h3>

        <span> LocalHub 서비스 안내 </span>
      </div>
    </div>

    <!-- Messages -->

    <div class="messages">
      <div v-if="loading" class="message bot">답변을 생성하고 있습니다...</div>
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
        {{ msg.text }}
      </div>
    </div>

    <!-- Input -->

    <div class="input-area">
      <input v-model="message" placeholder="궁금한 내용을 입력하세요" @keyup.enter="sendMessage" />

      <button @click="sendMessage">전송</button>
    </div>
  </div>
</template>

<style scoped>
.chat-window {
  position: fixed;

  right: 30px;
  bottom: 110px;

  width: 380px;
  height: 520px;

  background: white;

  border-radius: 16px;

  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);

  display: flex;
  flex-direction: column;

  overflow: hidden;
}

/* Header */

.header {
  height: 70px;

  background: #0068b7;

  color: white;

  padding: 15px 20px;

  display: flex;

  justify-content: space-between;

  align-items: center;
}

.header h3 {
  margin: 0;

  font-size: 18px;
}

.header span {
  font-size: 12px;

  opacity: 0.8;
}

.header button {
  background: none;

  border: none;

  color: white;

  font-size: 24px;

  cursor: pointer;
}

/* Messages */

.messages {
  flex: 1;

  padding: 20px;

  overflow-y: auto;

  background: #f5f6f8;
}

.message {
  max-width: 75%;

  padding: 12px 15px;

  border-radius: 15px;

  margin-bottom: 12px;

  line-height: 1.5;

  font-size: 14px;
}

.bot {
  background: white;

  align-self: flex-start;

  border: 1px solid #ddd;
}

.user {
  background: #0068b7;

  color: white;

  margin-left: auto;
}

/* Input */

.input-area {
  display: flex;

  padding: 15px;

  border-top: 1px solid #ddd;

  gap: 10px;
}

.input-area input {
  flex: 1;

  padding: 12px;

  border-radius: 20px;

  border: 1px solid #ccc;

  outline: none;
}

.input-area button {
  width: 70px;

  border: none;

  border-radius: 20px;

  background: #0068b7;

  color: white;

  cursor: pointer;
}
</style>
