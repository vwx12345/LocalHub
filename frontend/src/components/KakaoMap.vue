<template>
  <div class="map-layout">
    
    <div id="map" class="map-area"></div>

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

    <div class="sidebar" :class="{ 'is-open': activePlace !== null }">
      <button class="close-btn" @click="closeSidebar">✕</button>

      <div v-if="activePlace" class="sidebar-content">
        <div class="place-image-box">
          <img 
            :src="activePlace.image_url || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=400'" 
            alt="장소 이미지" 
            class="place-image"
          />
        </div>

        <div class="place-info">
          <span class="badge" :class="activePlace.type">
            {{ activePlace.type === 'restaurant' ? '🍔 맛집' : '🎯 관광지' }}
          </span>
          <h2 class="place-title">{{ activePlace.title }}</h2>
          <p class="place-address">📍 {{ activePlace.address }}</p>
          <p class="place-hours">⏰ 영업시간: 매일 09:00 - 21:00 (준비중)</p>
        </div>

        <hr class="divider" />

        <div class="review-section">
          <h3>💬 방문자 리뷰</h3>
          <div class="review-list">
            <div class="review-item">
              <span class="review-author">로컬러브</span>
              <p class="review-text">분위기도 좋고 맛도 훌륭합니다! 강력 추천해요.</p>
            </div>
          </div>
          
          <div class="review-input-box">
            <input type="text" placeholder="방문 후기를 한 줄로 남겨보세요!" class="review-input" />
            <button class="review-submit-btn">등록</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const activeFilter = ref('')
const activePlace = ref(null)
const markers = ref([])
let kakaoMap = null
let hoverInfowindow = null

onMounted(() => {
  const { kakao } = window
  if (!kakao) return

  kakao.maps.load(() => {
    const container = document.getElementById('map')
    const options = {
      center: new kakao.maps.LatLng(36.3504119, 127.3845475),
      level: 7,
    }
    kakaoMap = new kakao.maps.Map(container, options)
    
    hoverInfowindow = new kakao.maps.InfoWindow({
      zIndex: 1,
      disableAutoPan: true
    })

    fetchPlaces('')
  })
})

const fetchPlaces = async (type) => {
  const { kakao } = window
  activeFilter.value = type
  closeSidebar()

  try {
    markers.value.forEach((marker) => marker.setMap(null))
    markers.value = []

    const response = await axios.get(`http://localhost:8000/api/places?type=${type}`)
    const places = response.data

    places.forEach((place) => {
      if (place.map_x && place.map_y) {
        const markerPosition = new kakao.maps.LatLng(place.map_y, place.map_x)
        const marker = new kakao.maps.Marker({
          position: markerPosition,
          title: place.title,
        })

        marker.setMap(kakaoMap)
        markers.value.push(marker)

        kakao.maps.event.addListener(marker, 'mouseover', () => {
          const content = `
            <div style="padding: 6px 12px; font-size: 12px; font-weight: bold; color: #333; text-align: center; border-radius: 4px; border: none; background: #fff;">
              ${place.title}
            </div>
          `
          hoverInfowindow.setContent(content)
          hoverInfowindow.open(kakaoMap, marker)
        })

        kakao.maps.event.addListener(marker, 'mouseout', () => {
          hoverInfowindow.close()
        })

        kakao.maps.event.addListener(marker, 'click', () => {
          activePlace.value = place
          
          // ⭐️ 지도가 오른쪽 사이드바에 가려지지 않게, 중심을 약간 왼쪽으로 옮겨주는 로직도 가능하지만
          // 일단은 클릭한 마커가 화면 중앙으로 오도록 가장 베이직하게 구현했습니다.
          kakaoMap.panTo(markerPosition)
        })
      }
    })
  } catch (error) {
    console.error('❌ 백엔드 데이터 요청 실패:', error)
  }
}

const closeSidebar = () => {
  activePlace.value = null
}
</script>

<style scoped>
/* ⭐️ 화면 전체를 채우는 맵 레이아웃 */
.map-layout {
  position: relative; /* 자식 요소들이 공중에 뜰 수 있는 기준점 */
  width: 100%;
  
  /* 헤더 높이를 제외한 나머지 높이를 꽉 채우도록 설정 (헤더가 약 100px이라고 가정) */
  height: calc(100vh - 100px); 
  
  background-color: #f5f5f5;
  overflow: hidden;
}

/* 지도 영역 (100% 꽉 채우기) */
.map-area {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1; /* 제일 밑바닥 */
}

/* 필터 버튼 (좌측 상단에 동동 띄우기) */
.filter-buttons {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10; /* 지도 위 */
  display: flex;
  gap: 8px;
}

/* 버튼 스타일 (기존과 동일) */
.btn {
  padding: 10px 18px;
  border-radius: 30px;
  border: none;
  background-color: white;
  color: #444;
  cursor: pointer;
  font-weight: bold;
  font-size: 13px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}
.btn:hover { background-color: #f9f9f9; transform: translateY(-2px); }
.btn.active { background-color: #333; color: white; }
.btn-res.active { background-color: #ff9800; color: white; }
.btn-tour.active { background-color: #03a9f4; color: white; }


/* ⭐️ 오른쪽 사이드바 (지도 우측에서 슬라이딩) */
.sidebar {
  position: absolute;
  top: 0;
  right: 0;
  width: 380px;
  height: 100%;
  background-color: white;
  z-index: 50; /* 지도 위, 필터 버튼보다 위 */
  box-shadow: -4px 0 15px rgba(0, 0, 0, 0.1);
  
  /* 화면 우측 바깥으로 100% 밀어내서 숨겨둠 */
  transform: translateX(100%); 
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 열렸을 때 원래 위치(0)로 쏙 들어옴 */
.sidebar.is-open {
  transform: translateX(0);
}

.sidebar-content {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* 닫기 버튼 */
.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: white;
  border: 1px solid #ddd;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-weight: bold;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  z-index: 60;
}
.close-btn:hover { background: #f5f5f5; }

/* 디테일 내용 스타일 */
.place-image-box { width: 100%; height: 200px; border-radius: 12px; overflow: hidden; margin-bottom: 20px;}
.place-image { width: 100%; height: 100%; object-fit: cover; }
.badge { font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 20px; margin-bottom: 10px; display: inline-block;}
.badge.restaurant { background-color: #fff3e0; color: #ef6c00; border: 1px solid #ffe0b2; }
.badge.tour { background-color: #e1f5fe; color: #0288d1; border: 1px solid #b3e5fc; }
.place-title { font-size: 24px; font-weight: 800; margin: 0 0 10px 0; color: #111; }
.place-address, .place-hours { font-size: 14px; color: #666; margin: 5px 0; }
.divider { border-top: 1px solid #eee; margin: 24px 0; border-bottom: none; border-left: none; border-right: none;}
.review-section h3 { font-size: 16px; font-weight: 700; margin-bottom: 15px; }
.review-item { background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 15px;}
.review-author { font-size: 12px; font-weight: bold; color: #333; margin-bottom: 5px; display: block;}
.review-text { font-size: 13px; color: #555; line-height: 1.5; margin: 0;}
.review-input-box { display: flex; gap: 8px; margin-top: auto; padding-top: 20px;}
.review-input { flex-grow: 1; padding: 12px; font-size: 13px; border: 1px solid #ddd; border-radius: 8px; outline: none;}
.review-submit-btn { padding: 0 18px; background-color: #333; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;}
</style>