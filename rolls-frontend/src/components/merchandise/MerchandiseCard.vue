<template>
  <div class="merch-card">
    <div class="merch-card__img-wrap">
      <img
        :src="imageUrl"
        :alt="merchandise.name"
        class="merch-card__img"
        @error="onImgError"
        loading="lazy"
      />
    </div>

    <h3 class="merch-card__title">{{ merchandise.name }}</h3>

    <p v-if="merchandise.description" class="merch-card__desc">{{ merchandise.description }}</p>

    <div class="merch-card__variations">
      <div
        v-for="v in merchandise.variations"
        :key="v.id"
        class="variation"
        :class="{ 'variation--active': selectedVariationId === v.id }"
        @click="selectedVariationId = v.id"
      >
        <span class="variation__dot"></span>
        <span class="variation__label">{{ v.variation_text }} / {{ v.weight_gram }} г.</span>
        <span class="variation__price">{{ formatPrice(v.price) }} ₽</span>
      </div>
    </div>

    <div class="merch-card__footer">
      <div v-if="qtyInCart > 0" class="qty-control">
        <button class="qty-btn" @click="decrement">
          <img src="/src/public/mn.png" alt="−" />
        </button>
        <span class="qty-num">{{ qtyInCart }}</span>
        <button class="qty-btn" @click="increment">
          <img src="/src/public/pl.png" alt="+" />
        </button>
      </div>
      <button v-else class="add-btn" @click="addFirst">
        <img src="/src/public/plus.png" alt="+" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Merchandise } from '@/services/api'
import { getImageUrl } from '@/services/api'

const props = defineProps<{
  merchandise: Merchandise
  cartQuantities: Record<string, number>
}>()

const emit = defineEmits<{
  addToCart: [merchandiseId: number, variationId: number, quantity: number]
}>()

const selectedVariationId = ref<number>(props.merchandise.variations[0]?.id ?? 0)

// Используем единую функцию для получения URL изображения
const imageUrl = computed(() => getImageUrl(props.merchandise.image))

const formatPrice = (price: number) => {
  return price.toLocaleString('ru-RU')
}

const onImgError = (e: Event) => {
  const img = e.target as HTMLImageElement
  console.warn(`Не удалось загрузить изображение: ${img.src}`)
  img.src = '/src/public/hap.png'
  img.onerror = null
}

const qtyInCart = computed(() => {
  const key = `${props.merchandise.id}_${selectedVariationId.value}`
  return props.cartQuantities[key] ?? 0
})

const addFirst = () => emit('addToCart', props.merchandise.id, selectedVariationId.value, 1)
const increment = () => emit('addToCart', props.merchandise.id, selectedVariationId.value, 1)
const decrement = () => emit('addToCart', props.merchandise.id, selectedVariationId.value, -1)
</script>

<style scoped>
/* Все стили остаются без изменений */
.merch-card {
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(8px);
  border-radius: 20px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.09);
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: transform 0.25s, box-shadow 0.25s;
}
.merch-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 32px rgba(233, 84, 78, 0.15);
}

.merch-card__img-wrap {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 14px;
  overflow: hidden;
  background: #f5f5f5;
  flex-shrink: 0;
}
.merch-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.merch-card:hover .merch-card__img { transform: scale(1.04); }

.merch-card__title {
  font-family: 'Courier New', Courier, monospace;
  font-size: 15px;
  font-weight: 800;
  color: #222;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  line-height: 1.2;
}

.merch-card__desc {
  font-family: 'Courier New', Courier, monospace;
  font-size: 12px;
  color: #888;
  text-align: center;
  line-height: 1.4;
}

.merch-card__variations {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.variation {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 1.5px solid #e8e8e8;
  border-radius: 30px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.variation:hover { border-color: #E9544E; background: rgba(233, 84, 78, 0.04); }
.variation--active { border-color: #E9544E; background: rgba(233, 84, 78, 0.08); }

.variation__dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ddd;
  flex-shrink: 0;
  transition: background 0.2s, box-shadow 0.2s;
}
.variation--active .variation__dot {
  background: #E9544E;
  box-shadow: 0 0 0 3px rgba(233, 84, 78, 0.2);
}

.variation__label {
  flex: 1;
  font-family: 'Courier New', Courier, monospace;
  font-size: 12px;
  color: #444;
}

.variation__price {
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  font-weight: 800;
  color: #E9544E;
  white-space: nowrap;
}

.merch-card__footer {
  display: flex;
  justify-content: center;
  margin-top: auto;
  padding-top: 4px;
}

.add-btn {
  width: 48px;
  height: 48px;
  background: #E9544E;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, transform 0.2s;
  box-shadow: 0 4px 12px rgba(233, 84, 78, 0.35);
}
.add-btn:hover { background: #d43f39; transform: scale(1.08); }
.add-btn img { width: 22px; height: 22px; }

.qty-control {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 7px 16px;
  border-radius: 40px;
}

.qty-btn {
  
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, border-color 0.2s;
}
.qty-btn:hover { background: #E9544E; border-color: #E9544E; }
.qty-btn img { width: 20x; height: 20x; }
.qty-btn:hover img { filter: brightness(0) invert(1); }

.qty-num {
  font-family: 'Courier New', Courier, monospace;
  font-size: 23px;
  font-weight: 700;
  color: #333;
  min-width: 24px;
  text-align: center;
}
</style>