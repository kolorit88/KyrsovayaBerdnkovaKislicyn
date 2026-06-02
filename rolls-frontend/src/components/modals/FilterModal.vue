<template>
  <Teleport to="body">
    <div v-if="isOpen" class="filter-modal-overlay" @click="close">
      <div class="filter-modal" @click.stop>
        <div class="filter-modal-header">
          <h2>Фильтр по ингредиентам</h2>
          <button class="close-btn" @click="close">×</button>
        </div>
        
        <div class="filter-search">
          <input
            type="text"
            v-model="searchTerm"
            placeholder="Поиск ингредиента..."
            class="filter-search-input"
          />
        </div>
        
        <div class="ingredients-list">
          <button
            v-for="ing in filteredIngredients"
            :key="ing"
            class="ingredient-btn"
            :class="{ active: selectedIngredients.includes(ing) }"
            @click="$emit('toggleIngredient', ing)"
          >
            {{ ing }}
          </button>
        </div>
        
        <div class="filter-actions">
          <button class="reset-btn" @click="reset">Сбросить все</button>
          <button class="apply-btn" @click="apply">Применить</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  isOpen: boolean
  ingredients: string[]
  selectedIngredients: string[]
}>()

const emit = defineEmits<{
  close: []
  apply: []
  reset: []
  toggleIngredient: [ingredient: string]
}>()

const searchTerm = ref('')

const filteredIngredients = computed(() => {
  if (!searchTerm.value) return props.ingredients
  return props.ingredients.filter(ing => 
    ing.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const close = () => emit('close')
const apply = () => emit('apply')
const reset = () => emit('reset')
</script>

<style scoped>
.filter-modal-overlay {
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

.filter-modal {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
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

.filter-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0 24px;
}

.filter-modal-header h2 {
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

.filter-search {
  padding: 16px 24px;
}

.filter-search-input {
  width: 100%;
  padding: 10px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
}

.filter-search-input:focus {
  outline: none;
  border-color: #E9544E;
}

.ingredients-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 24px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  max-height: 400px;
}

.ingredient-btn {
  padding: 8px 16px;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 30px;
  cursor: pointer;
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  transition: all 0.2s;
}

.ingredient-btn:hover {
  border-color: #E9544E;
  transform: translateY(-2px);
}

.ingredient-btn.active {
  background: #E9544E;
  border-color: #E9544E;
  color: white;
}

.filter-actions {
  display: flex;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid #f0f0f0;
}

.reset-btn,
.apply-btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 12px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.reset-btn {
  background: #f0f0f0;
  color: #666;
}

.reset-btn:hover {
  background: #e0e0e0;
}

.apply-btn {
  background: #E9544E;
  color: white;
}

.apply-btn:hover {
  background: #d43f39;
  transform: scale(1.02);
}
</style>