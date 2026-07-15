<template>
  <div class="map-layout">
    
    <div id="map" class="map-area"></div>

    <div class="filter-bar">
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
        <button @click="handleSearch" class="btn search-btn">🔍 검색</button>
      </div>
    </div>

    <div class="sidebar" :class="{ 'is-open': isSidebarOpen }">
      <button class="close-btn" @click="closeSidebar">✕</button>

      <div v-if="sidebarMode === 'list'" class="sidebar-content">
        <h3 class="list-title">📍 검색된 장소 목록 ({{ placeList.length }}건)</h3>
        
        <div class="list-container">
          <div v-if="placeList.length === 0" class="empty-list">
            이 주변에는 등록된 장소가 없습니다.<br>지도를 다른 곳으로 이동해보세요!
          </div>
          
          <div v-for="p in placeList" :key="p.id" class="list-item" @click="selectPlace(p)">
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

      <div v-else-if="sidebarMode === 'detail' && activePlace" class="sidebar-content">
        <button class="back-btn" v-if="placeList.length > 1" @click="goToListMode">← 목록으로 돌아가기</button>

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
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const isSidebarOpen = ref(false)
const sidebarMode = ref('list') 
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

  kakao.maps.load(async () => { // ⭐️ async 추가
    const container = document.getElementById('map')
    const options = {
      center: new kakao.maps.LatLng(36.3504119, 127.3845475), 
      level: 6,
    }
    kakaoMap = new kakao.maps.Map(container, options)
    
    hoverInfowindow = new kakao.maps.InfoWindow({ zIndex: 1, disableAutoPan: true })

    kakao.maps.event.addListener(kakaoMap, 'idle', () => {
      if (isBoundsUpdateActive.value && sidebarMode.value === 'list') {
        updateVisibleList()
      }
    })

    // ⭐️ 데이터 로딩을 완전히 기다린 후 URL 체크를 진행하도록 수정
    await clickFilter('') 

    const params = new URLSearchParams(window.location.search)
    const placeId = params.get('place_id')
    
    if (placeId) {
      // 마커 데이터가 생성될 때까지 아주 짧은 대기 (비동기 처리)
      setTimeout(() => {
        const targetMarker = markers.value.find(m => m.place.id === Number(placeId))
        if (targetMarker) {
          selectPlace(targetMarker.place)
        }
      }, 300) // 마커 생성을 기다려주는 안전 장치
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

// ⭐️ 즉각 반응형(Optimistic) 리뷰 등록 함수
const submitReview = async () => {
  if (!reviewForm.value.nickname || !reviewForm.value.password || !reviewForm.value.content) {
    alert('닉네임, 비밀번호, 내용을 모두 입력해주세요!')
    return
  }

  // 1. 방어 코드: reviews.value가 배열이 아니면 강제로 빈 배열로 초기화
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
  
  // 이제 안전하게 unshift 사용 가능
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
    // 에러 발생 시 아까 넣었던 임시 데이터 제거 (배열의 첫 번째 요소 제거)
    reviews.value.shift() 
    alert('리뷰 등록에 실패했습니다.')
  }
}

// ⭐️ 선택 시 URL에 정보 남기기
const selectPlace = (place) => {
  const { kakao } = window
  activePlace.value = place
  
  // URL 주소창 뒤에 ?place_id=1 형태로 기록을 남깁니다. (새로고침 방지용)
  window.history.replaceState(null, '', `?place_id=${place.id}`)

  sidebarMode.value = 'detail'
  isSidebarOpen.value = true
  
  const target = new kakao.maps.LatLng(place.map_y, place.map_x)
  kakaoMap.setLevel(4)
  kakaoMap.panTo(target) 

  fetchReviews(place.id)
}

// ⭐️ 목록 모드로 돌아갈 때 URL 파라미터 지우기
const goToListMode = () => {
  sidebarMode.value = 'list'
  window.history.replaceState(null, '', window.location.pathname)
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
  goToListMode() // 리스트 모드로 가면서 URL 초기화
  isSidebarOpen.value = true
  
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
    selectPlace(dbPlaces[0])
    isBoundsUpdateActive.value = false 
    placeList.value = dbPlaces
  } 
  else if (dbPlaces.length > 1) {
    const target = new kakao.maps.LatLng(dbPlaces[0].map_y, dbPlaces[0].map_x)
    kakaoMap.setLevel(4)
    kakaoMap.panTo(target)
    
    placeList.value = dbPlaces
    goToListMode()
    isSidebarOpen.value = true
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
        goToListMode()
        isSidebarOpen.value = true
        
        setTimeout(updateVisibleList, 300)
      } else {
        alert("검색 결과가 없습니다.")
      }
    })
  }
}

const closeSidebar = () => {
  isSidebarOpen.value = false
  window.history.replaceState(null, '', window.location.pathname) // URL 파라미터 초기화
}
</script>

<style scoped>
.map-layout { position: relative; width: 100%; height: calc(100vh - 100px); background-color: #f5f5f5; overflow: hidden; }
.map-area { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
.filter-bar { position: absolute; top: 20px; left: 20px; z-index: 10; display: flex; gap: 15px; align-items: center; }
.filter-buttons, .search-box { display: flex; gap: 8px; }
.search-input { padding: 10px 18px; border-radius: 30px; border: 1px solid #e0e0e0; outline: none; font-size: 13px; width: 220px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15); transition: all 0.2s; }
.search-input:focus { border-color: #333; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); }
.btn { padding: 10px 18px; border-radius: 30px; border: none; background-color: white; color: #444; cursor: pointer; font-weight: bold; font-size: 13px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15); transition: all 0.2s ease; }
.btn:hover { background-color: #f9f9f9; transform: translateY(-2px); }
.btn.active { background-color: #333; color: white; }
.btn-res.active { background-color: #ff9800; color: white; }
.btn-tour.active { background-color: #03a9f4; color: white; }
.search-btn:hover { background-color: #f0f0f0; }

.sidebar { position: absolute; top: 0; right: 0; width: 380px; height: 100%; background-color: white; z-index: 50; box-shadow: -4px 0 15px rgba(0, 0, 0, 0.1); transform: translateX(100%); transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.sidebar.is-open { transform: translateX(0); }
.sidebar-content { padding: 24px; height: 100%; overflow-y: auto; display: flex; flex-direction: column; }
.close-btn { position: absolute; top: 16px; right: 16px; background: white; border: 1px solid #ddd; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-weight: bold; color: #666; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); z-index: 60; }

.back-btn { background: none; border: none; color: #1e88e5; font-weight: bold; cursor: pointer; text-align: left; padding: 0; margin-bottom: 20px; font-size: 14px; }
.back-btn:hover { text-decoration: underline; }
.list-title { font-size: 16px; font-weight: bold; margin: 0 0 15px 0; padding-bottom: 15px; border-bottom: 1px solid #eee; }
.empty-list { font-size: 13px; color: #888; text-align: center; padding: 40px 0; line-height: 1.6; }
.list-container { display: flex; flex-direction: column; gap: 12px; }
.list-item { display: flex; gap: 12px; padding: 12px; border: 1px solid #eee; border-radius: 12px; cursor: pointer; transition: background 0.2s; align-items: center;}
.list-item:hover { background: #f9f9f9; border-color: #ccc; }
.list-item-img { width: 70px; height: 70px; border-radius: 8px; overflow: hidden; flex-shrink: 0; }
.list-item-img img { width: 100%; height: 100%; object-fit: cover; }
.list-item-info { display: flex; flex-direction: column; gap: 4px; }
.list-item-info h4 { margin: 0; font-size: 15px; font-weight: 800; color: #222; }
.list-item-info p { margin: 0; font-size: 12px; color: #666; }

.place-image-box { width: 100%; height: 200px; border-radius: 12px; overflow: hidden; margin-bottom: 20px;}
.place-image { width: 100%; height: 100%; object-fit: cover; }
.badge { font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 20px; display: inline-block; width: fit-content; }
.badge.restaurant { background-color: #fff3e0; color: #ef6c00; border: 1px solid #ffe0b2; }
.badge.tour { background-color: #e1f5fe; color: #0288d1; border: 1px solid #b3e5fc; }
.place-title { font-size: 24px; font-weight: 800; margin: 8px 0; color: #111; }
.place-address, .place-hours { font-size: 14px; color: #666; margin: 4px 0; }
.divider { border-top: 1px solid #eee; margin: 24px 0; border-bottom: none; border-left: none; border-right: none;}

.review-section h3 { font-size: 16px; font-weight: 700; margin-bottom: 15px; }
.empty-review { font-size: 13px; color: #888; text-align: center; padding: 20px 0; }
.review-item { background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 15px;}
.review-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
.review-author { font-size: 12px; font-weight: bold; color: #333; }
.review-rating { font-size: 11px; }
.review-text { font-size: 13px; color: #555; line-height: 1.5; margin: 0;}
.review-date { font-size: 10px; color: #aaa; display: block; margin-top: 6px; text-align: right; }

.review-input-box { display: flex; flex-direction: column; gap: 8px; margin-top: auto; padding-top: 20px;}
.review-inputs-top { display: flex; gap: 6px; margin-bottom: 2px; }
.review-input-small { flex: 1; padding: 8px; font-size: 12px; border: 1px solid #ddd; border-radius: 6px; outline: none; }
.review-select { padding: 8px; font-size: 12px; border: 1px solid #ddd; border-radius: 6px; outline: none; background: white; cursor: pointer; }
.review-inputs-bottom { display: flex; gap: 6px; }
.review-input-main { flex: 1; padding: 10px; font-size: 13px; border: 1px solid #ddd; border-radius: 6px; outline: none; }
.review-submit-btn { padding: 0 18px; background-color: #333; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;}
</style>