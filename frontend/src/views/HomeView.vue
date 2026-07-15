<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { getPosts } from '../api/post'

import PostItem from '../components/post/PostItem.vue'

const posts = ref([])

const router = useRouter()

const loading = ref(false)

const error = ref(null)

async function fetchPosts() {
  try {
    loading.value = true

    posts.value = await getPosts()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function goCreate() {
  router.push('/posts/create')
}

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <main class="board-container">
    <div class="header">
      <h2>📌 지역 정보 게시판</h2>

      <button @click="goCreate">글쓰기</button>
    </div>

    <div v-if="loading">게시글을 불러오는 중입니다...</div>

    <div v-else-if="error">
      {{ error }}
    </div>

    <div v-else>
      <div v-if="posts.length === 0" class="empty">작성된 게시글이 없습니다.</div>

      <PostItem v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </main>
</template>

<style scoped>
.board-container {
  width: 80%;

  margin: 40px auto;
}

.header {
  display: flex;

  justify-content: space-between;

  align-items: center;

  margin-bottom: 20px;
}

button {
  padding: 10px 20px;

  border: none;

  border-radius: 8px;

  background: #1e88e5;

  color: white;

  cursor: pointer;
}

button:hover {
  background: #1565c0;
}

.empty {
  text-align: center;

  color: #777;

  margin-top: 50px;
}
</style>
