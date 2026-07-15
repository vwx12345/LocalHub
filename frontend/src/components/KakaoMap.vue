<template>
  <div class="map-layout">

    <div class="list-panel">
      <div class="list-panel-header">
        <div class="filter-buttons">
          <button @click="clickFilter('')" :class="['btn', { active: activeFilter === '' }]">전체보기</button>
          <button @click="clickFilter('restaurant')" :class="['btn', 'btn-res', { active: activeFilter === 'restaurant' }]">🍔 맛집</button>
          <button @click="clickFilter('tour')" :class="['btn', 'btn-tour', { active: activeFilter === 'tour' }]">🎯 관광지</button>
        </div>

        <div class="search-box">
          <input
            v-model="searchQuery"
            @keyup.enter="handleSearch"
            type="text"
            placeholder="역 이름, 지역, 식당 검색"
            class="search-input"
          />
          <button @click="handleSearch" class="btn search-btn">🔍</button>
        </div>
      </div>

      <div class="list-title-box">
        <h3 class="list-title">📍 검색된 장소 목록 <span>{{ placeList.length }}건</span></h3>
      </div>

      <div class="list-container">
        <div v-if="placeList.length === 0" class="empty-list">
          <span class="empty-emoji">🗺️</span>
          <p>이 주변에는 등록된 장소가 없습니다.<br>지도를 다른 곳으로 이동해보세요!</p>
        </div>

        <div
          v-for="p in placeList"
          :key="p.id"
          class="list-item"
          :class="{ 'is-active': activePlace && activePlace.id === p.id && isDetailOpen }"
          @click="selectPlace(p)"
        >
          <div class="list-item-img">
            <img :src="p.image_url || getDefaultImage(p.type)" alt="썸네일"/>
          </div>
          <div class="list-item-info">
            <span class="badge" :class="p.type">{{ p.type === 'restaurant' ? '맛집' : '관광지' }}</span>
            <h4>{{ p.title }}</h4>
            <p>{{ p.address }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="detail-panel" :class="{ 'is-open': isDetailOpen }" v-if="activePlace">
      <button class="close-btn" @click="closeDetail">✕</button>

      <div class="sidebar-content">
        <div class="place-image-box">
          <img :src="activePlace.image_url || getDefaultImage(activePlace.type)" class="place-image" />
        </div>

        <div class="place-info">
          <span class="badge" :class="activePlace.type">{{ activePlace.type === 'restaurant' ? '맛집' : '관광지' }}</span>
          <h2 class="place-title">{{ activePlace.title }}</h2>
          <p class="place-address">📍 {{ activePlace.address }}</p>
          <p class="place-hours">⏰ 영업시간: 매일 09:00 - 21:00 (준비중)</p>
        </div>

        <hr class="divider" />

        <div class="review-section">
          <h3>💬 방문자 리뷰 <span>{{ reviews.length }}</span></h3>

          <div class="review-list">
            <div v-if="reviews.length === 0" class="empty-review">
              아직 리뷰가 없습니다. 첫 리뷰를 남겨주세요!
            </div>

            <div v-for="rev in reviews" :key="rev.id" class="review-item">
              <div class="review-header">
                <div class="review-header-left">
                  <span class="review-author">{{ rev.nickname }}</span>
                  <span class="review-stars">
                    <span v-for="n in 5" :key="n" class="star" :class="{ 'is-empty': n > rev.rating }">
                      {{ n <= rev.rating ? '⭐' : '☆' }}
                    </span>
                  </span>
                </div>
                <div class="review-actions" v-if="editingReviewId !== rev.id && deletingReviewId !== rev.id">
                  <button class="action-btn" @click="startEditReview(rev)">수정</button>
                  <button class="action-btn danger" @click="startDeleteReview(rev)">삭제</button>
                </div>
              </div>

              <template v-if="editingReviewId !== rev.id">
                <p class="review-text">{{ rev.content }}</p>
                <span class="review-date">{{ new Date(rev.created_at).toLocaleDateString() }}</span>
              </template>

              <div v-else class="review-edit-box">
                <div class="review-edit-top">
                  <select v-model="editForm.rating" class="review-select">
                    <option value="5">⭐⭐⭐⭐⭐ 최고예요</option>
                    <option value="4">⭐⭐⭐⭐☆ 좋아요</option>
                    <option value="3">⭐⭐⭐☆☆ 보통이에요</option>
                    <option value="2">⭐⭐☆☆☆ 별로예요</option>
                    <option value="1">⭐☆☆☆☆ 최악이에요</option>
                  </select>
                  <input v-model="actionPassword" type="password" placeholder="비밀번호 확인" class="review-input-small" />
                </div>
                <input v-model="editForm.content" type="text" class="review-input-main" placeholder="내용 수정" />
                <div class="review-edit-buttons">
                  <button class="action-btn" @click="cancelReviewAction">취소</button>
                  <button class="review-submit-btn" @click="submitEditReview(rev)">저장</button>
                </div>
              </div>

              <div v-if="deletingReviewId === rev.id" class="review-delete-confirm">
                <input v-model="actionPassword" type="password" placeholder="비밀번호 입력" class="review-input-small" />
                <button class="action-btn" @click="cancelReviewAction">취소</button>
                <button class="action-btn danger" @click="confirmDeleteReview(rev)">확인</button>
              </div>
            </div>
          </div>

          <div class="review-input-box">
            <select v-model="reviewForm.rating" class="review-select">
              <option value="5">⭐⭐⭐⭐⭐ 최고예요</option>
              <option value="4">⭐⭐⭐⭐☆ 좋아요</option>
              <option value="3">⭐⭐⭐☆☆ 보통이에요</option>
              <option value="2">⭐⭐☆☆☆ 별로예요</option>
              <option value="1">⭐☆☆☆☆ 최악이에요</option>
            </select>
            <div class="review-inputs-top">
              <input v-model="reviewForm.nickname" type="text" placeholder="닉네임" class="review-input-small" />
              <input v-model="reviewForm.password" type="password" placeholder="비밀번호" class="review-input-small" />
            </div>
            <div class="review-inputs-bottom">
              <input
                v-model="reviewForm.content"
                @keyup.enter="submitReview"
                type="text"
                placeholder="솔직한 방문 후기를 남겨주세요!"
                class="review-input-main"
              />
              <button @click="submitReview" class="review-submit-btn primary">등록</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="map" class="map-area"></div>

  </div>
</template>

<script setup>
import { onMounted, ref, nextTick } from 'vue'
import axios from 'axios'

const isDetailOpen = ref(false)
const placeList = ref([])
const activePlace = ref(null)
const isBoundsUpdateActive = ref(true)

const activeFilter = ref('')
const searchQuery = ref('')
const markers = ref([])
let kakaoMap = null
let hoverOverlay = null

let selectedMarkerItem = null
let selectedLabelOverlay = null

const MARKER_COLORS = { restaurant: '#ff9800', tour: '#03a9f4' }
const SELECTED_MARKER_COLOR = '#212121'

// ⭐️ 추가된 부분: 카테고리별 기본 이미지 분기 처리 함수
const getDefaultImage = (type) => {
  if (type === 'tour') {
    // 관광지 기본 이미지 (여행/풍경 느낌)
    return 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=400';
  }
  // 맛집 기본 이미지
  return 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=400';
}

const createMarkerImage = (color, size = 36) => {
  const { kakao } = window
  const height = Math.round(size * 1.28)
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${height}" viewBox="0 0 36 46">
      <path d="M18 0C8.06 0 0 8.06 0 18c0 13.5 18 28 18 28s18-14.5 18-28C36 8.06 27.94 0 18 0z" fill="${color}"/>
      <circle cx="18" cy="18" r="7" fill="#ffffff"/>
    </svg>`
  const src = 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg)
  return new kakao.maps.MarkerImage(src, new kakao.maps.Size(size, height), {
    offset: new kakao.maps.Point(size / 2, height),
  })
}

const setMarkerSelected = (markerItem, isSelected) => {
  const image = isSelected ? createMarkerImage(SELECTED_MARKER_COLOR, 42) : markerItem.normalImage
  markerItem.marker.setImage(image)
}

const showSelectedLabel = (markerItem) => {
  const { kakao } = window
  hideSelectedLabel()

  const content = document.createElement('div')
  content.innerText = markerItem.place.title
  content.style.cssText = `
    padding: 6px 12px;
    background: ${SELECTED_MARKER_COLOR};
    color: #fff;
    font-size: 13px;
    font-weight: 700;
    border-radius: 8px;
    white-space: nowrap;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    font-family: 'Pretendard', sans-serif;
  `

  selectedLabelOverlay = new kakao.maps.CustomOverlay({
    content,
    position: markerItem.marker.getPosition(),
    yAnchor: 1.7,
    zIndex: 10,
  })
  selectedLabelOverlay.setMap(kakaoMap)
}

const hideSelectedLabel = () => {
  if (selectedLabelOverlay) {
    selectedLabelOverlay.setMap(null)
    selectedLabelOverlay = null
  }
}

const reviews = ref([])
const reviewForm = ref({ nickname: '', password: '', rating: 5, content: '' })

const editingReviewId = ref(null)
const deletingReviewId = ref(null)
const actionPassword = ref('')
const editForm = ref({ rating: 5, content: '' })

onMounted(() => {
  const { kakao } = window
  if (!kakao) return

  kakao.maps.load(async () => {
    const container = document.getElementById('map')
    const options = {
      center: new kakao.maps.LatLng(36.3504119, 127.3845475),
      level: 6,
    }
    kakaoMap = new kakao.maps.Map(container, options)

   hoverOverlay = new kakao.maps.CustomOverlay({
    zIndex: 5,
      yAnchor: 1.7 
    })
    kakao.maps.event.addListener(kakaoMap, 'idle', () => {
      if (isBoundsUpdateActive.value) {
        updateVisibleList()
      }
    })

    const params = new URLSearchParams(window.location.search)
    const placeId = params.get('place_id')

    await clickFilter('')

    if (placeId) {
      setTimeout(() => {
        const targetMarker = markers.value.find(m => m.place.id === Number(placeId))
        if (targetMarker) {
          selectPlace(targetMarker.place)
        }
      }, 300)
    }
  })
})

const loadDataFromServer = async (type, keyword) => {
  const { kakao } = window
  try {
    markers.value.forEach((m) => m.marker.setMap(null))
    markers.value = []

    selectedMarkerItem = null
    hideSelectedLabel()

    const url = `http://localhost:8000/api/places?type=${type}&keyword=${keyword}`
    const response = await axios.get(url)
    const places = response.data

    places.forEach((place) => {
      if (place.map_x && place.map_y) {
        const markerPosition = new kakao.maps.LatLng(place.map_y, place.map_x)
        const normalImage = createMarkerImage(MARKER_COLORS[place.type] || '#555555')
        const marker = new kakao.maps.Marker({
          position: markerPosition,
          title: place.title,
          image: normalImage,
        })

        marker.setMap(kakaoMap)
        const markerItem = { marker, place, normalImage }
        markers.value.push(markerItem)

        kakao.maps.event.addListener(marker, 'mouseover', () => {
          const content = `<div style="
            padding: 8px 16px;
            background: #ffffff;
            color: #212529;
            font-size: 13px;
            font-weight: 700;
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
            font-family: 'Pretendard', sans-serif;
            text-align: center;
            white-space: nowrap;
            border: 1px solid #e9ecef;
          ">${place.title}</div>`;

          hoverOverlay.setContent(content);
          hoverOverlay.setPosition(marker.getPosition());
          hoverOverlay.setMap(kakaoMap);
        });

        kakao.maps.event.addListener(marker, 'mouseout', () => {
          hoverOverlay.setMap(null);
        });
        kakao.maps.event.addListener(marker, 'click', () => selectPlace(place))
      }
    })
    return places
  } catch (error) {
    console.error('❌ 데이터 로드 실패:', error)
    return []
  }
}

const fetchReviews = async (placeId) => {
  try {
    const res = await axios.get(`http://localhost:8000/api/places/${placeId}/reviews`)
    reviews.value = res.data
  } catch (error) {
    console.error('❌ 리뷰 불러오기 실패:', error)
  }
}

const submitReview = async () => {
  if (!reviewForm.value.nickname || !reviewForm.value.password || !reviewForm.value.content) {
    alert('닉네임, 비밀번호, 내용을 모두 입력해주세요!')
    return
  }

  if (!Array.isArray(reviews.value)) {
    reviews.value = []
  }

  const tempReview = {
    id: Date.now(),
    nickname: reviewForm.value.nickname,
    rating: Number(reviewForm.value.rating),
    content: reviewForm.value.content,
    created_at: new Date().toISOString()
  }

  reviews.value.unshift(tempReview)

  const formData = { ...reviewForm.value }
  reviewForm.value = { nickname: '', password: '', rating: 5, content: '' }

  try {
    await axios.post('http://localhost:8000/api/reviews', {
      place_id: activePlace.value.id,
      nickname: formData.nickname,
      password: formData.password,
      rating: Number(formData.rating),
      content: formData.content
    })

    fetchReviews(activePlace.value.id)
  } catch (error) {
    console.error('❌ 리뷰 등록 실패:', error)
    reviews.value.shift()
    alert('리뷰 등록에 실패했습니다.')
  }
}

const startEditReview = (rev) => {
  editingReviewId.value = rev.id
  deletingReviewId.value = null
  actionPassword.value = ''
  editForm.value = { rating: rev.rating, content: rev.content }
}

const submitEditReview = async (rev) => {
  if (!actionPassword.value) {
    alert('비밀번호를 입력해주세요!')
    return
  }
  if (!editForm.value.content) {
    alert('내용을 입력해주세요!')
    return
  }

  try {
    await axios.put(`http://localhost:8000/api/reviews/${rev.id}`, {
      password: actionPassword.value,
      rating: Number(editForm.value.rating),
      content: editForm.value.content
    })

    await fetchReviews(activePlace.value.id)
    cancelReviewAction()
  } catch (error) {
    console.error('❌ 리뷰 수정 실패:', error)
    if (error.response && error.response.status === 401) {
      alert('비밀번호가 일치하지 않습니다.')
    } else {
      alert('리뷰 수정에 실패했습니다.')
    }
  }
}

const startDeleteReview = (rev) => {
  deletingReviewId.value = rev.id
  editingReviewId.value = null
  actionPassword.value = ''
}

const confirmDeleteReview = async (rev) => {
  if (!actionPassword.value) {
    alert('비밀번호를 입력해주세요!')
    return
  }

  try {
    await axios.delete(`http://localhost:8000/api/reviews/${rev.id}`, {
      data: { password: actionPassword.value }
    })

    reviews.value = reviews.value.filter((r) => r.id !== rev.id)
    cancelReviewAction()
  } catch (error) {
    console.error('❌ 리뷰 삭제 실패:', error)
    if (error.response && error.response.status === 401) {
      alert('비밀번호가 일치하지 않습니다.')
    } else {
      alert('리뷰 삭제에 실패했습니다.')
    }
  }
}

const cancelReviewAction = () => {
  editingReviewId.value = null
  deletingReviewId.value = null
  actionPassword.value = ''
}

const selectPlace = (place) => {
  const { kakao } = window
  activePlace.value = place
  isDetailOpen.value = true

  window.history.replaceState(null, '', `?place_id=${place.id}`)

  cancelReviewAction()
  fetchReviews(place.id)

  const markerItem = markers.value.find((m) => m.place.id === place.id)
  if (selectedMarkerItem && selectedMarkerItem !== markerItem) {
    setMarkerSelected(selectedMarkerItem, false)
  }
  if (markerItem) {
    setMarkerSelected(markerItem, true)
    showSelectedLabel(markerItem)
    selectedMarkerItem = markerItem
  }

  nextTick(() => {
    kakaoMap.relayout()
    const target = new kakao.maps.LatLng(place.map_y, place.map_x)
    kakaoMap.setLevel(4)
    kakaoMap.panTo(target)
  })
}

const closeDetail = () => {
  isDetailOpen.value = false
  activePlace.value = null
  window.history.replaceState(null, '', window.location.pathname)
  cancelReviewAction()

  if (selectedMarkerItem) {
    setMarkerSelected(selectedMarkerItem, false)
    selectedMarkerItem = null
  }
  hideSelectedLabel()

  nextTick(() => {
    kakaoMap.relayout()
  })
}

const updateVisibleList = () => {
  if (!kakaoMap) return
  const bounds = kakaoMap.getBounds()
  const visible = []
  markers.value.forEach(item => {
    if (bounds.contain(item.marker.getPosition())) visible.push(item.place)
  })
  placeList.value = visible
}

const clickFilter = async (type) => {
  activeFilter.value = type
  searchQuery.value = ''
  await loadDataFromServer(type, '')

  isBoundsUpdateActive.value = true
  closeDetail()

  setTimeout(updateVisibleList, 100)
}

const handleSearch = async () => {
  const { kakao } = window
  const kw = searchQuery.value.trim()

  if (!kw) {
    clickFilter(activeFilter.value)
    return
  }

  const dbPlaces = await loadDataFromServer(activeFilter.value, kw)

  if (dbPlaces.length === 1) {
    isBoundsUpdateActive.value = false
    placeList.value = dbPlaces
    selectPlace(dbPlaces[0])
  }
  else if (dbPlaces.length > 1) {
    const target = new kakao.maps.LatLng(dbPlaces[0].map_y, dbPlaces[0].map_x)
    kakaoMap.setLevel(4)
    kakaoMap.panTo(target)

    placeList.value = dbPlaces
    closeDetail()
    isBoundsUpdateActive.value = false
  }
  else {
    if (!kakao.maps.services) return
    const ps = new kakao.maps.services.Places()

    ps.keywordSearch(kw, async (data, status) => {
      if (status === kakao.maps.services.Status.OK) {
        const target = new kakao.maps.LatLng(data[0].y, data[0].x)
        kakaoMap.setLevel(4)
        kakaoMap.panTo(target)

        await loadDataFromServer(activeFilter.value, '')

        isBoundsUpdateActive.value = true
        closeDetail()

        setTimeout(updateVisibleList, 300)
      } else {
        alert("검색 결과가 없습니다.")
      }
    })
  }
}
</script>

<style scoped>
/* ⭐️ 웹 폰트 적용 (Pretendard) - 모던한 느낌의 핵심 */
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

* {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
  box-sizing: border-box;
}

/* 커스텀 스크롤바 (얇고 예쁘게) */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #e0e0e0; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #bdbdbd; }

.map-layout {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #f8f9fa;
  overflow: hidden;
  display: flex;
  align-items: stretch;
}

/* ---------- 1. 리스트 패널 ---------- */
.list-panel {
  width: 380px;
  flex-shrink: 0;
  height: 100%;
  background-color: #ffffff;
  border-right: 1px solid #edf2f7;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.04);
  z-index: 20;
  display: flex;
  flex-direction: column;
}

.list-panel-header {
  padding: 24px 20px 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: white;
  z-index: 2;
}

.filter-buttons { display: flex; gap: 8px; }
.btn { 
  padding: 10px 16px; 
  border-radius: 12px;
  border: 1px solid transparent; 
  background-color: #f1f3f5; 
  color: #495057; 
  cursor: pointer; 
  font-weight: 600; 
  font-size: 13px; 
  transition: all 0.2s ease; 
}
.btn:hover { background-color: #e9ecef; transform: translateY(-1px); }
.btn.active { background-color: #212529; color: white; box-shadow: 0 4px 12px rgba(33, 37, 41, 0.2); }
.btn-res.active { background-color: #ff922b; color: white; box-shadow: 0 4px 12px rgba(255, 146, 43, 0.2); }
.btn-tour.active { background-color: #339af0; color: white; box-shadow: 0 4px 12px rgba(51, 154, 240, 0.2); }

.search-box { display: flex; gap: 8px; }
.search-input { 
  flex: 1; 
  padding: 12px 16px; 
  border-radius: 12px; 
  border: 1px solid #e9ecef; 
  background: #f8f9fa;
  outline: none; 
  font-size: 14px; 
  transition: all 0.2s; 
}
.search-input:focus { border-color: #212529; background: #fff; box-shadow: 0 0 0 3px rgba(33, 37, 41, 0.1); }
.search-btn { flex-shrink: 0; padding: 0 16px; background-color: #212529; color: white; border-radius: 12px; font-size: 16px;}
.search-btn:hover { background-color: #343a40; }

.list-title-box { padding: 0 20px 12px 20px; border-bottom: 1px solid #f1f3f5; margin-bottom: 12px; }
.list-title { font-size: 15px; font-weight: 700; color: #212529; display: flex; justify-content: space-between; align-items: center; margin: 0; }
.list-title span { font-size: 13px; color: #868e96; font-weight: 500; }

.list-container { flex: 1; overflow-y: auto; padding: 0 20px 20px 20px; display: flex; flex-direction: column; gap: 12px; }
.empty-list { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #868e96; text-align: center; gap: 12px;}
.empty-emoji { font-size: 40px; }

.list-item { 
  display: flex; gap: 14px; padding: 14px; 
  border: 1px solid #f1f3f5; border-radius: 16px; 
  cursor: pointer; background: white;
  transition: all 0.2s ease; 
  align-items: center; 
}
.list-item:hover { transform: translateY(-2px); box-shadow: 0 8px 16px rgba(0,0,0,0.06); border-color: #e9ecef; }
.list-item.is-active { background: #f8f9fa; border-color: #212529; border-width: 2px; padding: 13px; }
.list-item-img { width: 68px; height: 68px; border-radius: 12px; overflow: hidden; flex-shrink: 0; background: #f1f3f5;}
.list-item-img img { width: 100%; height: 100%; object-fit: cover; }
.list-item-info { display: flex; flex-direction: column; gap: 6px; min-width: 0; }
.list-item-info h4 { margin: 0; font-size: 16px; font-weight: 700; color: #212529; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.list-item-info p { margin: 0; font-size: 13px; color: #868e96; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* 뱃지 디자인 */
.badge { font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 6px; display: inline-block; width: fit-content; letter-spacing: -0.3px;}
.badge.restaurant { background-color: #fff4e6; color: #fd7e14; }
.badge.tour { background-color: #e7f5ff; color: #228be6; }

/* ---------- 2. 상세정보 패널 ---------- */
.detail-panel {
  width: 0; flex-shrink: 0; height: 100%; background-color: #ffffff;
  border-right: 1px solid #edf2f7; box-shadow: 4px 0 24px rgba(0, 0, 0, 0.04);
  z-index: 15; overflow: hidden; position: relative;
  transition: width 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.detail-panel.is-open { width: 400px; }

.close-btn {
  position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.9); border: 1px solid #e9ecef;
  width: 36px; height: 36px; border-radius: 18px; cursor: pointer; font-size: 14px; font-weight: bold; color: #495057;
  display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.08); z-index: 60;
  backdrop-filter: blur(4px); transition: all 0.2s;
}
.close-btn:hover { background: #f8f9fa; transform: scale(1.05); }

.sidebar-content { padding: 24px; height: 100%; overflow-y: auto; box-sizing: border-box; width: 400px; }

.place-image-box { width: 100%; height: 220px; border-radius: 16px; overflow: hidden; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.place-image { width: 100%; height: 100%; object-fit: cover; }
.place-title { font-size: 26px; font-weight: 800; margin: 10px 0 8px 0; color: #212529; letter-spacing: -0.5px;}
.place-address, .place-hours { font-size: 14px; color: #495057; margin: 6px 0; display: flex; align-items: center; gap: 4px;}
.divider { border-top: 1px solid #f1f3f5; margin: 28px 0; border-bottom: none; border-left: none; border-right: none; }

.review-section h3 { font-size: 18px; font-weight: 700; margin-bottom: 20px; display: flex; align-items: center; gap: 8px;}
.review-section h3 span { font-size: 14px; color: #868e96; font-weight: 500; background: #f1f3f5; padding: 2px 8px; border-radius: 20px;}
.empty-review { font-size: 14px; color: #868e96; text-align: center; padding: 30px 0; background: #f8f9fa; border-radius: 12px;}

.review-item { background-color: #ffffff; padding: 20px; border: 1px solid #f1f3f5; border-radius: 16px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);}
.review-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; gap: 8px; }
.review-header-left { display: flex; align-items: center; gap: 10px; min-width: 0; }
.review-author { font-size: 14px; font-weight: 700; color: #212529; white-space: nowrap; }

/* ⭐️ 별점 스타일링 (글씨체 영향 없이 렌더링되게) */
.review-stars { display: inline-flex; gap: 1px; flex-shrink: 0; }
.star { font-size: 13px; line-height: 1; }
.star.is-empty { color: #868e96; }

.review-actions { display: flex; gap: 6px; flex-shrink: 0; }
.action-btn { background: #f8f9fa; border: 1px solid transparent; border-radius: 6px; padding: 6px 12px; font-size: 12px; font-weight: 600; color: #495057; cursor: pointer; transition: all 0.2s; }
.action-btn:hover { background: #e9ecef; }
.action-btn.danger { color: #fa5252; background: #fff5f5; }
.action-btn.danger:hover { background: #ffe3e3; }

.review-text { font-size: 14px; color: #495057; line-height: 1.6; margin: 0; }
.review-date { font-size: 12px; color: #adb5bd; display: block; margin-top: 10px; }

/* 리뷰 폼 입력창 공통 디자인 */
.review-input-box { display: flex; flex-direction: column; gap: 10px; margin-top: 32px; padding: 24px; background: #f8f9fa; border-radius: 16px; }
.review-inputs-top, .review-inputs-bottom { display: flex; gap: 8px; width: 100%; }
/* ⭐️ min-width: 0 추가로 입력창 잘림/삐져나감 방지 */
.review-input-small, .review-input-main, .review-select { 
  padding: 12px; font-size: 14px; border: 1px solid #e9ecef; border-radius: 10px; outline: none; transition: all 0.2s; background: white; min-width: 0;
}
.review-input-small:focus, .review-input-main:focus, .review-select:focus { border-color: #212529; box-shadow: 0 0 0 3px rgba(33, 37, 41, 0.1); }
.review-input-small { flex: 1; }
.review-input-main { flex: 1; }
.review-select { width: 100%; cursor: pointer; color: #495057; font-weight: 500;}

.review-submit-btn { padding: 0 20px; background-color: #212529; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; transition: background 0.2s;}
.review-submit-btn:hover { background-color: #343a40; }

/* 수정/삭제 폼 여백 */
.review-edit-box { display: flex; flex-direction: column; gap: 8px; margin-top: 12px; padding-top: 12px; border-top: 1px dashed #e9ecef;}
.review-delete-confirm { display: flex; gap: 8px; align-items: center; margin-top: 12px; padding-top: 12px; border-top: 1px dashed #e9ecef;}

/* ---------- 3. 지도 ---------- */
.map-area { flex: 1; height: 100%; min-width: 0; }
</style>