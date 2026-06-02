<template>
  <div 
    ref="anchorBarRef"
    class="anchor-bar" 
    :class="{ fixed: isAnchorBarFixed }"
    @wheel.prevent="handleWheel"
  >
    <div class="anchor-bar-container">
      <div class="anchor-icons">
        <img 
          :src="hasActiveFilters ? '/src/public/settings1.png' : '/src/public/settings.png'" 
          alt="Settings" 
          class="anchor-icon" 
          @click="$emit('openFilter')"
        />
        <img 
          :src="isSearchOpen ? '/src/public/search1.png' : '/src/public/search.png'" 
          alt="Search" 
          class="anchor-icon" 
          @click="$emit('openSearch')"
        />
      </div>
      
      <div class="vertical-divider"></div>
      
      <div class="anchor-buttons-wrapper">
        <div 
          class="anchor-buttons-container"
          @mousedown="startDrag"
          @mouseup="stopDrag"
          @mouseleave="stopDrag"
          @mousemove="onDrag"
        >
          <button
            v-for="category in categories"
            :key="category.id"
            class="anchor-button"
            :class="{ active: activeCategory === category.id }"
            @click="$emit('scrollTo', category.id)"
          >
            {{ category.name }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

defineProps<{
  categories: Array<{ id: string; name: string }>
  activeCategory: string
  hasActiveFilters: boolean
  isSearchOpen: boolean
  isAnchorBarFixed: boolean
}>()

defineEmits<{
  openFilter: []
  openSearch: []
  scrollTo: [categoryId: string]
}>()

const anchorBarRef = ref<HTMLElement | null>(null)

const isDragging = ref(false)
const startX = ref(0)
const scrollLeft = ref(0)

const startDrag = (e: MouseEvent) => {
  isDragging.value = true
  const container = anchorBarRef.value?.querySelector('.anchor-buttons-container')
  if (container) {
    startX.value = e.pageX - container.offsetLeft
    scrollLeft.value = container.scrollLeft
    container.style.cursor = 'grabbing'
  }
}

const stopDrag = () => {
  isDragging.value = false
  const container = anchorBarRef.value?.querySelector('.anchor-buttons-container')
  if (container) {
    container.style.cursor = 'grab'
  }
}

const onDrag = (e: MouseEvent) => {
  if (!isDragging.value) return
  e.preventDefault()
  const container = anchorBarRef.value?.querySelector('.anchor-buttons-container')
  if (container) {
    const x = e.pageX - container.offsetLeft
    const walk = (x - startX.value) * 1.5
    container.scrollLeft = scrollLeft.value - walk
  }
}

const handleWheel = (event: WheelEvent) => {
  const container = anchorBarRef.value?.querySelector('.anchor-buttons-container')
  if (container) {
    container.scrollLeft += event.deltaY
    event.preventDefault()
  }
}

onMounted(() => {
  const container = anchorBarRef.value?.querySelector('.anchor-buttons-container')
  if (container) {
    container.style.cursor = 'grab'
  }
})

onUnmounted(() => {
  const container = anchorBarRef.value?.querySelector('.anchor-buttons-container')
  if (container) {
    container.style.cursor = ''
  }
})
</script>

<style scoped>
.anchor-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: transparent;
  z-index: 999;
  padding: 20px 0;
  transition: all 0.3s ease;
  pointer-events: none;
}

.anchor-bar.fixed {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 -2px 20px rgba(0, 0, 0, 0.1);
  pointer-events: auto;
}

.anchor-bar:not(.fixed) .anchor-bar-container {
  pointer-events: auto;
}

.anchor-bar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.anchor-icons {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-shrink: 0;
}

.anchor-icon {
  width: 40px;
  height: 40px;
  cursor: pointer;
  transition: all 0.3s ease;
  pointer-events: auto;
}

.anchor-icon:hover {
  transform: scale(1.1);
  opacity: 0.8;
}

.vertical-divider {
  width: 2px;
  height: 40px;
  background-color: #E9544E;
  flex-shrink: 0;
  pointer-events: auto;
}

.anchor-buttons-wrapper {
  flex: 1;
  overflow: hidden;
  position: relative;
  pointer-events: auto;
}

.anchor-buttons-container {
  display: flex;
  gap: 12px;
  white-space: nowrap;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;
  -ms-overflow-style: none;
  cursor: grab;
  padding: 5px 0;
}

.anchor-buttons-container::-webkit-scrollbar {
  display: none;
}

.anchor-buttons-container:active {
  cursor: grabbing;
}

.anchor-button {
  background: white;
  border: 1.5px solid rgba(0, 0, 0, 0.15);
  padding: 10px 20px;
  border-radius: 30px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  background: rgba(255, 255, 255, 0.95);
}

.anchor-button:hover {
  border-color: #E9544E;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(233, 84, 78, 0.2);
}

.anchor-button.active {
  border-color: #E9544E;
  background: rgba(233, 84, 78, 0.1);
  color: #E9544E;
  box-shadow: 0 2px 8px rgba(233, 84, 78, 0.15);
}

@media (max-width: 768px) {
  .anchor-button {
    font-size: 12px;
    padding: 8px 16px;
  }
  
  .anchor-icon {
    width: 32px;
    height: 32px;
  }
  
  .vertical-divider {
    height: 32px;
  }
}

@media (max-width: 480px) {
  .anchor-button {
    font-size: 10px;
    padding: 6px 12px;
  }
  
  .anchor-icon {
    width: 28px;
    height: 28px;
  }
  
  .vertical-divider {
    height: 28px;
  }
  
  .anchor-bar-container {
    gap: 12px;
  }
  
  .anchor-icons {
    gap: 8px;
  }
}
</style>