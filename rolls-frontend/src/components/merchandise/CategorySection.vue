<template>
  <div class="category-section" :id="category.slug || `category-${category.id}`">
    <div class="category-header">
      <h2 class="category-title">{{ (category.name || '').toUpperCase() }}</h2>
      <img src="/src/public/lin.png" alt="" class="category-underline" />
    </div>

    <div
      v-if="category.merchandises && category.merchandises.length > 0"
      class="merchandise-grid"
    >
      <MerchandiseCard
        v-for="item in category.merchandises"
        :key="item.id"
        :merchandise="item"
        :cartQuantities="cartQuantities"
        @addToCart="(mId, vId, qty) => $emit('addToCart', mId, vId, qty)"
      />
    </div>

    <div v-else class="empty-category">
      <p>Товары в этой категории скоро появятся</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import MerchandiseCard from './MerchandiseCard.vue'
import type { Category } from '../services/api'

defineProps<{
  category: Category
  cartQuantities: Record<string, number>
}>()

defineEmits<{
  addToCart: [merchandiseId: number, variationId: number, quantity: number]
}>()
</script>

<style scoped>
/* Стили остаются без изменений */
.category-section {
  margin-bottom: 64px;
  scroll-margin-top: 160px;
}

.category-header {
  text-align: center;
  margin-bottom: 28px;
}

.category-title {
  font-family: 'Courier New', Courier, monospace;
  font-size: clamp(22px, 4vw, 32px);
  font-weight: 800;
  color: #333;
  letter-spacing: 2px;
  margin-bottom: 10px;
}

.category-underline {
  display: block;
  margin: 0 auto;
  width: 150px;
  height: auto;
}

.merchandise-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

@media (max-width: 900px) {
  .merchandise-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}

@media (max-width: 550px) {
  .merchandise-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

.empty-category {
  text-align: center;
  padding: 40px;
  background: rgba(249, 249, 249, 0.8);
  border-radius: 20px;
  font-family: 'Courier New', Courier, monospace;
  color: #999;
  backdrop-filter: blur(6px);
}
</style>