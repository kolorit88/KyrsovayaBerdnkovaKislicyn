<template>
  <div v-if="isOpen" class="cart-overlay" @click.self="$emit('close')">
    <div class="cart-modal">
      <div class="cart-content">
        <div class="cart-header">
          <h2 class="cart-title">Корзина</h2>
        </div>

        <div v-if="items.length > 0" class="cart-items">
          <div v-for="item in items" :key="`${item.merchandiseId}_${item.variationId}`" class="cart-item">
            <div class="cart-item-info">
              <h3 class="cart-item-name">{{ getMerchandiseName(item.merchandiseId) }}</h3>
              <p class="cart-item-variation">{{ getVariationText(item.variationId) }}</p>
              <p class="cart-item-price">{{ getVariationPrice(item.variationId) }} ₽</p>
            </div>
            <div class="cart-item-quantity">
              <button class="quantity-btn" @click="$emit('decrement', item.merchandiseId, item.variationId)">-</button>
              <span class="quantity">{{ item.quantity }}</span>
              <button class="quantity-btn" @click="$emit('increment', item.merchandiseId, item.variationId)">+</button>
            </div>
            <button class="remove-item" @click="$emit('remove', item.merchandiseId, item.variationId)">Удалить</button>
          </div>
          
          <div class="cart-footer">
            <div class="cart-total">
              <span>Итого:</span>
              <span class="total-price">{{ total }} ₽</span>
            </div>
            <button class="checkout-btn" :disabled="isLoading" @click="$emit('checkout')">
              {{ isLoading ? 'Оформление...' : 'Оформить заказ' }}
            </button>
          </div>
        </div>
        
        <div v-else class="empty-cart">
          <div class="empty-cart-icon"></div>
          <h3 class="empty-cart-title">Ваша корзина пуста</h3>
          <p class="empty-cart-text">Добавьте товары в корзину, чтобы сделать заказ</p>
          <button class="continue-shopping" @click="$emit('close')">Продолжить покупки</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  isOpen: boolean
  cartItems: Array<{ merchandiseId: number; variationId: number; quantity: number }>
  categories: any[]
  isLoading?: boolean
}>()

const emit = defineEmits<{
  close: []
  increment: [merchandiseId: number, variationId: number]
  decrement: [merchandiseId: number, variationId: number]
  remove: [merchandiseId: number, variationId: number]
  checkout: []
}>()

const getMerchandise = (merchandiseId: number) => {
  for (const category of props.categories) {
    const merch = category.merchandises?.find((m: any) => m.id === merchandiseId)
    if (merch) return merch
  }
  return null
}

const getVariation = (variationId: number) => {
  for (const category of props.categories) {
    for (const merch of category.merchandises || []) {
      const variation = merch.variations?.find((v: any) => v.id === variationId)
      if (variation) return variation
    }
  }
  return null
}

const getMerchandiseName = (merchandiseId: number) => {
  const merch = getMerchandise(merchandiseId)
  return merch?.name || 'Товар'
}

const getVariationText = (variationId: number) => {
  const variation = getVariation(variationId)
  return variation?.variation_text || ''
}

const getVariationPrice = (variationId: number) => {
  const variation = getVariation(variationId)
  return variation?.price || 0
}

const items = computed(() => props.cartItems)

const total = computed(() => {
  return props.cartItems.reduce((sum, item) => {
    const price = getVariationPrice(item.variationId)
    return sum + (price * item.quantity)
  }, 0)
})

const isLoading = computed(() => props.isLoading || false)
</script>

<style scoped>
.cart-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 3000;
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(5px);
  padding: 20px;
}

.cart-modal {
  position: relative;
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease;
}

.cart-modal::-webkit-scrollbar {
  width: 8px;
}

.cart-modal::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.cart-modal::-webkit-scrollbar-thumb {
  background: #E9544E;
  border-radius: 10px;
}

.cart-content {
  padding: 20px 40px 40px 40px;
}

.cart-header {
  text-align: center;
  margin-bottom: 30px;
  padding-top: 20px;
}

.cart-title {
  font-family: 'Courier New', Courier, monospace;
  font-size: 32px;
  color: #333;
  font-weight: 700;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cart-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.cart-item:hover {
  transform: translateX(5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.cart-item-info {
  flex: 2;
}

.cart-item-name {
  font-family: 'Courier New', Courier, monospace;
  font-size: 18px;
  color: #333;
  margin-bottom: 5px;
}

.cart-item-variation {
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  color: #666;
  margin-bottom: 5px;
}

.cart-item-price {
  font-family: 'Courier New', Courier, monospace;
  font-size: 16px;
  color: #E9544E;
  font-weight: bold;
}

.cart-item-quantity {
  display: flex;
  align-items: center;
  gap: 15px;
  margin: 0 20px;
}

.quantity-btn {
  width: 30px;
  height: 30px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.3s ease;
}

.quantity-btn:hover {
  background: #E9544E;
  color: white;
  border-color: #E9544E;
}

.quantity {
  font-family: 'Courier New', Courier, monospace;
  font-size: 16px;
  font-weight: bold;
  min-width: 30px;
  text-align: center;
  color: #312424;
}

.remove-item {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  transition: all 0.3s ease;
  padding: 5px 10px;
  border-radius: 6px;
}

.remove-item:hover {
  color: #E9544E;
  background-color: rgba(233, 84, 78, 0.1);
}

.cart-footer {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid #e0e0e0;
}

.cart-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Courier New', Courier, monospace;
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.total-price {
  color: #E9544E;
  font-size: 28px;
}

.checkout-btn {
  width: 100%;
  background: #E9544E;
  color: white;
  border: none;
  padding: 15px;
  font-size: 18px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.checkout-btn:hover:not(:disabled) {
  background: #d43f39;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(233, 84, 78, 0.3);
}

.checkout-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.empty-cart {
  text-align: center;
  padding: 60px 20px;
}

.empty-cart-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-cart-title {
  font-family: 'Courier New', Courier, monospace;
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

.empty-cart-text {
  font-family: 'Courier New', Courier, monospace;
  color: #999;
  margin-bottom: 30px;
}

.continue-shopping {
  background: #E9544E;
  color: white;
  border: none;
  padding: 12px 30px;
  font-size: 16px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.continue-shopping:hover {
  background: #d43f39;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(233, 84, 78, 0.3);
}

@keyframes slideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .cart-content {
    padding: 20px;
  }
  
  .cart-item {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .cart-item-quantity {
    margin: 10px 0;
  }
}

@media (max-width: 480px) {
  .cart-title {
    font-size: 20px;
  }
  
  .cart-total {
    font-size: 20px;
  }
  
  .total-price {
    font-size: 24px;
  }
}
</style>