
<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { getPosts } from '../api/post'

const router = useRouter()

const posts = ref([])
const loading = ref(false)
const error = ref('')

const recentPosts = computed(() => {
  return posts.value.slice(0, 3)
})

const categoryInfo = {
  restaurant: {
    label: '맛집 추천',
    icon: '🍽️',
  },
  tour: {
    label: '관광지 추천',
    icon: '🗺️',
  },
  free: {
    label: '자유게시판',
    icon: '💬',
  },
}

async function fetchRecentPosts() {
  try {
    loading.value = true
    error.value = ''

    posts.value = await getPosts()
  } catch (err) {
    error.value =
      err.message ||
      '최근 게시글을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

function getCategory(post) {
  return categoryInfo[post.category] || categoryInfo.free
}

function goMap(type) {
  router.push({
    path: '/map',
    query: { type },
  })
}

function goBoard() {
  router.push('/board')
}

function goPost(postId) {
  router.push(`/posts/${postId}`)
}

function formatDate(date) {
  if (!date) return ''

  return new Intl.DateTimeFormat('ko-KR', {
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(date))
}

onMounted(fetchRecentPosts)
</script>

<template>
  <main class="home-page">
    <section class="hero-section">
      <div class="hero-content">
        <span class="hero-label">DAEJEON · CHUNGCHEONG</span>

        <h1>
          대전·충청의 맛집과 관광지를<br />
          한곳에서 찾아보세요
        </h1>

        <p>
          지도에서 원하는 장소를 찾고 지역 이용자들과 다양한 정보를 공유해 보세요.
        </p>

        <div class="hero-buttons">
          <button
            class="hero-button restaurant"
            @click="goMap('restaurant')"
          >
            🍽️ 맛집 찾기
          </button>

          <button
            class="hero-button tour"
            @click="goMap('tour')"
          >
            🗺️ 관광지 찾기
          </button>
        </div>
      </div>
    </section>

    <section class="home-section">
      <div class="section-header">
        <div>
          <span class="section-label">COMMUNITY</span>
          <h2>최근 지역 이야기</h2>
        </div>

        <button class="board-link" @click="goBoard">
          게시판 전체 보기
          <span>→</span>
        </button>
      </div>

      <div v-if="loading" class="recent-state">
        <span>⏳</span>
        <p>최근 게시글을 불러오는 중입니다.</p>
      </div>

      <div
        v-else-if="error"
        class="recent-state error-state"
      >
        <span>⚠️</span>
        <p>{{ error }}</p>

        <button
          type="button"
          @click="fetchRecentPosts"
        >
          다시 불러오기
        </button>
      </div>

      <div
        v-else-if="recentPosts.length === 0"
        class="recent-state"
      >
        <span>📝</span>
        <p>아직 작성된 게시글이 없습니다.</p>
      </div>

      <div
        v-else
        class="recent-post-list"
      >
        <article
          v-for="post in recentPosts"
          :key="post.id"
          class="recent-post-card"
          tabindex="0"
          @click="goPost(post.id)"
          @keyup.enter="goPost(post.id)"
        >
          <div class="recent-post-top">
            <span
              class="recent-category"
              :class="post.category || 'free'"
            >
              {{ getCategory(post).icon }}
              {{ getCategory(post).label }}
            </span>

            <span class="recent-date">
              {{ formatDate(post.created_at) }}
            </span>
          </div>

          <h3>{{ post.title }}</h3>

          <p>
            {{ post.content }}
          </p>

          <div class="recent-post-bottom">
            <span>👁 {{ post.views }}</span>
            <span class="recent-arrow">자세히 보기 →</span>
          </div>
        </article>
      </div>
    </section>
  </main>
</template>

<style scoped>
.home-page {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background: #f8f9fa;
}

.hero-section {
  width: 100%;
  padding: 80px 20px;
  box-sizing: border-box;
  background:
    radial-gradient(
      circle at 80% 20%,
      rgba(255, 146, 43, 0.18),
      transparent 30%
    ),
    linear-gradient(
      135deg,
      #fff9f2 0%,
      #ffffff 55%,
      #f1f8ff 100%
    );
  border-bottom: 1px solid #edf2f7;
}

.hero-content {
  width: min(1080px, 100%);
  margin: 0 auto;
}

.hero-label,
.section-label {
  display: block;
  margin-bottom: 12px;
  color: #f08c00;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 2px;
}

.hero-content h1 {
  margin: 0;
  color: #212529;
  font-size: clamp(36px, 5vw, 58px);
  font-weight: 900;
  line-height: 1.25;
  letter-spacing: -2px;
}

.hero-content p {
  max-width: 620px;
  margin: 22px 0 0;
  color: #6c757d;
  font-size: 17px;
  line-height: 1.8;
}

.hero-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 32px;
}

.hero-button {
  padding: 15px 24px;
  border: none;
  border-radius: 14px;
  color: #fff;
  cursor: pointer;
  font-size: 15px;
  font-weight: 800;
  transition: all 0.2s ease;
}

.hero-button:hover {
  transform: translateY(-2px);
}

.hero-button.restaurant {
  background: #ff922b;
  box-shadow: 0 7px 18px rgba(255, 146, 43, 0.25);
}

.hero-button.restaurant:hover {
  background: #f76707;
}

.hero-button.tour {
  background: #339af0;
  box-shadow: 0 7px 18px rgba(51, 154, 240, 0.22);
}

.hero-button.tour:hover {
  background: #228be6;
}

.home-section {
  width: min(1080px, calc(100% - 40px));
  margin: 0 auto;
  padding: 55px 0 70px;
}

.section-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  color: #212529;
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -1px;
}

.section-label {
  margin-bottom: 7px;
}

.board-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border: none;
  background: transparent;
  color: #495057;
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
}

.board-link:hover {
  color: #f08c00;
}

.recent-post-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.recent-post-card {
  min-width: 0;
  padding: 22px;
  background: #fff;
  border: 1px solid #edf2f7;
  border-radius: 18px;
  cursor: pointer;
  outline: none;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
}

.recent-post-card:hover,
.recent-post-card:focus {
  border-color: #dee2e6;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.075);
  transform: translateY(-3px);
}

.recent-post-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.recent-category {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 9px;
  border-radius: 7px;
  font-size: 11px;
  font-weight: 800;
}

.recent-category.restaurant {
  background: #fff4e6;
  color: #f76707;
}

.recent-category.tour {
  background: #e7f5ff;
  color: #228be6;
}

.recent-category.free {
  background: #f1f3f5;
  color: #495057;
}

.recent-date {
  flex-shrink: 0;
  color: #adb5bd;
  font-size: 12px;
}

.recent-post-card h3 {
  margin: 18px 0 0;
  overflow: hidden;
  color: #212529;
  font-size: 17px;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-post-card > p {
  display: -webkit-box;
  min-height: 44px;
  margin: 10px 0 0;
  overflow: hidden;
  color: #868e96;
  font-size: 13px;
  line-height: 1.65;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.recent-post-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #f1f3f5;
  color: #adb5bd;
  font-size: 12px;
}

.recent-arrow {
  color: #495057;
  font-weight: 700;
}

.recent-state {
  min-height: 190px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fff;
  border: 1px solid #edf2f7;
  border-radius: 18px;
  color: #868e96;
  text-align: center;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.04);
}

.recent-state > span {
  font-size: 36px;
}

.recent-state p {
  margin: 12px 0 0;
}

.recent-state button {
  margin-top: 14px;
  padding: 9px 14px;
  border: none;
  border-radius: 9px;
  background: #e9ecef;
  color: #495057;
  cursor: pointer;
  font-weight: 700;
}

.error-state {
  color: #fa5252;
}

@media (max-width: 850px) {
  .recent-post-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .hero-section {
    padding: 55px 20px;
  }

  .hero-content h1 {
    font-size: 34px;
    letter-spacing: -1.3px;
  }

  .hero-content p {
    font-size: 15px;
  }

  .hero-buttons {
    flex-direction: column;
  }

  .hero-button {
    width: 100%;
  }

  .home-section {
    width: calc(100% - 24px);
    padding-top: 40px;
  }

  .section-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .board-link {
    padding-left: 0;
  }
}
</style>