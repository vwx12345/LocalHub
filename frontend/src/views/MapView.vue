```vue
<template>
  <div class="map-view-container">
    <div class="map-header">
      <div class="title-icon">🗺️</div>

      <div class="title-content">
        <span class="title-region">DAEJEON · CHUNGCHEONG</span>
        <h2>대전·충청 맛집/관광 지도</h2>
      </div>
    </div>

    <KakaoMap class="map-flex-fill" />
  </div>
</template>

<script setup>
import KakaoMap from '../components/KakaoMap.vue'
</script>

<style scoped>
.map-view-container {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 18px 20px 0;
  background: #f8f9fa;
}

.map-header {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
  margin-bottom: 16px;
  padding: 15px 20px;

  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.98),
    rgba(255, 247, 237, 0.98)
  );

  border: 1px solid rgba(255, 146, 43, 0.18);
  border-radius: 18px;

  box-shadow:
    0 8px 24px rgba(33, 37, 41, 0.07),
    0 2px 6px rgba(255, 146, 43, 0.06);

  overflow: hidden;
}

/* 왼쪽 주황색 바 */
.map-header::before {
  content: '';
  position: absolute;
  top: 14px;
  bottom: 14px;
  left: 0;
  width: 5px;

  background: linear-gradient(
    to bottom,
    #ff922b,
    #fab005
  );

  border-radius: 0 8px 8px 0;
}

/* 오른쪽 주황색 바 */
.map-header::after {
  content: '';
  position: absolute;
  top: 14px;
  bottom: 14px;
  right: 0;
  width: 5px;

  background: linear-gradient(
    to bottom,
    #ff922b,
    #fab005
  );

  border-radius: 8px 0 0 8px;
}

.title-icon {
  width: 48px;
  height: 48px;

  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;
  font-size: 25px;

  background: linear-gradient(
    135deg,
    #fff4e6,
    #ffe8cc
  );

  border: 1px solid #ffd8a8;
  border-radius: 15px;
  box-shadow: 0 5px 12px rgba(255, 146, 43, 0.14);
}

.title-content {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.title-region {
  color: #f08c00;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1.7px;
}

.title-content h2 {
  margin: 0;
  color: #212529;
  font-size: 22px;
  font-weight: 800;
  line-height: 1.25;
  letter-spacing: -0.8px;
}

.map-flex-fill {
  flex: 1;
  min-height: 0;
  border-radius: 18px 18px 0 0;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(33, 37, 41, 0.08);
}

@media (max-width: 768px) {
  .map-view-container {
    padding: 12px 12px 0;
  }

  .map-header {
    margin-bottom: 12px;
    padding: 13px 15px;
    border-radius: 15px;
  }

  .map-header::before,
  .map-header::after {
    top: 12px;
    bottom: 12px;
    width: 4px;
  }

  .title-icon {
    width: 42px;
    height: 42px;
    font-size: 22px;
    border-radius: 13px;
  }

  .title-content h2 {
    font-size: 19px;
  }

  .title-region {
    font-size: 9px;
    letter-spacing: 1.2px;
  }

  .map-flex-fill {
    border-radius: 15px 15px 0 0;
  }
}
</style>
```
