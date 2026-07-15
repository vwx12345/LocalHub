<template>
  <div class="map-container">
    <div class="filter-buttons">
      <button @click="fetchPlaces('')" :class="['btn', { active: activeFilter === '' }]">
        전체보기
      </button>
      <button
        @click="fetchPlaces('restaurant')"
        :class="['btn', 'btn-res', { active: activeFilter === 'restaurant' }]"
      >
        🍔 맛집
      </button>
      <button
        @click="fetchPlaces('tour')"
        :class="['btn', 'btn-tour', { active: activeFilter === 'tour' }]"
      >
        🎯 관광지
      </button>
    </div>

    <div id="map" class="map-area"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

// 현재 어떤 필터가 선택되었는지 저장하는 상태 변수 ('', 'restaurant', 'tour')
const activeFilter = ref('')
const markers = ref([])
let kakaoMap = null

onMounted(() => {
  const { kakao } = window
  if (!kakao) return

  kakao.maps.load(() => {
    const container = document.getElementById('map')
    const options = {
      center: new kakao.maps.LatLng(36.3504119, 127.3845475), // 대전시청
      level: 7,
    }
    kakaoMap = new kakao.maps.Map(container, options)
    fetchPlaces('') // 초기 전체 데이터 로드
  })
})

const fetchPlaces = async (type) => {
  const { kakao } = window

  // ⭐️ 핵심: 내가 클릭한 버튼을 '활성화 상태'로 변경합니다.
  activeFilter.value = type

  try {
    // 기존 마커 제거
    markers.value.forEach((marker) => marker.setMap(null))
    markers.value = []

    // 백엔드로 데이터 요청
    const response = await axios.get(`http://localhost:8000/api/places?type=${type}`)
    const places = response.data

    console.log(`🎒 백엔드 수신 (${type || '전체'}):`, places)

    places.forEach((place) => {
      if (place.map_x && place.map_y) {
        const markerPosition = new kakao.maps.LatLng(place.map_y, place.map_x)
        const marker = new kakao.maps.Marker({
          position: markerPosition,
          title: place.title,
        })

        marker.setMap(kakaoMap)
        markers.value.push(marker)
      }
    })
  } catch (error) {
    console.error('❌ 백엔드 데이터 요청 실패:', error)
  }
}
</script>

<style scoped>
.map-container {
  width: 100%;
  margin-top: 15px;
}

.filter-buttons {
  margin-bottom: 15px;
  display: flex;
  gap: 10px;
}

/* 기본 버튼 스타일 */
.btn {
  padding: 8px 18px;
  border-radius: 20px;
  border: 1.5px solid #e0e0e0;
  background-color: white;
  color: #666;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.25s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.btn:hover {
  background-color: #f5f5f5;
  color: #333;
}

/* ⭐️ 클릭되어 활성화(active) 되었을 때의 색상 정의 */
.btn.active {
  background-color: #333;
  color: white;
  border-color: #333;
}

/* 맛집 버튼 클릭 활성화 스타일 */
.btn-res.active {
  background-color: #ff9800;
  color: white;
  border-color: #ff9800;
  box-shadow: 0 4px 10px rgba(255, 152, 0, 0.3);
}

/* 관광지 버튼 클릭 활성화 스타일 */
.btn-tour.active {
  background-color: #03a9f4;
  color: white;
  border-color: #03a9f4;
  box-shadow: 0 4px 10px rgba(3, 169, 244, 0.3);
}

.map-area {
  width: 100%;
  height: 65vh;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: 1px solid #e0e0e0;
}
</style>
