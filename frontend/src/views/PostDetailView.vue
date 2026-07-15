<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { deletePost, getComments, getPost } from '../api/post'
import CommentList from '../components/post/CommentList.vue'

const route = useRoute()
const router = useRouter()

const post = ref(null)
const comments = ref([])
const loading = ref(true)
const error = ref('')

const postId = route.params.id

const categoryInfo = computed(() => {
  const categories = {
    restaurant: { label: '맛집 추천', icon: '🍽️' },
    tour: { label: '관광지 추천', icon: '🗺️' },
    free: { label: '자유게시판', icon: '💬' },
  }

  return categories[post.value?.category] || categories.free
})

async function fetchData() {
  try {
    loading.value = true
    error.value = ''

    const [postData, commentData] = await Promise.all([getPost(postId), getComments(postId)])

    post.value = postData
    comments.value = commentData
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function refreshComments() {
  try {
    comments.value = await getComments(postId)
  } catch (err) {
    alert(err.message)
  }
}

function goList() {
  router.push({
    path: '/board',
    query: post.value?.category ? { category: post.value.category } : {},
  })
}

function goEdit() {
  router.push(`/posts/${postId}/edit`)
}

async function removePost() {
  const password = prompt('게시글 비밀번호를 입력하세요.')

  if (!password) return

  const confirmed = confirm(
    '게시글을 삭제하면 작성된 댓글도 함께 삭제됩니다.\n정말 삭제하시겠습니까?',
  )

  if (!confirmed) return

  try {
    await deletePost(postId, password)

    alert('게시글이 삭제되었습니다.')
    goList()
  } catch (err) {
    alert(err.message)
  }
}

function formatDate(date) {
  if (!date) return ''

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date))
}

onMounted(fetchData)
</script>

<template>
  <main class="detail-page">
    <div class="detail-container">
      <div v-if="loading" class="state-card">
        <span>⏳</span>
        <p>게시글을 불러오는 중입니다.</p>
      </div>

      <div v-else-if="error" class="state-card error-state">
        <span>⚠️</span>
        <p>{{ error }}</p>

        <button class="soft-button" @click="goList">목록으로 돌아가기</button>
      </div>

      <template v-else>
        <button class="back-button" @click="goList">← 게시판 목록</button>

        <article class="post-card">
          <header class="post-header">
            <span
              class="category-badge"
              :class="post.category || 'free'"
            >
              {{ categoryInfo.icon }} {{ categoryInfo.label }}
            </span>

            <h1>{{ post.title }}</h1>

            <div class="meta">
              <span>📅 {{ formatDate(post.created_at) }}</span>
              <span>👁 조회 {{ post.views }}</span>
            </div>
          </header>

          <div class="divider"></div>

          <div class="post-content">
            {{ post.content }}
          </div>

          <footer class="post-actions">
            <button class="soft-button" @click="goEdit">수정</button>

            <button class="danger-button" @click="removePost">삭제</button>
          </footer>
        </article>

        <CommentList :post-id="Number(postId)" :comments="comments" @refresh="refreshComments" />
      </template>
    </div>
  </main>
</template>

<style scoped>
.detail-page {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background: #f8f9fa;
}

.detail-container {
  width: min(900px, calc(100% - 40px));
  margin: 0 auto;
  padding: 34px 0 60px;
}

.back-button {
  margin-bottom: 16px;
  padding: 8px 0;
  background: none;
  border: none;
  color: #868e96;
  cursor: pointer;
  font-size: 14px;
  font-weight: 650;
}

.back-button:hover {
  color: #212529;
}

.post-card {
  padding: 34px;
  background: #fff;
  border: 1px solid #edf2f7;
  border-radius: 18px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.04);
}

.category-badge {
  display: inline-block;
  margin-bottom: 14px;
  padding: 5px 10px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 700;
}


.category-badge.restaurant {
  background: #fff4e6;
  color: #f76707;
}

.category-badge.tour {
  background: #e7f5ff;
  color: #228be6;
}

.category-badge.free {
  background: #f1f3f5;
  color: #495057;
}

.post-header h1 {
  margin: 0;
  color: #212529;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.8px;
  line-height: 1.35;
}

.meta {
  display: flex;
  gap: 18px;
  margin-top: 16px;
  color: #868e96;
  font-size: 13px;
}

.divider {
  height: 1px;
  margin: 28px 0;
  background: #f1f3f5;
}

.post-content {
  min-height: 230px;
  color: #343a40;
  font-size: 16px;
  line-height: 1.85;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.post-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 32px;
}

.soft-button,
.danger-button {
  padding: 9px 15px;
  border: 1px solid transparent;
  border-radius: 9px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 700;
  transition: all 0.2s ease;
}

.soft-button {
  background: #f1f3f5;
  color: #495057;
}

.soft-button:hover {
  background: #e9ecef;
}

.danger-button {
  background: #fff5f5;
  color: #fa5252;
}

.danger-button:hover {
  background: #ffe3e3;
}

.state-card {
  min-height: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fff;
  border: 1px solid #edf2f7;
  border-radius: 18px;
  color: #868e96;
  text-align: center;
}

.state-card span {
  font-size: 38px;
}

.error-state {
  color: #fa5252;
}

@media (max-width: 650px) {
  .detail-container {
    width: min(100% - 24px, 900px);
    padding-top: 22px;
  }

  .post-card {
    padding: 24px 20px;
  }

  
.category-badge.restaurant {
  background: #fff4e6;
  color: #f76707;
}

.category-badge.tour {
  background: #e7f5ff;
  color: #228be6;
}

.category-badge.free {
  background: #f1f3f5;
  color: #495057;
}

.post-header h1 {
    font-size: 24px;
  }

  .meta {
    flex-direction: column;
    gap: 5px;
  }
}
</style>
