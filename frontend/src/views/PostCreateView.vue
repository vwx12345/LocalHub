
<script setup>
import { ref, watch } from 'vue'
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

/* 장소 검색 관련 상태 */
const placeSearchQuery = ref('')
const placeResults = ref([])
const selectedPlace = ref(null)
const placeLoading = ref(false)
const placeError = ref('')
const hasSearched = ref(false)

/* 맛집 또는 관광지 검색 */
async function searchPlaces() {
  if (category.value === 'free') {
    placeResults.value = []
    selectedPlace.value = null
    return
  }

  const keyword = placeSearchQuery.value.trim()

  try {
    placeLoading.value = true
    placeError.value = ''
    hasSearched.value = true

    const query = new URLSearchParams({
      type: category.value,
      keyword,
    })

    const response = await fetch(
      `/api/places?${query.toString()}`,
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(
        data.detail ?? '장소 검색에 실패했습니다.',
      )
    }

    placeResults.value = Array.isArray(data)
      ? data
      : []
  } catch (err) {
    placeError.value =
      err.message ||
      '장소를 검색하지 못했습니다.'

    placeResults.value = []
  } finally {
    placeLoading.value = false
  }
}

/* 검색 결과에서 장소 선택 */
function selectPlace(place) {
  selectedPlace.value = place
  placeSearchQuery.value = place.title
  placeResults.value = []
  placeError.value = ''
}

/* 선택한 장소 취소 */
function clearSelectedPlace() {
  selectedPlace.value = null
  placeSearchQuery.value = ''
  placeResults.value = []
  placeError.value = ''
  hasSearched.value = false
}

/* 게시판 종류를 바꾸면 기존 장소 선택 초기화 */
watch(category, () => {
  clearSelectedPlace()
})

async function submitPost() {
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

  /* 맛집·관광지 추천은 장소 선택 필수 */
  if (
    category.value !== 'free' &&
    !selectedPlace.value
  ) {
    alert(
      category.value === 'restaurant'
        ? '추천할 맛집을 검색한 뒤 선택해주세요.'
        : '추천할 관광지를 검색한 뒤 선택해주세요.',
    )
    return
  }

  try {
    loading.value = true

    const post = await createPost({
      category: category.value,

      /* 자유게시판이면 null, 추천 게시판이면 장소 ID 저장 */
      place_id: selectedPlace.value
        ? Number(selectedPlace.value.id)
        : null,

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
      <button
        type="button"
        class="back-button"
        @click="goBack"
      >
        ← 돌아가기
      </button>

      <section class="form-card">
        <header class="form-header">
          <div class="header-icon">✏️</div>

          <div>
            <h1>게시글 작성</h1>

            <p>
              지역 주민들과 공유하고 싶은 이야기를
              작성해 주세요.
            </p>
          </div>
        </header>

        <div class="divider"></div>

        <form
          class="post-form"
          @submit.prevent="submitPost"
        >
          <!-- 게시판 종류 -->
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

          <!-- 맛집·관광지 검색 -->
          <section
            v-if="category !== 'free'"
            class="place-search-section"
          >
            <label>
              <span>
                {{
                  category === 'restaurant'
                    ? '추천 맛집'
                    : '추천 관광지'
                }}
              </span>

              <div class="place-search-box">
                <input
                  v-model="placeSearchQuery"
                  type="text"
                  :disabled="Boolean(selectedPlace)"
                  :placeholder="
                    category === 'restaurant'
                      ? '맛집 이름 또는 주소를 검색하세요.'
                      : '관광지 이름 또는 주소를 검색하세요.'
                  "
                  @keyup.enter.prevent="searchPlaces"
                />

                <button
                  type="button"
                  class="place-search-button"
                  :disabled="
                    placeLoading ||
                    Boolean(selectedPlace)
                  "
                  @click="searchPlaces"
                >
                  {{
                    placeLoading
                      ? '검색 중...'
                      : '검색'
                  }}
                </button>
              </div>

              <small class="place-help">
                검색어 없이 검색하면 등록된 장소 전체를
                확인할 수 있습니다.
              </small>
            </label>

            <!-- 선택된 장소 -->
            <div
              v-if="selectedPlace"
              class="selected-place"
            >
              <div class="selected-place-info">
                <span class="selected-label">
                  선택한 장소
                </span>

                <strong>
                  📍 {{ selectedPlace.title }}
                </strong>

                <p>
                  {{
                    selectedPlace.address ||
                    '주소 정보가 없습니다.'
                  }}
                </p>
              </div>

              <button
                type="button"
                class="clear-place-button"
                @click="clearSelectedPlace"
              >
                선택 변경
              </button>
            </div>

            <!-- 검색 오류 -->
            <p
              v-if="placeError"
              class="place-error"
            >
              {{ placeError }}
            </p>

            <!-- 검색 결과 -->
            <div
              v-if="
                !selectedPlace &&
                placeResults.length > 0
              "
              class="place-results"
            >
              <button
                v-for="place in placeResults"
                :key="place.id"
                type="button"
                class="place-result-item"
                @click="selectPlace(place)"
              >
                <div class="place-result-main">
                  <strong>{{ place.title }}</strong>

                  <span>
                    {{
                      place.address ||
                      '주소 정보가 없습니다.'
                    }}
                  </span>
                </div>

                <span class="select-text">
                  선택
                </span>
              </button>
            </div>

            <!-- 검색 결과 없음 -->
            <div
              v-else-if="
                hasSearched &&
                !placeLoading &&
                !placeError &&
                !selectedPlace &&
                placeResults.length === 0
              "
              class="place-empty"
            >
              <span>🔍</span>

              <p>검색 결과가 없습니다.</p>

              <small>
                다른 이름이나 주소로 검색해 보세요.
              </small>
            </div>
          </section>

          <!-- 제목 -->
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

          <!-- 내용 -->
          <label>
            <span>내용</span>

            <textarea
              v-model="content"
              placeholder="공유하고 싶은 지역 정보를 자세히 작성해주세요."
            ></textarea>
          </label>

          <!-- 비밀번호 -->
          <label class="password-field">
            <span>비밀번호</span>

            <input
              v-model="password"
              type="password"
              maxlength="100"
              placeholder="수정·삭제 시 사용할 비밀번호"
            />

            <small>
              비밀번호는 게시글 수정과 삭제에
              사용됩니다.
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
              :disabled="loading"
            >
              {{
                loading
                  ? '작성 중...'
                  : '게시글 등록'
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
  width: 48px;
  height: 48px;

  display: flex;
  align-items: center;
  justify-content: center;

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

  box-shadow:
    0 0 0 3px rgba(33, 37, 41, 0.08);
}

input:disabled {
  color: #868e96;
  cursor: not-allowed;
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

/* 장소 검색 영역 */
.place-search-section {
  display: flex;
  flex-direction: column;
  gap: 11px;

  padding: 18px;

  background: #fffaf5;
  border: 1px solid #ffe8cc;
  border-radius: 14px;
}

.place-search-box {
  display: flex;
  gap: 8px;
}

.place-search-box input {
  flex: 1;
}

.place-search-button {
  flex-shrink: 0;
  min-width: 78px;
  padding: 0 18px;

  border: none;
  border-radius: 11px;

  background: #212529;
  color: #fff;

  cursor: pointer;

  font-weight: 700;
}

.place-search-button:hover:not(:disabled) {
  background: #343a40;
}

.place-search-button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.place-help {
  align-self: flex-start;

  color: #adb5bd;

  font-size: 11px;
}

/* 선택된 장소 */
.selected-place {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;

  padding: 15px 16px;

  background: #fff;
  border: 1px solid #ffd8a8;
  border-radius: 12px;
}

.selected-place-info {
  min-width: 0;

  display: flex;
  flex-direction: column;
  gap: 5px;
}

.selected-label {
  color: #f08c00;

  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1px;
}

.selected-place strong {
  overflow: hidden;

  color: #e8590c;

  font-size: 14px;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.selected-place p {
  margin: 0;

  overflow: hidden;

  color: #868e96;

  font-size: 12px;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.clear-place-button {
  flex-shrink: 0;
  padding: 8px 11px;

  border: none;
  border-radius: 8px;

  background: #ffe8cc;
  color: #e8590c;

  cursor: pointer;

  font-size: 12px;
  font-weight: 700;
}

.clear-place-button:hover {
  background: #ffd8a8;
}

/* 검색 결과 */
.place-results {
  max-height: 270px;
  overflow-y: auto;

  display: flex;
  flex-direction: column;
  gap: 7px;

  padding: 7px;

  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 12px;
}

.place-result-item {
  width: 100%;
  padding: 12px 14px;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;

  border: 1px solid transparent;
  border-radius: 9px;

  background: #fff;

  cursor: pointer;
  text-align: left;

  transition: all 0.2s ease;
}

.place-result-item:hover {
  border-color: #ffd8a8;
  background: #fff9f2;
}

.place-result-main {
  min-width: 0;

  display: flex;
  flex-direction: column;
  gap: 5px;
}

.place-result-main strong {
  overflow: hidden;

  color: #212529;

  font-size: 14px;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.place-result-main span {
  overflow: hidden;

  color: #868e96;

  font-size: 12px;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.select-text {
  flex-shrink: 0;

  color: #f08c00;

  font-size: 12px;
  font-weight: 700;
}

.place-error {
  margin: 0;

  color: #fa5252;

  font-size: 13px;
}

/* 검색 결과 없음 */
.place-empty {
  min-height: 120px;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  background: #f8f9fa;
  border-radius: 11px;

  color: #868e96;
  text-align: center;
}

.place-empty > span {
  font-size: 28px;
}

.place-empty p {
  margin: 9px 0 0;

  font-size: 13px;
  font-weight: 700;
}

.place-empty small {
  margin-top: 5px;

  color: #adb5bd;

  font-size: 11px;
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

  .place-search-section {
    padding: 14px;
  }

  .place-search-box {
    flex-direction: column;
  }

  .place-search-button {
    min-height: 44px;
  }

  .selected-place {
    align-items: flex-start;
    flex-direction: column;
  }

  .selected-place p {
    white-space: normal;
  }

  .form-actions {
    flex-direction: column-reverse;
  }
}
</style>

