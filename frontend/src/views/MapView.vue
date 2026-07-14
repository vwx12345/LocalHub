<template>
  <div class="map-view-container">
    <h2>🗺️ 대전/충청 맛집·관광 지도</h2>
    <p class="subtitle">원하는 구역의 맛집과 관광지를 한눈에 확인해 보세요!</p>

    <KakaoMap />
  </div>
</template>

<script setup>
import KakaoMap from '../components/KakaoMap.vue'
</script>

<style scoped>
.map-view-container {
  padding: 20px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}
h2 {
  margin-bottom: 5px;
  color: #333;
}
.subtitle {
  color: #666;
  margin-bottom: 20px;
  font-size: 14px;
}
</style>
