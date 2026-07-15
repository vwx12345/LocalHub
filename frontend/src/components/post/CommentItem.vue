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
const editPassword = ref('')
const saving = ref(false)

function formatDate(date) {
  if (!date) return ''

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date))
}

function startEdit() {
  editContent.value = props.comment.content
  editPassword.value = ''
  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false
  editContent.value = ''
  editPassword.value = ''
}

async function saveEdit() {
  const content = editContent.value.trim()
  const password = editPassword.value.trim()

  if (!content || !password) {
    alert('댓글 내용과 비밀번호를 입력해주세요.')
    return
  }

  try {
    saving.value = true

    await updateComment(props.comment.id, {
      content,
      password,
    })

    cancelEdit()
    emit('refresh')
  } catch (err) {
    alert(err.message)
  } finally {
    saving.value = false
  }
}

async function removeComment() {
  const password = prompt('댓글 비밀번호를 입력하세요.')

  if (!password) return

  const confirmed = confirm(
    props.comment.replies?.length
      ? '댓글을 삭제하면 작성된 대댓글도 함께 삭제됩니다.\n정말 삭제하시겠습니까?'
      : '댓글을 삭제하시겠습니까?',
  )

  if (!confirmed) return

  try {
    await deleteComment(props.comment.id, password)
    emit('refresh')
  } catch (err) {
    alert(err.message)
  }
}
</script>

<template>
  <article class="comment-item">
    <div v-if="isEditing" class="edit-box">
      <textarea v-model="editContent" maxlength="1000"></textarea>

      <div class="edit-footer">
        <input v-model="editPassword" type="password" maxlength="100" placeholder="비밀번호 확인" />

        <button class="action-button" @click="cancelEdit">취소</button>

        <button class="save-button" :disabled="saving" @click="saveEdit">
          {{ saving ? '저장 중...' : '저장' }}
        </button>
      </div>
    </div>

    <template v-else>
      <div class="comment-top">
        <div class="comment-info">
          <span class="anonymous-badge">익명</span>
          <span class="comment-date">
            {{ formatDate(comment.created_at) }}
          </span>
        </div>

        <div class="comment-actions">
          <button class="action-button" @click="startEdit">수정</button>

          <button class="action-button danger" @click="removeComment">삭제</button>
        </div>
      </div>

      <p class="comment-content">
        {{ comment.content }}
      </p>
    </template>

    <div v-if="comment.replies?.length" class="reply-list">
      <article v-for="reply in comment.replies" :key="reply.id" class="reply-item">
        <span class="reply-arrow">↳</span>

        <div>
          <div class="reply-meta">
            <span>답글</span>
            <small>{{ formatDate(reply.created_at) }}</small>
          </div>

          <p>{{ reply.content }}</p>
        </div>
      </article>
    </div>
  </article>
</template>

<style scoped>
.comment-item {
  padding: 20px;
  background: #fff;
  border: 1px solid #f1f3f5;
  border-radius: 15px;
  transition: border-color 0.2s ease;
}

.comment-item:hover {
  border-color: #e9ecef;
}

.comment-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.comment-info {
  display: flex;
  align-items: center;
  gap: 9px;
}

.anonymous-badge {
  padding: 4px 9px;
  border-radius: 6px;
  background: #f1f3f5;
  color: #495057;
  font-size: 12px;
  font-weight: 700;
}

.comment-date {
  color: #adb5bd;
  font-size: 12px;
}

.comment-actions {
  display: flex;
  gap: 6px;
}

.action-button,
.save-button {
  padding: 6px 11px;
  border: 1px solid transparent;
  border-radius: 7px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 650;
}

.action-button {
  background: #f8f9fa;
  color: #495057;
}

.action-button:hover {
  background: #e9ecef;
}

.action-button.danger {
  background: #fff5f5;
  color: #fa5252;
}

.action-button.danger:hover {
  background: #ffe3e3;
}

.save-button {
  background: #212529;
  color: #fff;
}

.save-button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.comment-content {
  margin: 14px 0 0;
  color: #495057;
  font-size: 14px;
  line-height: 1.7;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.edit-box {
  padding: 14px;
  background: #f8f9fa;
  border-radius: 12px;
}

.edit-box textarea,
.edit-box input {
  box-sizing: border-box;
  border: 1px solid #e9ecef;
  outline: none;
  background: #fff;
  font: inherit;
}

.edit-box textarea:focus,
.edit-box input:focus {
  border-color: #212529;
  box-shadow: 0 0 0 3px rgba(33, 37, 41, 0.08);
}

.edit-box textarea {
  width: 100%;
  min-height: 90px;
  padding: 12px;
  border-radius: 9px;
  resize: vertical;
}

.edit-footer {
  display: flex;
  justify-content: flex-end;
  gap: 7px;
  margin-top: 9px;
}

.edit-footer input {
  width: 170px;
  padding: 8px 11px;
  border-radius: 8px;
}

.reply-list {
  display: flex;
  flex-direction: column;
  gap: 9px;
  margin-top: 16px;
  padding-left: 18px;
  border-left: 3px solid #f1f3f5;
}

.reply-item {
  display: flex;
  gap: 10px;
  padding: 13px 15px;
  background: #f8f9fa;
  border-radius: 11px;
}

.reply-arrow {
  color: #adb5bd;
  font-weight: 800;
}

.reply-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.reply-meta span {
  color: #495057;
  font-size: 12px;
  font-weight: 700;
}

.reply-meta small {
  color: #adb5bd;
  font-size: 11px;
}

.reply-item p {
  margin: 6px 0 0;
  color: #495057;
  font-size: 13px;
  line-height: 1.6;
}

@media (max-width: 560px) {
  .comment-top,
  .edit-footer {
    align-items: flex-start;
    flex-direction: column;
  }

  .comment-actions {
    align-self: flex-end;
  }

  .edit-footer input {
    width: 100%;
  }
}
</style>
