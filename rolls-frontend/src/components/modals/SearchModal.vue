<template>
  <Teleport to="body">
    <div v-if="isOpen" class="search-modal-overlay" @click="close">
      <div class="search-modal" @click.stop>
        <div class="search-modal-header">
          <h2>Поиск</h2>
          <button class="close-btn" @click="close">×</button>
        </div>
        
        <div class="search-input-wrapper">
          <input
            type="text"
            :value="query"
            @input="$emit('update:query', ($event.target as HTMLInputElement).value)"
            @keyup.enter="search"
            placeholder="Введите название блюда..."
            class="search-input"
            autofocus
          />
          <button v-if="query" class="clear-input" @click="$emit('update:query', '')">×</button>
        </div>
        
        <div class="search-hint">
          <p>Поиск осуществляется по названию блюда</p>
        </div>
        
        <div class="search-actions">
          <button class="search-btn" @click="search">Найти</button>
          <button class="cancel-btn" @click="close">Отмена</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{
  isOpen: boolean
  query: string
}>()

const emit = defineEmits<{
  close: []
  search: []
  'update:query': [value: string]
}>()

const close = () => emit('close')
const search = () => emit('search')
</script>

<style scoped>
.search-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.search-modal {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 500px;
  padding: 24px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(-30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.search-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-modal-header h2 {
  font-family: 'Courier New', Courier, monospace;
  color: #333;
  font-size: 24px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 32px;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #E9544E;
}

.search-input-wrapper {
  position: relative;
  margin-bottom: 16px;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 16px;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #E9544E;
}

.clear-input {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: #e0e0e0;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.clear-input:hover {
  background: #ccc;
}

.search-hint {
  margin-bottom: 24px;
  padding: 8px 0;
}

.search-hint p {
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  color: #999;
  font-style: italic;
  margin: 0;
}

.search-actions {
  display: flex;
  gap: 12px;
}

.search-btn,
.cancel-btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 12px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.search-btn {
  background: #E9544E;
  color: white;
}

.search-btn:hover {
  background: #d43f39;
  transform: scale(1.02);
}

.cancel-btn {
  background: #f0f0f0;
  color: #666;
}

.cancel-btn:hover {
  background: #e0e0e0;
}
</style>