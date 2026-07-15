
<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const router = useRouter()

const place = ref(null)

const categoryInfo = computed(() => {
  const categories = {
    restaurant: {
      label: '맛집 추천',
      icon: '🍽️',
    },
    tour: {
      label: '관광지 추천',
      icon: '🗺️',
    },
    free: {
      label: '자유게시판',
      icon: '💬',
    },
  }

  return categories[props.post.category] || categories.free
})

const placeTitle = computed(() => {
  if (!place.value) {
    return ''
  }

  return place.value.title || '장소 정보'
})

async function fetchPlace() {
  if (!props.post.place_id) {
    return
  }

  try {
    const response = await fetch(
      `/api/places/${props.post.place_id}`,
    )

    if (!response.ok) {
      return
    }

    place.value = await response.json()
  } catch (error) {
    console.error('장소 정보 조회 실패:', error)
    place.value = null
  }
}

function goDetail() {
  router.push(`/posts/${props.post.id}`)
}

function goPlace(event) {
  event.stopPropagation()

  if (!props.post.place_id) {
    return
  }

  router.push({
    path: '/map',
    query: {
      place_id: props.post.place_id,
    },
  })
}

function formatDate(date) {
  if (!date) {
    return ''
  }

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(date))
}

onMounted(fetchPlace)
</script>

<template>
  <article
    class="post-item"
    tabindex="0"
    @click="goDetail"
    @keyup.enter="goDetail"
  >
    <div class="post-main">
      <span
        class="post-badge"
        :class="post.category || 'free'"
      >
        {{ categoryInfo.icon }} {{ categoryInfo.label }}
      </span>

      <h3>{{ post.title }}</h3>

      <button
        v-if="place"
        type="button"
        class="place-tag"
        @click="goPlace"
      >
        📍 {{ placeTitle }}
      </button>

      <p class="post-preview">
        {{ post.content }}
      </p>
    </div>

    <div class="post-meta">
      <span>👁 {{ post.views }}</span>
      <span>{{ formatDate(post.created_at) }}</span>
      <span class="arrow">›</span>
    </div>
  </article>
</template>

<style scoped>
.post-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;

  padding: 20px 22px;

  background: #fff;
  border: 1px solid #f1f3f5;
  border-radius: 15px;

  cursor: pointer;
  outline: none;

  transition: all 0.2s ease;
}

.post-item:hover,
.post-item:focus {
  border-color: #dee2e6;
  box-shadow: 0 9px 20px rgba(0, 0, 0, 0.055);
  transform: translateY(-2px);
}

.post-main {
  min-width: 0;
  flex: 1;
}

.post-badge {
  display: inline-block;

  margin-bottom: 9px;
  padding: 4px 9px;

  border-radius: 6px;

  font-size: 11px;
  font-weight: 700;
}

.post-badge.restaurant {
  background: #fff4e6;
  color: #f76707;
}

.post-badge.tour {
  background: #e7f5ff;
  color: #228be6;
}

.post-badge.free {
  background: #f1f3f5;
  color: #495057;
}

h3 {
  margin: 0;
  overflow: hidden;

  color: #212529;

  font-size: 17px;
  font-weight: 750;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.place-tag {
  display: inline-flex;
  align-items: center;

  width: fit-content;
  margin-top: 9px;
  padding: 5px 9px;

  border: 1px solid #ffd8a8;
  border-radius: 7px;

  background: #fff4e6;
  color: #e8590c;

  cursor: pointer;

  font-size: 12px;
  font-weight: 700;

  transition: all 0.2s ease;
}

.place-tag:hover {
  background: #ffe8cc;
  border-color: #ffa94d;
}

.post-preview {
  display: -webkit-box;

  margin: 8px 0 0;
  overflow: hidden;

  color: #868e96;

  font-size: 14px;
  line-height: 1.55;

  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;

  color: #adb5bd;

  font-size: 12px;
}

.arrow {
  color: #868e96;

  font-size: 26px;
  line-height: 1;
}

@media (max-width: 650px) {
  .post-item {
    align-items: flex-start;
    flex-direction: column;
    gap: 14px;
  }

  .post-meta {
    width: 100%;
  }

  .arrow {
    margin-left: auto;
  }
}
</style>

