<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getPost, updatePost } from '../api/post'

const route = useRoute()
const router = useRouter()

const postId = route.params.id

const title = ref('')
const content = ref('')
const password = ref('')

const loading = ref(false)
const loadingPost = ref(true)

async function fetchPost() {
  try {
    loadingPost.value = true

    const post = await getPost(postId)

    title.value = post.title

    content.value = post.content
  } catch (err) {
    alert(err.message)

    router.push('/')
  } finally {
    loadingPost.value = false
  }
}

async function submitUpdate() {
  if (!title.value || !content.value || !password.value) {
    alert('모든 항목을 입력해주세요.')

    return
  }

  try {
    loading.value = true

    await updatePost(postId, {
      title: title.value,
      content: content.value,
      password: password.value,
    })

    alert('수정되었습니다.')

    router.push(`/posts/${postId}`)
  } catch (err) {
    alert(err.message)
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.back()
}

onMounted(() => {
  fetchPost()
})
</script>

<template>
  <main class="edit-container">
    <div v-if="loadingPost">게시글 정보를 불러오는 중...</div>

    <div v-else>
      <h2>📌 게시글 수정</h2>

      <div class="form">
        <input v-model="title" placeholder="제목" />

        <textarea v-model="content" placeholder="내용" />

        <input v-model="password" type="password" placeholder="비밀번호" />

        <div class="buttons">
          <button @click="submitUpdate" :disabled="loading">
            {{ loading ? '수정 중...' : '수정' }}
          </button>

          <button class="cancel" @click="goBack">취소</button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.edit-container {
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
}
</style>
