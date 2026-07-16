```vue
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

  messages.value.push({
    role: 'user',
    text: userMessage,
  })

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
      throw new Error(
        data.detail ?? '챗봇 요청 실패',
      )
    }

    messages.value.push({
      role: 'bot',
      text: data.answer,
    })

    previousResponseId.value =
      data.response_id
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
    <div class="header">
      <div>
        <h3>🤖 AI 상담 챗봇</h3>
        <span>LocalHub 서비스 안내</span>
      </div>
    </div>

    <div class="messages">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.role]"
      >
        {{ msg.text }}
      </div>

      <div
        v-if="loading"
        class="message bot loading-message"
      >
        답변을 생성하고 있습니다...
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="message"
        type="text"
        placeholder="궁금한 내용을 입력하세요"
        :disabled="loading"
        @keyup.enter="sendMessage"
      />

      <button
        type="button"
        :disabled="loading || !message.trim()"
        @click="sendMessage"
      >
        {{ loading ? '대기' : '전송' }}
      </button>
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

  display: flex;
  flex-direction: column;

  overflow: hidden;

  background: #fff;
  color: #000;

  border: 1px solid #e9ecef;
  border-radius: 16px;

  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

/* Header */
.header {
  min-height: 70px;
  box-sizing: border-box;
  padding: 15px 20px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  background: #0068b7;
  color: #fff;
}

.header h3 {
  margin: 0;

  color: #fff;

  font-size: 18px;
  font-weight: 800;
}

.header span {
  display: block;
  margin-top: 4px;

  color: #fff;

  font-size: 12px;
  opacity: 0.9;
}

/* Messages */
.messages {
  flex: 1;

  display: flex;
  flex-direction: column;

  padding: 20px;
  overflow-y: auto;

  background: #f5f6f8;
  color: #000;
}

.message {
  box-sizing: border-box;
  max-width: 75%;
  margin-bottom: 12px;
  padding: 12px 15px;

  border-radius: 15px;

  color: #000;

  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;

  overflow-wrap: anywhere;
  white-space: pre-wrap;
}

.bot {
  align-self: flex-start;

  background: #fff;
  color: #000;

  border: 1px solid #d9dee3;
}

.user {
  align-self: flex-end;
  margin-left: auto;

  background: #0068b7;
  color: #fff;

  border: 1px solid #0068b7;
}

.loading-message {
  color: #343a40;
}

/* Input */
.input-area {
  display: flex;
  gap: 10px;

  padding: 15px;

  background: #fff;
  border-top: 1px solid #ddd;
}

.input-area input {
  flex: 1;
  min-width: 0;
  padding: 12px 15px;

  background: #fff;
  color: #000;

  border: 1px solid #adb5bd;
  border-radius: 20px;
  outline: none;

  font-size: 14px;
  font-weight: 500;
}

.input-area input::placeholder {
  color: #6c757d;
  opacity: 1;
}

.input-area input:focus {
  border-color: #0068b7;
  box-shadow: 0 0 0 3px rgba(0, 104, 183, 0.12);
}

.input-area input:disabled {
  background: #f1f3f5;
  color: #495057;
  cursor: not-allowed;
}

.input-area button {
  width: 70px;
  flex-shrink: 0;

  border: none;
  border-radius: 20px;

  background: #0068b7;
  color: #fff;

  cursor: pointer;

  font-size: 14px;
  font-weight: 700;
}

.input-area button:hover:not(:disabled) {
  background: #005a9e;
}

.input-area button:disabled {
  background: #adb5bd;
  cursor: not-allowed;
}

@media (max-width: 500px) {
  .chat-window {
    right: 12px;
    bottom: 90px;

    width: calc(100% - 24px);
    height: min(520px, calc(100vh - 120px));
  }
}
</style>
```
