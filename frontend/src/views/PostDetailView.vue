<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getPost, getComments, deletePost } from '../api/post'

const route = useRoute()
const router = useRouter()

const post = ref(null)
const comments = ref([])

const loading = ref(true)

const error = ref(null)

const postId = route.params.id

async function fetchData() {
  try {
    loading.value = true

    post.value = await getPost(postId)

    comments.value = await getComments(postId)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function goEdit() {
  router.push(`/posts/${postId}/edit`)
}

async function removePost() {
  const password = prompt('게시글 비밀번호를 입력하세요')

  if (!password) {
    return
  }

  try {
    await deletePost(postId, password)

    alert('삭제되었습니다.')

    router.push('/')
  } catch (err) {
    alert(err.message)
  }
}

function formatDate(date) {
  return new Date(date).toLocaleString()
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <main class="detail-container">
    <div v-if="loading">불러오는 중...</div>

    <div v-else-if="error">
      {{ error }}
    </div>

    <div v-else>
      <section class="post">
        <h1>
          {{ post.title }}
        </h1>

        <div class="meta">
          조회수 {{ post.views }}

          |

          {{ formatDate(post.created_at) }}
        </div>

        <hr />

        <p class="content">
          {{ post.content }}
        </p>

        <div class="actions">
          <button @click="goEdit">수정</button>

          <button class="delete" @click="removePost">삭제</button>
        </div>
      </section>

      <CommentList :post-id="Number(postId)" :comments="comments" @refresh="fetchData" />
    </div>
  </main>
</template>

<style scoped>
.detail-container {
  width: 80%;

  margin: 40px auto;
}

.post {
  padding: 20px;
}

.meta {
  color: #777;

  margin: 10px 0;
}

.content {
  min-height: 200px;

  white-space: pre-line;
}

.actions {
  margin-top: 30px;

  display: flex;

  gap: 10px;
}

button {
  padding: 8px 16px;

  border: none;

  border-radius: 6px;

  cursor: pointer;
}

.delete {
  background: #e53935;

  color: white;
}

.comments {
  margin-top: 40px;
}

.comment {
  border-bottom: 1px solid #ddd;

  padding: 15px 0;
}

.reply {
  margin-left: 30px;

  color: #666;
}
</style>
