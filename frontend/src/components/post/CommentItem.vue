<script setup>
import { ref } from 'vue'

import { deleteComment, updateComment } from '../../api/post'

const props = defineProps({
  comment: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['refresh'])

const isEditing = ref(false)

const editContent = ref('')

function formatDate(date) {
  return new Date(date).toLocaleString()
}

function startEdit() {
  editContent.value = props.comment.content

  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false

  editContent.value = ''
}

async function saveEdit() {
  const password = prompt('댓글 비밀번호를 입력하세요')

  if (!password) {
    return
  }

  try {
    await updateComment(props.comment.id, {
      content: editContent.value,
      password,
    })

    alert('댓글이 수정되었습니다.')

    isEditing.value = false

    emit('refresh')
  } catch (err) {
    alert(err.message)
  }
}

async function removeComment() {
  const password = prompt('댓글 비밀번호를 입력하세요')

  if (!password) {
    return
  }

  try {
    await deleteComment(props.comment.id, password)

    alert('댓글이 삭제되었습니다.')

    emit('refresh')
  } catch (err) {
    alert(err.message)
  }
}
</script>

<template>
  <div class="comment-item">
    <!-- 수정 모드 -->
    <div v-if="isEditing">
      <textarea v-model="editContent" />

      <div class="buttons">
        <button @click="saveEdit">저장</button>

        <button @click="cancelEdit">취소</button>
      </div>
    </div>

    <!-- 일반 표시 -->
    <div v-else>
      <p>
        {{ comment.content }}
      </p>

      <div class="meta">
        <span>
          {{ formatDate(comment.created_at) }}
        </span>

        <button @click="startEdit">수정</button>

        <button class="delete" @click="removeComment">삭제</button>
      </div>
    </div>

    <!-- 대댓글 -->
    <div v-for="reply in comment.replies" :key="reply.id" class="reply">
      <p>↳ {{ reply.content }}</p>
    </div>
  </div>
</template>

<style scoped>
.comment-item {
  padding: 15px 0;

  border-bottom: 1px solid #ddd;
}

.meta {
  display: flex;

  gap: 10px;

  align-items: center;

  color: #777;

  font-size: 13px;
}

button {
  border: none;

  background: none;

  cursor: pointer;
}

.delete {
  color: #e53935;
}

textarea {
  width: 100%;

  height: 80px;
}

.buttons {
  margin-top: 10px;

  display: flex;

  gap: 10px;
}

.reply {
  margin-left: 30px;

  color: #666;
}
</style>
