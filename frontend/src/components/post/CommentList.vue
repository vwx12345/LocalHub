<script setup>
import { ref } from 'vue'

import { createComment } from '../../api/post'

import CommentItem from './CommentItem.vue'

const props = defineProps({
  postId: {
    type: Number,
    required: true,
  },

  comments: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['refresh'])

const content = ref('')

const password = ref('')

async function addComment() {
  if (!content.value || !password.value) {
    alert('내용과 비밀번호를 입력하세요')

    return
  }

  try {
    await createComment(props.postId, {
      content: content.value,
      password: password.value,
    })

    content.value = ''
    password.value = ''

    emit('refresh')
  } catch (err) {
    alert(err.message)
  }
}
</script>

<template>
  <section class="comment-section">
    <h2>댓글</h2>

    <div v-if="comments.length === 0">작성된 댓글이 없습니다.</div>

    <CommentItem
      v-for="comment in comments"
      :key="comment.id"
      :comment="comment"
      @refresh="emit('refresh')"
    />

    <div class="write-box">
      <textarea v-model="content" placeholder="댓글 작성" />

      <input v-model="password" type="password" placeholder="비밀번호" />

      <button @click="addComment">작성</button>
    </div>
  </section>
</template>

<style scoped>
.comment-section {
  margin-top: 40px;
}

textarea {
  width: 100%;

  height: 100px;

  resize: none;
}

input {
  margin-top: 10px;

  padding: 8px;
}

button {
  margin-top: 10px;

  padding: 8px 15px;

  cursor: pointer;
}

.write-box {
  margin-top: 20px;
}
</style>
