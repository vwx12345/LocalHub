<script setup>
defineProps({
  open: Boolean,
})

const emit = defineEmits(['toggle'])
</script>

<template>
  <button class="chat-button" @click="emit('toggle')">💬</button>
</template>

<style scoped>
.chat-button {
  position: fixed;
  right: 30px;
  bottom: 30px;

  width: 64px;
  height: 64px;

  border-radius: 50%;
  border: none;

  background: #0068b7;
  color: white;

  font-size: 28px;

  cursor: pointer;

  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);

  transition: 0.2s;
}

.chat-button:hover {
  transform: scale(1.05);
}
</style>
