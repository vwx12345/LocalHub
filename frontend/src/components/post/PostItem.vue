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
  return new Date(date).toLocaleDateString()
}
</script>

<template>
  <div class="post-item" @click="goDetail">
    <h3>
      {{ post.title }}
    </h3>

    <p class="content">
      {{ post.content }}
    </p>

    <div class="info">
      <span> 조회수 {{ post.views }} </span>

      <span>
        {{ formatDate(post.created_at) }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.post-item {
  padding: 20px;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
  transition: background-color 0.2s;
}

.post-item:hover {
  background-color: #f5f7fa;
}

h3 {
  margin-bottom: 10px;
}

.content {
  color: #666;

  overflow: hidden;
  text-overflow: ellipsis;

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.info {
  margin-top: 15px;

  display: flex;
  justify-content: space-between;

  color: #888;
  font-size: 14px;
}
</style>
