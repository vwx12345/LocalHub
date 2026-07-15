<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { createPost } from '../api/post'

const router = useRouter()

const title = ref('')
const content = ref('')
const password = ref('')

const loading = ref(false)

async function submitPost() {
  if (!title.value || !content.value || !password.value) {
    alert('모든 항목을 입력해주세요.')

    return
  }

  try {
    loading.value = true

    const post = await createPost({
      title: title.value,

      content: content.value,

      password: password.value,
    })

    alert('게시글이 작성되었습니다.')

    router.push(`/posts/${post.id}`)
  } catch (err) {
    alert(err.message)
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.back()
}
</script>

<template>
  <main class="create-container">
    <h2>📌 게시글 작성</h2>

    <div class="form">
      <input v-model="title" placeholder="제목" />

      <textarea v-model="content" placeholder="내용" />

      <input v-model="password" type="password" placeholder="비밀번호" />

      <div class="buttons">
        <button @click="submitPost" :disabled="loading">
          {{ loading ? '작성 중...' : '작성' }}
        </button>

        <button class="cancel" @click="goBack">취소</button>
      </div>
    </div>
  </main>
</template>

<style scoped>
.create-container {
  width: 80%;

  margin: 40px auto;
}

.form {
  display: flex;

  flex-direction: column;

  gap: 15px;
}

input {
  padding: 12px;

  font-size: 16px;
}

textarea {
  height: 250px;

  padding: 12px;

  resize: none;

  font-size: 16px;
}

.buttons {
  display: flex;

  gap: 10px;
}

button {
  padding: 10px 20px;

  border: none;

  border-radius: 6px;

  background: #1e88e5;

  color: white;

  cursor: pointer;
}

.cancel {
  background: #777;
}

button:disabled {
  opacity: 0.6;

  cursor: not-allowed;
}
</style>
