
<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import {
  deletePost,
  getComments,
  getPost,
} from '../api/post'

import CommentList from '../components/post/CommentList.vue'

const route = useRoute()
const router = useRouter()

const postId = route.params.id

const post = ref(null)
const comments = ref([])

/* 게시글에 연결된 장소 정보 */
const place = ref(null)
const placeLoading = ref(false)
const placeError = ref('')

const loading = ref(true)
const error = ref('')

const categoryInfo = computed(() => {
  const categories = {
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

  return (
    categories[post.value?.category] ||
    categories.free
  )
})

/*
 * place 객체에서 프로젝트마다 필드명이 다를 수 있어
 * title 또는 name을 모두 처리합니다.
 */
const placeTitle = computed(() => {
  if (!place.value) return ''

  return (
    place.value.title ||
    place.value.name ||
    '장소 정보'
  )
})

const placeAddress = computed(() => {
  if (!place.value) return ''

  return (
    place.value.address ||
    place.value.road_address ||
    place.value.roadAddress ||
    ''
  )
})

/* 장소 한 개 조회 */
async function fetchPlace(placeId) {
  if (!placeId) {
    place.value = null
    return
  }

  try {
    placeLoading.value = true
    placeError.value = ''

    const response = await fetch(
      `/api/places/${placeId}`,
    )

    let data = null

    try {
      data = await response.json()
    } catch {
      data = null
    }

    if (!response.ok) {
      throw new Error(
        data?.detail ||
        '장소 정보를 불러오지 못했습니다.',
      )
    }

    place.value = data
  } catch (err) {
    /*
     * 장소 조회 실패가 게시글 전체 오류로 이어지지 않게
     * 장소 영역에서만 오류를 처리합니다.
     */
    place.value = null

    placeError.value =
      err.message ||
      '장소 정보를 불러오지 못했습니다.'
  } finally {
    placeLoading.value = false
  }
}

async function fetchData() {
  try {
    loading.value = true
    error.value = ''

    const [postData, commentData] =
      await Promise.all([
        getPost(postId),
        getComments(postId),
      ])

    post.value = postData
    comments.value = commentData

    /*
     * 게시글에 place_id가 있을 때만
     * 장소 정보를 추가로 조회합니다.
     */
    if (postData.place_id) {
      await fetchPlace(postData.place_id)
    }
  } catch (err) {
    error.value =
      err.message ||
      '게시글을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

async function refreshComments() {
  try {
    comments.value =
      await getComments(postId)
  } catch (err) {
    alert(err.message)
  }
}

function goList() {
  router.push({
    path: '/board',

    query: post.value?.category
      ? {
          category: post.value.category,
        }
      : {},
  })
}

function goEdit() {
  router.push(
    `/posts/${postId}/edit`,
  )
}

/* 연결된 장소를 지도에서 열기 */
function goPlaceMap() {
  if (!post.value?.place_id) return

  router.push({
    path: '/map',

    query: {
      place_id: post.value.place_id,
    },
  })
}

async function removePost() {
  const password = prompt(
    '게시글 비밀번호를 입력하세요.',
  )

  if (!password) return

  const confirmed = confirm(
    '게시글을 삭제하면 작성된 댓글도 함께 삭제됩니다.\n정말 삭제하시겠습니까?',
  )

  if (!confirmed) return

  try {
    await deletePost(
      postId,
      password,
    )

    alert('게시글이 삭제되었습니다.')
    goList()
  } catch (err) {
    alert(err.message)
  }
}

function formatDate(date) {
  if (!date) return ''

  return new Intl.DateTimeFormat(
    'ko-KR',
    {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    },
  ).format(new Date(date))
}

onMounted(fetchData)
</script>

<template>
  <main class="detail-page">
    <div class="detail-container">
      <div
        v-if="loading"
        class="state-card"
      >
        <span>⏳</span>

        <p>
          게시글을 불러오는 중입니다.
        </p>
      </div>

      <div
        v-else-if="error"
        class="state-card error-state"
      >
        <span>⚠️</span>

        <p>{{ error }}</p>

        <button
          type="button"
          class="soft-button"
          @click="goList"
        >
          목록으로 돌아가기
        </button>
      </div>

      <template v-else>
        <button
          type="button"
          class="back-button"
          @click="goList"
        >
          ← 게시판 목록
        </button>

        <article class="post-card">
          <header class="post-header">
            <span
              class="category-badge"
              :class="
                post.category || 'free'
              "
            >
              {{ categoryInfo.icon }}
              {{ categoryInfo.label }}
            </span>

            <h1>{{ post.title }}</h1>

            <div class="meta">
              <span>
                📅
                {{ formatDate(post.created_at) }}
              </span>

              <span>
                👁 조회 {{ post.views }}
              </span>
            </div>
          </header>

          <!-- 연결된 장소 -->
          <section
            v-if="post.place_id"
            class="place-section"
          >
            <div
              v-if="placeLoading"
              class="place-state"
            >
              <span>⏳</span>
              장소 정보를 불러오는 중입니다.
            </div>

            <button
              v-else-if="place"
              type="button"
              class="place-card"
              @click="goPlaceMap"
            >
              <div class="place-icon">
                {{
                  post.category ===
                  'restaurant'
                    ? '🍽️'
                    : '📍'
                }}
              </div>

              <div class="place-info">
                <span class="place-label">
                  {{
                    post.category ===
                    'restaurant'
                      ? '추천 맛집'
                      : '추천 장소'
                  }}
                </span>

                <strong>
                  {{ placeTitle }}
                </strong>

                <p v-if="placeAddress">
                  {{ placeAddress }}
                </p>
              </div>

              <div class="place-map-link">
                지도에서 보기
                <span>→</span>
              </div>
            </button>

            <div
              v-else-if="placeError"
              class="place-error"
            >
              <span>⚠️</span>

              <div>
                <strong>
                  연결된 장소 정보를 불러오지 못했습니다.
                </strong>

                <p>{{ placeError }}</p>
              </div>

              <button
                type="button"
                @click="goPlaceMap"
              >
                지도 열기
              </button>
            </div>
          </section>

          <div class="divider"></div>

          <div class="post-content">
            {{ post.content }}
          </div>

          <footer class="post-actions">
            <button
              type="button"
              class="soft-button"
              @click="goEdit"
            >
              수정
            </button>

            <button
              type="button"
              class="danger-button"
              @click="removePost"
            >
              삭제
            </button>
          </footer>
        </article>

        <CommentList
          :post-id="Number(postId)"
          :comments="comments"
          @refresh="refreshComments"
        />
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
  width: min(
    900px,
    calc(100% - 40px)
  );

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

  box-shadow:
    0 8px 28px
    rgba(0, 0, 0, 0.04);
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

/* 장소 영역 */
.place-section {
  margin-top: 24px;
}

.place-card {
  box-sizing: border-box;
  width: 100%;
  padding: 17px 18px;

  display: flex;
  align-items: center;
  gap: 14px;

  border: 1px solid #ffd8a8;
  border-radius: 14px;

  background: #fffaf5;

  cursor: pointer;
  text-align: left;

  transition:
    transform 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.place-card:hover {
  transform: translateY(-2px);

  border-color: #ffa94d;

  box-shadow:
    0 8px 22px
    rgba(247, 103, 7, 0.1);
}

.place-icon {
  width: 44px;
  height: 44px;

  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  border-radius: 12px;

  background: #ffe8cc;

  font-size: 21px;
}

.place-info {
  min-width: 0;
  flex: 1;

  display: flex;
  flex-direction: column;
  gap: 4px;
}

.place-label {
  color: #f08c00;

  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.6px;
}

.place-info strong {
  overflow: hidden;

  color: #212529;

  font-size: 15px;
  font-weight: 800;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.place-info p {
  margin: 0;

  overflow: hidden;

  color: #868e96;

  font-size: 12px;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.place-map-link {
  display: flex;
  align-items: center;
  gap: 5px;

  flex-shrink: 0;

  color: #e8590c;

  font-size: 12px;
  font-weight: 750;
}

.place-map-link span {
  font-size: 15px;
}

.place-state {
  padding: 18px;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  border: 1px solid #e9ecef;
  border-radius: 13px;

  background: #f8f9fa;
  color: #868e96;

  font-size: 13px;
}

.place-error {
  padding: 16px;

  display: flex;
  align-items: flex-start;
  gap: 10px;

  border: 1px solid #ffe3e3;
  border-radius: 13px;

  background: #fff5f5;
  color: #fa5252;
}

.place-error > span {
  font-size: 18px;
}

.place-error div {
  flex: 1;
}

.place-error strong {
  display: block;

  font-size: 13px;
}

.place-error p {
  margin: 5px 0 0;

  color: #868e96;

  font-size: 11px;
}

.place-error button {
  flex-shrink: 0;
  padding: 7px 10px;

  border: none;
  border-radius: 8px;

  background: #ffe3e3;
  color: #e03131;

  cursor: pointer;

  font-size: 11px;
  font-weight: 700;
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

  overflow-wrap: anywhere;
  white-space: pre-wrap;
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
    width: min(
      100% - 24px,
      900px
    );

    padding-top: 22px;
  }

  .post-card {
    padding: 24px 20px;
  }

  .post-header h1 {
    font-size: 24px;
  }

  .meta {
    flex-direction: column;
    gap: 5px;
  }

  .place-card {
    align-items: flex-start;
  }

  .place-info p {
    white-space: normal;
  }

  .place-map-link {
    display: none;
  }

  .place-error {
    flex-wrap: wrap;
  }

  .place-error button {
    margin-left: 28px;
  }
}
</style>

