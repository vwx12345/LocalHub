<template>
  <div class="map-view-container">
    <h2>🗺️ 대전/충청 맛집·관광 지도</h2>
    <p class="subtitle">원하는 구역의 맛집과 관광지를 한눈에 확인해 보세요!</p>

    <KakaoMap class="map-flex-fill" />
  </div>
</template>

<script setup>
import KakaoMap from '../components/KakaoMap.vue'
</script>

<style scoped>
.map-view-container {
  width: 100%;
  height: 100%;           /* 부모(main-content)의 높이를 물려받음 */
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 20px 20px 0 20px; /* 제목/부제목 여백은 유지, 아래쪽만 지도가 꽉 채우도록 0 */
}
h2 {
  margin-bottom: 5px;
  color: #333;
  flex-shrink: 0;         /* 제목은 원래 크기 유지 */
}
.subtitle {
  color: #666;
  margin-bottom: 15px;
  font-size: 14px;
  flex-shrink: 0;         /* 부제목도 원래 크기 유지 */
}

/* KakaoMap(=map-layout을 감싸는 루트)이 제목/부제목을 뺀 나머지 공간을 전부 차지하도록 */
.map-flex-fill {
  flex: 1;
  min-height: 0; /* flex 자식이 내용 때문에 넘치는 것 방지 (매우 중요) */
}
</style>