<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { getPosts } from '../api/post'
import PostItem from '../components/post/PostItem.vue'

const router = useRouter()

const posts = ref([])
const loading = ref(false)
const error = ref('')

async function fetchPosts() {
  try {
    loading.value = true
    error.value = ''

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

onMounted(fetchPosts)
</script>

<template>
  <main class="board-page">
    <div class="board-container">
      <section class="board-header">
        <div>
          <div class="title-row">
            <span class="title-icon">💬</span>
            <h1>지역 정보 게시판</h1>
          </div>

          <p>대전·충청 지역의 생활 정보와 유용한 이야기를 자유롭게 공유해 보세요.</p>
        </div>

        <button class="primary-button" @click="goCreate">
          <span>✏️</span>
          글쓰기
        </button>
      </section>

      <section class="board-card">
        <div class="list-header">
          <div>
            <h2>최근 게시글</h2>
            <p>새롭게 등록된 지역 이야기를 확인해 보세요.</p>
          </div>

          <span class="post-count">{{ posts.length }}건</span>
        </div>

        <div v-if="loading" class="state-box">
          <span class="state-icon">⏳</span>
          <p>게시글을 불러오는 중입니다.</p>
        </div>

        <div v-else-if="error" class="state-box error-state">
          <span class="state-icon">⚠️</span>
          <p>{{ error }}</p>

          <button class="secondary-button" @click="fetchPosts">다시 불러오기</button>
        </div>

        <div v-else-if="posts.length === 0" class="state-box">
          <span class="state-icon">📝</span>
          <h3>아직 작성된 게시글이 없습니다.</h3>
          <p>첫 번째 지역 이야기를 남겨보세요.</p>

          <button class="secondary-button" @click="goCreate">첫 글 작성하기</button>
        </div>

        <div v-else class="post-list">
          <PostItem v-for="post in posts" :key="post.id" :post="post" />
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.board-page {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background: #f8f9fa;
  box-sizing: border-box;
}

.board-container {
  width: min(1080px, calc(100% - 40px));
  margin: 0 auto;
  padding: 40px 0 60px;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 24px;
  margin-bottom: 24px;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 14px;
  background: #e7f5ff;
  font-size: 23px;
}

.board-header h1 {
  margin: 0;
  color: #212529;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.8px;
}

.board-header p {
  margin: 10px 0 0;
  color: #868e96;
  font-size: 15px;
  line-height: 1.6;
}

.primary-button,
.secondary-button {
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.2s ease;
}

.primary-button {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  padding: 13px 20px;
  background: #212529;
  color: #fff;
  box-shadow: 0 5px 14px rgba(33, 37, 41, 0.18);
}

.primary-button:hover {
  background: #343a40;
  transform: translateY(-2px);
}

.secondary-button {
  margin-top: 14px;
  padding: 10px 16px;
  background: #e9ecef;
  color: #495057;
}

.secondary-button:hover {
  background: #dee2e6;
}

.board-card {
  overflow: hidden;
  background: #fff;
  border: 1px solid #edf2f7;
  border-radius: 18px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.04);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 26px;
  border-bottom: 1px solid #f1f3f5;
}

.list-header h2 {
  margin: 0;
  color: #212529;
  font-size: 19px;
  font-weight: 800;
}

.list-header p {
  margin: 6px 0 0;
  color: #868e96;
  font-size: 13px;
}

.post-count {
  padding: 5px 11px;
  border-radius: 20px;
  background: #f1f3f5;
  color: #868e96;
  font-size: 13px;
  font-weight: 600;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 18px;
}

.state-box {
  min-height: 300px;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #868e96;
  text-align: center;
}

.state-box h3 {
  margin: 12px 0 4px;
  color: #495057;
  font-size: 17px;
}

.state-box p {
  margin: 6px 0 0;
  line-height: 1.6;
}

.state-icon {
  font-size: 40px;
}

.error-state {
  color: #fa5252;
}

@media (max-width: 700px) {
  .board-container {
    width: min(100% - 24px, 1080px);
    padding-top: 24px;
  }

  .board-header {
    align-items: stretch;
    flex-direction: column;
  }

  .primary-button {
    align-self: flex-end;
  }

  .board-header h1 {
    font-size: 25px;
  }
}
</style>
