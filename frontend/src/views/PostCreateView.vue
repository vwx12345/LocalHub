<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { createPost } from '../api/post'

const route = useRoute()
const router = useRouter()

const allowedCategories = ['restaurant', 'tour', 'free']
const initialCategory =
  typeof route.query.category === 'string' &&
  allowedCategories.includes(route.query.category)
    ? route.query.category
    : 'free'

const category = ref(initialCategory)
const title = ref('')
const content = ref('')
const password = ref('')
const loading = ref(false)

async function submitPost() {
  const trimmedTitle = title.value.trim()
  const trimmedContent = content.value.trim()
  const trimmedPassword = password.value.trim()

  if (!category.value || !trimmedTitle || !trimmedContent || !trimmedPassword) {
    alert('게시판 종류, 제목, 내용, 비밀번호를 모두 입력해주세요.')
    return
  }

  try {
    loading.value = true

    const post = await createPost({
      category: category.value,
      title: trimmedTitle,
      content: trimmedContent,
      password: trimmedPassword,
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
  <main class="form-page">
    <div class="form-container">
      <button class="back-button" @click="goBack">← 돌아가기</button>

      <section class="form-card">
        <header class="form-header">
          <div class="header-icon">✏️</div>

          <div>
            <h1>게시글 작성</h1>
            <p>지역 주민들과 공유하고 싶은 이야기를 작성해 주세요.</p>
          </div>
        </header>

        <div class="divider"></div>

        <form class="post-form" @submit.prevent="submitPost">
          <label>
            <span>게시판 종류</span>

            <select v-model="category">
              <option value="restaurant">🍽️ 맛집 추천</option>
              <option value="tour">🗺️ 관광지 추천</option>
              <option value="free">💬 자유게시판</option>
            </select>
          </label>

          <label>
            <span>제목</span>

            <input
              v-model="title"
              type="text"
              maxlength="200"
              placeholder="게시글 제목을 입력해주세요."
            />

            <small>{{ title.length }} / 200</small>
          </label>

          <label>
            <span>내용</span>

            <textarea
              v-model="content"
              placeholder="공유하고 싶은 지역 정보를 자세히 작성해주세요."
            ></textarea>
          </label>

          <label class="password-field">
            <span>비밀번호</span>

            <input
              v-model="password"
              type="password"
              maxlength="100"
              placeholder="수정·삭제 시 사용할 비밀번호"
            />

            <small>비밀번호는 게시글 수정과 삭제에 사용됩니다.</small>
          </label>

          <div class="form-actions">
            <button type="button" class="cancel-button" @click="goBack">취소</button>

            <button type="submit" class="submit-button" :disabled="loading">
              {{ loading ? '작성 중...' : '게시글 등록' }}
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

.form-card {
  padding: 34px;
  background: #fff;
  border: 1px solid #edf2f7;
  border-radius: 18px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.04);
}

.form-header {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 14px;
  background: #e7f5ff;
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
  box-shadow: 0 0 0 3px rgba(33, 37, 41, 0.08);
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

  .form-header {
    align-items: flex-start;
  }

  .form-actions {
    flex-direction: column-reverse;
  }
}
</style>
