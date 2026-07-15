<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const router = useRouter()

function goDetail() {
  router.push(`/posts/${props.post.id}`)
}

function formatDate(date) {
  if (!date) return ''

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(date))
}
</script>

<template>
  <article class="post-item" tabindex="0" @click="goDetail" @keyup.enter="goDetail">
    <div class="post-main">
      <span class="post-badge">지역 이야기</span>

      <h3>{{ post.title }}</h3>

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
  background: #e7f5ff;
  color: #228be6;
  font-size: 11px;
  font-weight: 700;
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
