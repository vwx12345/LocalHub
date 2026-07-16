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
const submitting = ref(false)

async function addComment() {
  const trimmedContent = content.value.trim()
  const trimmedPassword = password.value.trim()

  if (!trimmedContent || !trimmedPassword) {
    alert('댓글 내용과 비밀번호를 입력해주세요.')
    return
  }

  try {
    submitting.value = true

    await createComment(props.postId, {
      content: trimmedContent,
      password: trimmedPassword,
      parent_id: null,
    })

    content.value = ''
    password.value = ''

    emit('refresh')
  } catch (err) {
    alert(err.message)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section class="comment-section">
    <header class="comment-header">
      <div>
        <h2>
          💬 댓글
          <span>{{ comments.length }}</span>
        </h2>

        <p>게시글에 대한 의견이나 지역 정보를 나눠보세요.</p>
      </div>
    </header>

    <div class="comment-write-box">
      <textarea
        v-model="content"
        maxlength="1000"
        placeholder="댓글 내용을 입력해주세요."
      ></textarea>

      <div class="write-footer">
        <input
          v-model="password"
          type="password"
          maxlength="100"
          placeholder="비밀번호"
          @keyup.enter="addComment"
        />

        <button class="submit-button" :disabled="submitting" @click="addComment">
          {{ submitting ? '등록 중...' : '댓글 등록' }}
        </button>
      </div>
    </div>

    <div v-if="comments.length === 0" class="empty-comments">
      <span>💭</span>
      <p>아직 작성된 댓글이 없습니다.</p>
      <small>첫 번째 댓글을 남겨보세요.</small>
    </div>

    <div v-else class="comment-list">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        @refresh="emit('refresh')"
      />
    </div>
  </section>
</template>

<style scoped>
.comment-section {
  margin-top: 24px;
  padding: 30px;
  background: #fff;
  border: 1px solid #edf2f7;
  border-radius: 18px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.04);
}

.comment-header h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  color: #212529;
  font-size: 20px;
  font-weight: 800;
}

.comment-header h2 span {
  padding: 2px 8px;
  border-radius: 20px;
  background: #f1f3f5;
  color: #868e96;
  font-size: 13px;
  font-weight: 600;
}

.comment-header p {
  margin: 8px 0 0;
  color: #868e96;
  font-size: 13px;
}

.comment-write-box {
  margin-top: 22px;
  padding: 18px;
  background: #f8f9fa;
  border-radius: 15px;
}

textarea,
input {
  box-sizing: border-box;
  border: 1px solid #e9ecef;
  outline: none;
  background: #fff;
  color: #343a40;
  font: inherit;
  transition: all 0.2s ease;
}

textarea:focus,
input:focus {
  border-color: #212529;
  box-shadow: 0 0 0 3px rgba(33, 37, 41, 0.08);
}

textarea {
  width: 100%;
  min-height: 105px;
  padding: 14px;
  border-radius: 11px;
  resize: vertical;
  line-height: 1.6;
}

.write-footer {
  display: flex;
  justify-content: flex-end;
  gap: 9px;
  margin-top: 10px;
}

.write-footer input {
  width: 180px;
  padding: 11px 13px;
  border-radius: 10px;
}

.submit-button {
  padding: 0 18px;
  border: none;
  border-radius: 10px;
  background: #212529;
  color: #fff;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.2s ease;
}

.submit-button:hover:not(:disabled) {
  background: #343a40;
}

.submit-button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.empty-comments {
  padding: 48px 20px;
  color: #868e96;
  text-align: center;
}

.empty-comments span {
  font-size: 34px;
}

.empty-comments p {
  margin: 10px 0 4px;
  color: #495057;
  font-weight: 650;
}

.empty-comments small {
  color: #adb5bd;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 22px;
}

@media (max-width: 600px) {
  .comment-section {
    padding: 22px 16px;
  }

  .write-footer {
    flex-direction: column;
  }

  .write-footer input {
    width: 100%;
  }

  .submit-button {
    min-height: 42px;
  }
}
</style>
