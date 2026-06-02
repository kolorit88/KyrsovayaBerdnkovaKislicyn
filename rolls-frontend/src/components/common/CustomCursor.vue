<template>
  <div 
    v-if="visible" 
    class="custom-cursor"
    :style="{ left: x + 'px', top: y + 'px' }"
  >
    <img 
      src="/src/public/krest.png" 
      alt="cursor" 
      class="cursor-img"
      draggable="false"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  visible: boolean
  x: number
  y: number
}>()
</script>

<style scoped>
.custom-cursor {
  position: fixed;
  pointer-events: none;
  z-index: 10000;
  transform: translate(-50%, -50%);
}

.cursor-img {
  width: 120px;
  height: 120px;
  display: block;
  pointer-events: none;
  user-select: none;
}
</style>