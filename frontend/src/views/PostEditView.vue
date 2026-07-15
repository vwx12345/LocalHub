
<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getPost, updatePost } from '../api/post'

const route = useRoute()
const router = useRouter()

const postId = route.params.id

const category = ref('free')
const placeId = ref(null)

const title = ref('')
const content = ref('')
const password = ref('')

const loadingPost = ref(true)
const submitting = ref(false)
const error = ref('')

async function fetchPost() {
  try {
    loadingPost.value = true
    error.value = ''

    const post = await getPost(postId)

    category.value = post.category || 'free'

    /* 기존 장소 연결을 보존 */
    placeId.value = post.place_id ?? null

    title.value = post.title
    content.value = post.content
  } catch (err) {
    error.value = err.message
  } finally {
    loadingPost.value = false
  }
}

async function submitUpdate() {
  const trimmedTitle = title.value.trim()
  const trimmedContent = content.value.trim()
  const trimmedPassword = password.value.trim()

  if (
    !category.value ||
    !trimmedTitle ||
    !trimmedContent ||
    !trimmedPassword
  ) {
    alert(
      '게시판 종류, 제목, 내용, 비밀번호를 모두 입력해주세요.',
    )
    return
  }

  try {
    submitting.value = true

    await updatePost(postId, {
      category: category.value,

      /* 화면에서는 수정하지 않지만 기존 장소 ID는 그대로 전송 */
      place_id: placeId.value,

      title: trimmedTitle,
      content: trimmedContent,
      password: trimmedPassword,
    })

    alert('게시글이 수정되었습니다.')
    router.push(`/posts/${postId}`)
  } catch (err) {
    alert(err.message)
  } finally {
    submitting.value = false
  }
}

function goBack() {
  router.back()
}

onMounted(fetchPost)
</script>

<template>
  <main class="form-page">
    <div class="form-container">
      <button
        type="button"
        class="back-button"
        @click="goBack"
      >
        ← 돌아가기
      </button>

      <div
        v-if="loadingPost"
        class="state-card"
      >
        <span>⏳</span>
        <p>게시글 정보를 불러오는 중입니다.</p>
      </div>

      <div
        v-else-if="error"
        class="state-card error-state"
      >
        <span>⚠️</span>
        <p>{{ error }}</p>
      </div>

      <section
        v-else
        class="form-card"
      >
        <header class="form-header">
          <div class="header-icon">🛠️</div>

          <div>
            <h1>게시글 수정</h1>

            <p>
              게시판 종류와 게시글 내용을 수정할 수 있습니다.
            </p>
          </div>
        </header>

        <div class="divider"></div>

        <form
          class="post-form"
          @submit.prevent="submitUpdate"
        >
          <label>
            <span>게시판 종류</span>

            <select v-model="category">
              <option value="restaurant">
                🍽️ 맛집 추천
              </option>

              <option value="tour">
                🗺️ 관광지 추천
              </option>

              <option value="free">
                💬 자유게시판
              </option>
            </select>
          </label>

          <div
            v-if="placeId"
            class="place-notice"
          >
            <span>📍</span>

            <div>
              <strong>장소 연결 유지 중</strong>

              <p>
                작성할 때 선택한 장소는 그대로 유지됩니다.
              </p>
            </div>
          </div>

          <label>
            <span>제목</span>

            <input
              v-model="title"
              type="text"
              maxlength="200"
              placeholder="게시글 제목"
            />

            <small>{{ title.length }} / 200</small>
          </label>

          <label>
            <span>내용</span>

            <textarea
              v-model="content"
              placeholder="게시글 내용"
            ></textarea>
          </label>

          <label class="password-field">
            <span>비밀번호 확인</span>

            <input
              v-model="password"
              type="password"
              maxlength="100"
              placeholder="작성할 때 설정한 비밀번호"
            />

            <small>
              기존 게시글의 비밀번호가 일치해야 수정됩니다.
            </small>
          </label>

          <div class="form-actions">
            <button
              type="button"
              class="cancel-button"
              @click="goBack"
            >
              취소
            </button>

            <button
              type="submit"
              class="submit-button"
              :disabled="submitting"
            >
              {{
                submitting
                  ? '수정 중...'
                  : '수정 내용 저장'
              }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </main>
</template>

<style scoped>
.form-page {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background: #f8f9fa;
}

.form-container {
  width: min(820px, calc(100% - 40px));
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
  font-weight: 650;
}

.back-button:hover {
  color: #212529;
}

.form-card,
.state-card {
  background: #fff;
  border: 1px solid #edf2f7;
  border-radius: 18px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.04);
}

.form-card {
  padding: 34px;
}

.state-card {
  min-height: 320px;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  color: #868e96;
  text-align: center;
}

.state-card span {
  font-size: 38px;
}

.error-state {
  color: #fa5252;
}

.form-header {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-icon {
  width: 48px;
  height: 48px;

  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  border-radius: 14px;
  background: #fff4e6;

  font-size: 23px;
}

.form-header h1 {
  margin: 0;

  color: #212529;

  font-size: 26px;
  font-weight: 800;
}

.form-header p {
  margin: 7px 0 0;

  color: #868e96;

  font-size: 14px;
}

.divider {
  height: 1px;
  margin: 28px 0;

  background: #f1f3f5;
}

.post-form {
  display: flex;
  flex-direction: column;
  gap: 23px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

label > span {
  color: #343a40;

  font-size: 14px;
  font-weight: 700;
}

input,
textarea,
select {
  box-sizing: border-box;
  width: 100%;
  padding: 14px;

  border: 1px solid #e9ecef;
  border-radius: 11px;
  outline: none;

  background: #f8f9fa;
  color: #343a40;

  font: inherit;

  transition: all 0.2s ease;
}

input:focus,
textarea:focus,
select:focus {
  border-color: #212529;
  background: #fff;

  box-shadow:
    0 0 0 3px rgba(33, 37, 41, 0.08);
}

select {
  cursor: pointer;
}

textarea {
  min-height: 300px;

  resize: vertical;

  line-height: 1.7;
}

label small {
  align-self: flex-end;

  color: #adb5bd;

  font-size: 11px;
}

.password-field small {
  align-self: flex-start;
}

/* 기존 장소 연결 안내 */
.place-notice {
  display: flex;
  align-items: flex-start;
  gap: 11px;

  padding: 14px 16px;

  background: #fff4e6;
  border: 1px solid #ffd8a8;
  border-radius: 12px;
}

.place-notice > span {
  font-size: 19px;
}

.place-notice strong {
  display: block;

  color: #e8590c;

  font-size: 13px;
}

.place-notice p {
  margin: 5px 0 0;

  color: #868e96;

  font-size: 12px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 9px;

  margin-top: 8px;
}

.cancel-button,
.submit-button {
  padding: 11px 18px;

  border: none;
  border-radius: 10px;

  cursor: pointer;

  font-weight: 700;
}

.cancel-button {
  background: #f1f3f5;
  color: #495057;
}

.cancel-button:hover {
  background: #e9ecef;
}

.submit-button {
  background: #212529;
  color: #fff;
}

.submit-button:hover:not(:disabled) {
  background: #343a40;
}

.submit-button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .form-container {
    width: min(100% - 24px, 820px);
    padding-top: 22px;
  }

  .form-card {
    padding: 24px 18px;
  }

  .form-actions {
    flex-direction: column-reverse;
  }
}
</style>
