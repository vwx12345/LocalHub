<template>
  <div class="map-layout">

    <!-- 1. 왼쪽: 검색 + 필터 + 리스트 패널 (항상 보임) -->
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
            placeholder="역 이름, 지역, 랜드마크, 식당 검색"
            class="search-input"
          />
          <button @click="handleSearch" class="btn search-btn">🔍</button>
        </div>
      </div>

      <h3 class="list-title">📍 검색된 장소 목록 ({{ placeList.length }}건)</h3>

      <div class="list-container">
        <div v-if="placeList.length === 0" class="empty-list">
          이 주변에는 등록된 장소가 없습니다.<br>지도를 다른 곳으로 이동해보세요!
        </div>

        <div
          v-for="p in placeList"
          :key="p.id"
          class="list-item"
          :class="{ 'is-active': activePlace && activePlace.id === p.id && isDetailOpen }"
          @click="selectPlace(p)"
        >
          <div class="list-item-img">
            <img :src="p.image_url || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=400'" alt="썸네일"/>
          </div>
          <div class="list-item-info">
            <span class="badge" :class="p.type">{{ p.type === 'restaurant' ? '🍔 맛집' : '🎯 관광지' }}</span>
            <h4>{{ p.title }}</h4>
            <p>{{ p.address }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 2. 가운데: 클릭한 장소의 상세정보 사이드바 (선택 시에만 보임) -->
    <div class="detail-panel" :class="{ 'is-open': isDetailOpen }" v-if="activePlace">
      <button class="close-btn" @click="closeDetail">✕</button>

      <div class="sidebar-content">
        <div class="place-image-box">
          <img :src="activePlace.image_url || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=400'" class="place-image" />
        </div>

        <div class="place-info">
          <span class="badge" :class="activePlace.type">{{ activePlace.type === 'restaurant' ? '🍔 맛집' : '🎯 관광지' }}</span>
          <h2 class="place-title">{{ activePlace.title }}</h2>
          <p class="place-address">📍 {{ activePlace.address }}</p>
          <p class="place-hours">⏰ 영업시간: 매일 09:00 - 21:00 (준비중)</p>
        </div>

        <hr class="divider" />

        <div class="review-section">
          <h3>💬 방문자 리뷰 ({{ reviews.length }})</h3>

          <div class="review-list">
            <div v-if="reviews.length === 0" class="empty-review">
              아직 리뷰가 없습니다. 첫 리뷰를 남겨주세요!
            </div>

            <div v-for="rev in reviews" :key="rev.id" class="review-item">
              <div class="review-header">
                <span class="review-author">{{ rev.nickname }}</span>
                <span class="review-rating">{{ '⭐'.repeat(rev.rating) }}</span>
              </div>
              <p class="review-text">{{ rev.content }}</p>
              <span class="review-date">{{ new Date(rev.created_at).toLocaleDateString() }}</span>
            </div>
          </div>

          <div class="review-input-box">
            <div class="review-inputs-top">
              <input v-model="reviewForm.nickname" type="text" placeholder="닉네임" class="review-input-small" />
              <input v-model="reviewForm.password" type="password" placeholder="비밀번호" class="review-input-small" />
              <select v-model="reviewForm.rating" class="review-select">
                <option value="5">⭐⭐⭐⭐⭐</option>
                <option value="4">⭐⭐⭐⭐</option>
                <option value="3">⭐⭐⭐</option>
                <option value="2">⭐⭐</option>
                <option value="1">⭐</option>
              </select>
            </div>
            <div class="review-inputs-bottom">
              <input
                v-model="reviewForm.content"
                @keyup.enter="submitReview"
                type="text"
                placeholder="솔직한 방문 후기를 남겨주세요!"
                class="review-input-main"
              />
              <button @click="submitReview" class="review-submit-btn">등록</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. 오른쪽: 지도 (남은 공간을 모두 차지) -->
    <div id="map" class="map-area"></div>

  </div>
</template>

<script setup>
import { onMounted, ref, nextTick } from 'vue'
import axios from 'axios'

// 리스트 패널은 항상 열려있고, 상세정보 패널만 토글됩니다.
const isDetailOpen = ref(false)
const placeList = ref([])
const activePlace = ref(null)
const isBoundsUpdateActive = ref(true)

const activeFilter = ref('')
const searchQuery = ref('')
const markers = ref([])
let kakaoMap = null
let hoverInfowindow = null

const reviews = ref([])
const reviewForm = ref({ nickname: '', password: '', rating: 5, content: '' })

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

    hoverInfowindow = new kakao.maps.InfoWindow({ zIndex: 1, disableAutoPan: true })

    kakao.maps.event.addListener(kakaoMap, 'idle', () => {
      if (isBoundsUpdateActive.value) {
        updateVisibleList()
      }
    })

    await clickFilter('')

    const params = new URLSearchParams(window.location.search)
    const placeId = params.get('place_id')

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

    const url = `http://localhost:8000/api/places?type=${type}&keyword=${keyword}`
    const response = await axios.get(url)
    const places = response.data

    places.forEach((place) => {
      if (place.map_x && place.map_y) {
        const markerPosition = new kakao.maps.LatLng(place.map_y, place.map_x)
        const marker = new kakao.maps.Marker({ position: markerPosition, title: place.title })

        marker.setMap(kakaoMap)
        markers.value.push({ marker, place })

        kakao.maps.event.addListener(marker, 'mouseover', () => {
          hoverInfowindow.setContent(`<div style="padding: 6px 12px; font-size: 12px; font-weight: bold;">${place.title}</div>`)
          hoverInfowindow.open(kakaoMap, marker)
        })
        kakao.maps.event.addListener(marker, 'mouseout', () => hoverInfowindow.close())
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

// 장소를 선택하면 가운데 상세정보 패널이 열리고, 그만큼 지도 영역이 줄어듭니다.
// 이때 kakaoMap.relayout()을 호출해줘야 지도가 잘린 것처럼 보이지 않고 새 크기에 맞게 다시 그려집니다.
const selectPlace = (place) => {
  const { kakao } = window
  activePlace.value = place
  isDetailOpen.value = true

  window.history.replaceState(null, '', `?place_id=${place.id}`)

  fetchReviews(place.id)

  nextTick(() => {
    kakaoMap.relayout()
    const target = new kakao.maps.LatLng(place.map_y, place.map_x)
    kakaoMap.setLevel(4)
    kakaoMap.panTo(target)
  })
}

// 상세정보 패널을 닫으면 지도 영역이 다시 넓어지므로 relayout이 필요합니다.
const closeDetail = () => {
  isDetailOpen.value = false
  activePlace.value = null
  window.history.replaceState(null, '', window.location.pathname)

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
.map-layout {
  position: relative;
  width: 100%;
  height: 100%; /* 부모(main-content)가 이미 헤더 높이를 뺀 나머지 공간을 계산해줌 */
  background-color: #f5f5f5;
  overflow: hidden;
  display: flex;
  align-items: stretch;
}

/* ---------- 1. 리스트 패널 (왼쪽, 항상 보임) ---------- */
.list-panel {
  width: 360px;
  flex-shrink: 0;
  height: 100%;
  background-color: white;
  border-right: 1px solid #eee;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  z-index: 20;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.list-panel-header {
  padding: 20px 20px 0 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.filter-buttons { display: flex; gap: 8px; }
.search-box { display: flex; gap: 8px; }
.search-input { flex: 1; padding: 10px 16px; border-radius: 30px; border: 1px solid #e0e0e0; outline: none; font-size: 13px; transition: all 0.2s; }
.search-input:focus { border-color: #333; }
.btn { padding: 10px 16px; border-radius: 30px; border: none; background-color: #f2f2f2; color: #444; cursor: pointer; font-weight: bold; font-size: 13px; transition: all 0.2s ease; white-space: nowrap; }
.btn:hover { background-color: #e8e8e8; }
.btn.active { background-color: #333; color: white; }
.btn-res.active { background-color: #ff9800; color: white; }
.btn-tour.active { background-color: #03a9f4; color: white; }
.search-btn { flex-shrink: 0; padding: 10px 14px; background-color: #333; color: white; }
.search-btn:hover { background-color: #444; }

.list-title { font-size: 14px; font-weight: bold; margin: 16px 20px 12px 20px; padding-bottom: 12px; border-bottom: 1px solid #eee; flex-shrink: 0; }
.list-container { flex: 1; overflow-y: auto; padding: 0 20px 20px 20px; display: flex; flex-direction: column; gap: 12px; }
.empty-list { font-size: 13px; color: #888; text-align: center; padding: 40px 0; line-height: 1.6; }
.list-item { display: flex; gap: 12px; padding: 12px; border: 1px solid #eee; border-radius: 12px; cursor: pointer; transition: background 0.2s; align-items: center; }
.list-item:hover { background: #f9f9f9; border-color: #ccc; }
.list-item.is-active { background: #f2f7ff; border-color: #90caf9; }
.list-item-img { width: 60px; height: 60px; border-radius: 8px; overflow: hidden; flex-shrink: 0; }
.list-item-img img { width: 100%; height: 100%; object-fit: cover; }
.list-item-info { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.list-item-info h4 { margin: 0; font-size: 14px; font-weight: 800; color: #222; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.list-item-info p { margin: 0; font-size: 12px; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ---------- 2. 상세정보 패널 (가운데, 선택시만 보임) ---------- */
.detail-panel {
  width: 0;
  flex-shrink: 0;
  height: 100%;
  background-color: white;
  border-right: 1px solid #eee;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  z-index: 15;
  overflow: hidden;
  position: relative;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.detail-panel.is-open { width: 380px; }

.close-btn {
  position: absolute; top: 16px; right: 16px; background: white; border: 1px solid #ddd;
  width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-weight: bold; color: #666;
  display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); z-index: 60;
}

.sidebar-content { padding: 24px; height: 100%; overflow-y: auto; box-sizing: border-box; width: 380px; }

.place-image-box { width: 100%; height: 200px; border-radius: 12px; overflow: hidden; margin-bottom: 20px; }
.place-image { width: 100%; height: 100%; object-fit: cover; }
.badge { font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 20px; display: inline-block; width: fit-content; }
.badge.restaurant { background-color: #fff3e0; color: #ef6c00; border: 1px solid #ffe0b2; }
.badge.tour { background-color: #e1f5fe; color: #0288d1; border: 1px solid #b3e5fc; }
.place-title { font-size: 24px; font-weight: 800; margin: 8px 0; color: #111; }
.place-address, .place-hours { font-size: 14px; color: #666; margin: 4px 0; }
.divider { border-top: 1px solid #eee; margin: 24px 0; border-bottom: none; border-left: none; border-right: none; }

.review-section h3 { font-size: 16px; font-weight: 700; margin-bottom: 15px; }
.empty-review { font-size: 13px; color: #888; text-align: center; padding: 20px 0; }
.review-item { background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
.review-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
.review-author { font-size: 12px; font-weight: bold; color: #333; }
.review-rating { font-size: 11px; }
.review-text { font-size: 13px; color: #555; line-height: 1.5; margin: 0; }
.review-date { font-size: 10px; color: #aaa; display: block; margin-top: 6px; text-align: right; }

.review-input-box { display: flex; flex-direction: column; gap: 8px; margin-top: 24px; padding-top: 20px; border-top: 1px solid #eee; }
.review-inputs-top { display: flex; gap: 6px; margin-bottom: 2px; }
.review-input-small { flex: 1; padding: 8px; font-size: 12px; border: 1px solid #ddd; border-radius: 6px; outline: none; }
.review-select { padding: 8px; font-size: 12px; border: 1px solid #ddd; border-radius: 6px; outline: none; background: white; cursor: pointer; }
.review-inputs-bottom { display: flex; gap: 6px; }
.review-input-main { flex: 1; padding: 10px; font-size: 13px; border: 1px solid #ddd; border-radius: 6px; outline: none; }
.review-submit-btn { padding: 0 18px; background-color: #333; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }

/* ---------- 3. 지도 (오른쪽, 남은 공간 전부) ---------- */
.map-area {
  flex: 1;
  height: 100%;
  min-width: 0;
}
</style>