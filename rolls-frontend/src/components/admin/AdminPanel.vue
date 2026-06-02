// src/components/admin/AdminPanel.vue
<template>
  <div class="admin-panel">
    <!-- Фоновые круги как на главной -->
    <div class="bg-circles" aria-hidden="true">
      <div class="circle c1"></div>
      <div class="circle c2"></div>
      <div class="circle c3"></div>
      <div class="circle c4"></div>
      <div class="circle c5"></div>
    </div>

    <div class="admin-container">
      <!-- Статистика -->
      <div class="stats-section">
        <div class="stats-header">
          <h1 class="stats-title">Статистика заказов</h1>
          <button class="history-btn" @click="openHistoryModal">История заказов</button>
        </div>
        
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon"></div>
            <div class="stat-info">
              <div class="stat-value">{{ dailyOrders.length }}</div>
              <div class="stat-label">ЗАКАЗОВ ЗА СЕГОДНЯ</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon"></div>
            <div class="stat-info">
              <div class="stat-value">{{ dailyRevenue }} ₽</div>
              <div class="stat-label">ВЫРУЧКА ЗА СЕГОДНЯ</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon"></div>
            <div class="stat-info">
              <div class="stat-value">{{ avgOrderValue }} ₽</div>
              <div class="stat-label">СРЕДНИЙ ЧЕК</div>
            </div>
          </div>
        </div>
        
        <!-- Круговая диаграмма -->
        <div class="chart-card">
          <h3 class="chart-title">Распределение заказов по времени суток</h3>
          <div class="pie-chart-container">
            <svg viewBox="0 0 200 200" class="pie-chart">
              <circle cx="100" cy="100" r="80" fill="none" stroke="#E9544E" 
                :stroke-dasharray="getPieDashArray(morningPercent)" 
                stroke-width="40" transform="rotate(-90 100 100)"/>
              <circle cx="100" cy="100" r="80" fill="none" stroke="#FFBF9C" 
                :stroke-dasharray="getPieDashArray(dayPercent)" 
                stroke-width="40" transform="rotate(-90 100 100)"
                :stroke-dashoffset="getPieOffset(morningPercent)"/>
              <circle cx="100" cy="100" r="80" fill="none" stroke="#E8A87C" 
                :stroke-dasharray="getPieDashArray(eveningPercent)" 
                stroke-width="40" transform="rotate(-90 100 100)"
                :stroke-dashoffset="getPieOffset(morningPercent + dayPercent)"/>
              <circle cx="100" cy="100" r="80" fill="none" stroke="#C38D6F" 
                :stroke-dasharray="getPieDashArray(nightPercent)" 
                stroke-width="40" transform="rotate(-90 100 100)"
                :stroke-dashoffset="getPieOffset(morningPercent + dayPercent + eveningPercent)"/>
            </svg>
            <div class="pie-legend">
              <div class="legend-item"><span class="legend-color morning"></span>Утро (6:00-12:00) - {{ morningOrders }}</div>
              <div class="legend-item"><span class="legend-color day"></span>День (12:00-18:00) - {{ dayOrders }}</div>
              <div class="legend-item"><span class="legend-color evening"></span>Вечер (18:00-00:00) - {{ eveningOrders }}</div>
              <div class="legend-item"><span class="legend-color night"></span>Ночь (00:00-6:00) - {{ nightOrders }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Заказы -->
      <div class="orders-section">
        <div class="orders-header">
          <h2 class="orders-title">ЗАКАЗЫ НА СЕГОДНЯ</h2>
          <div class="orders-actions">
            <div class="auto-refresh-indicator" v-if="autoRefreshEnabled">
              <span class="refresh-dot"></span>
              Автообновление 10с
            </div>
            <button class="refresh-btn" @click="manualRefresh" :disabled="loading">
               {{ loading ? 'ЗАГРУЗКА...' : 'ОБНОВИТЬ' }}
            </button>
          </div>
        </div>
        
        <div v-if="initialLoading" class="state-loading">
          <div class="spinner"></div>
          <p>Загрузка заказов...</p>
        </div>
        
        <div v-else-if="dailyOrders.length === 0" class="empty-orders">
          <p>Сегодня пока нет заказов</p>
        </div>
        
        <div v-else class="orders-list">
          <div 
            v-for="order in dailyOrders" 
            :key="order.id" 
            class="order-card"
            :class="{ completed: order.completed, 'new-order': order.isNew }"
          >
            <div class="order-header">
              <div class="order-number">ЗАКАЗ #{{ order.id }}</div>
              <div class="order-time">{{ formatTime(order.created_at) }}</div>
              <div v-if="order.isNew" class="new-badge">НОВЫЙ</div>
            </div>
            
            <div class="order-info">
              <div class="info-row">
                <span class="info-label">Имя:</span>
                <span class="info-value">{{ order.user_name }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Телефон:</span>
                <span class="info-value">{{ order.user_phone_number }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Адрес:</span>
                <span class="info-value">{{ order.user_address }}</span>
              </div>
            </div>
            
            <!-- Состав заказа как на главной -->
            <div class="order-items">
              <div class="items-title">Состав заказа:</div>
              <div class="merchandise-list">
                <div v-for="(item, idx) in order.items" :key="item.id" class="merchandise-item">
                  <div class="item-img-wrapper">
                    <img 
                      :src="getItemImage(item)" 
                      :alt="getItemName(item)"
                      class="item-img"
                      @error="handleImageError"
                    />
                  </div>
                  <div class="item-details">
                    <div class="item-name">{{ getItemName(item) }}</div>
                    <div class="item-variation">{{ getItemVariation(item) }}</div>
                    <div class="item-price-row">
                      <div class="item-quantity">x{{ item.quantity }}</div>
                      <div class="item-price">{{ parseFloat(item.price_at_time).toFixed(0) }} ₽</div>
                      <div class="item-total">{{ parseFloat(item.price_at_time) * item.quantity }} ₽</div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="order-total">Итого: {{ calculateOrderTotal(order) }} ₽</div>
            </div>
            
            <button 
              class="complete-btn" 
              :class="{ completed: order.completed }"
              @click="toggleComplete(order)"
              :disabled="updatingOrderId === order.id"
            >
              {{ updatingOrderId === order.id ? 'СОХРАНЕНИЕ...' : (order.completed ? 'ВЫПОЛНЕН' : 'ОТМЕТИТЬ ВЫПОЛНЕННЫМ') }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Модалка истории -->
    <div v-if="showHistoryModal" class="modal-overlay" @click.self="closeHistoryModal">
      <div class="history-modal">
        <div class="modal-header">
          <h2>ИСТОРИЯ ЗАКАЗОВ</h2>
          <button class="modal-close" @click="closeHistoryModal">×</button>
        </div>
        <div class="modal-body">
          <div class="date-selector">
            <label>Выберите дату:</label>
            <input type="date" v-model="selectedDate" />
            <button class="load-history-btn" @click="loadHistoryOrders" :disabled="historyLoading">
              {{ historyLoading ? 'ЗАГРУЗКА...' : 'ПОКАЗАТЬ' }}
            </button>
          </div>
          
          <div v-if="historyLoading" class="state-loading">
            <div class="spinner"></div>
            <p>Загрузка истории...</p>
          </div>
          
          <div v-else-if="historyOrders.length === 0" class="empty-history">
            <p>За выбранную дату заказов нет</p>
          </div>
          
          <div v-else class="history-list">
            <div v-for="order in historyOrders" :key="order.id" class="history-order-card">
              <div class="history-order-header">
                <span class="history-order-number">ЗАКАЗ #{{ order.id }}</span>
                <span class="history-order-time">{{ formatDateTime(order.created_at) }}</span>
              </div>
              <div class="history-order-info">
                <div><strong>{{ order.user_name }}</strong> | {{ order.user_phone_number }}</div>
                <div>{{ order.user_address }}</div>
                <div class="history-order-total">Сумма: {{ calculateOrderTotal(order) }} ₽</div>
              </div>
              <div class="history-order-items">
                <div class="items-title-small">Состав заказа:</div>
                <div class="merchandise-list">
                  <div v-for="item in order.items" :key="item.id" class="merchandise-item small">
                    <div class="item-details">
                      <div class="item-name">{{ getItemName(item) }}</div>
                      <div class="item-price-row">
                        <span class="item-quantity">x{{ item.quantity }}</span>
                        <span class="item-price">{{ parseFloat(item.price_at_time).toFixed(0) }} ₽</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
// ВАЖНО: используем настроенный axiosInstance вместо обычного axios
import { axiosInstance } from '@/services/api'
import merchandiseDataRaw from '@/data/merchandise.json'

// Типы
interface OrderItemResponse {
  id: number
  variation_id: number
  quantity: number
  price_at_time: string
}

interface OrderResponse {
  id: number
  user_name: string
  user_email: string
  user_phone_number: string
  user_address: string
  created_at: string
  items: OrderItemResponse[]
  status: 'PENDING' | 'COMPLETED'
}

interface ExtendedOrder extends OrderResponse {
  completed: boolean
  isNew?: boolean
}

interface Variation {
  id: number
  merchandise_id: number
  quantity: number
  price: number
  variation_text: string
  weight_gram: number
}

interface Merchandise {
  id: number
  category_id: number
  name: string
  description: string
  image: string
  variations: Variation[]
}

interface Category {
  id: number
  name: string
  slug: string
  description: string
  merchandises: Merchandise[]
}

// Загружаем данные из merchandise.json
const categoriesData = ref<Category[]>([])

// Строим карту товаров и вариаций
const merchandiseMap = new Map<number, Merchandise>()
const variationMap = new Map<number, { merchandise: Merchandise; variation: Variation }>()

const initMerchandiseData = () => {
  categoriesData.value = (merchandiseDataRaw as any).categories || []
  
  for (const category of categoriesData.value) {
    for (const merchandise of category.merchandises) {
      merchandiseMap.set(merchandise.id, merchandise)
      for (const variation of merchandise.variations) {
        variationMap.set(variation.id, { merchandise, variation })
      }
    }
  }
}

const API_BASE = '/api'

const allOrders = ref<ExtendedOrder[]>([])
const loading = ref(false)
const initialLoading = ref(true)
const showHistoryModal = ref(false)
const historyOrders = ref<OrderResponse[]>([])
const historyLoading = ref(false)
const selectedDate = ref(new Date().toISOString().split('T')[0])
const updatingOrderId = ref<number | null>(null)
const autoRefreshEnabled = ref(true)
let refreshInterval: number | null = null
let lastOrderIds = new Set<number>()

// Заказы за сегодня
const dailyOrders = computed(() => {
  const today = new Date().toDateString()
  return allOrders.value.filter(order => {
    const orderDate = new Date(order.created_at).toDateString()
    return orderDate === today
  })
})

const dailyRevenue = computed(() => {
  return dailyOrders.value.reduce((sum, order) => sum + calculateOrderTotal(order), 0)
})

const avgOrderValue = computed(() => {
  if (dailyOrders.value.length === 0) return 0
  return Math.round(dailyRevenue.value / dailyOrders.value.length)
})

// Распределение по времени
const morningOrders = computed(() => {
  return dailyOrders.value.filter(order => {
    const hour = new Date(order.created_at).getHours()
    return hour >= 6 && hour < 12
  }).length
})

const dayOrders = computed(() => {
  return dailyOrders.value.filter(order => {
    const hour = new Date(order.created_at).getHours()
    return hour >= 12 && hour < 18
  }).length
})

const eveningOrders = computed(() => {
  return dailyOrders.value.filter(order => {
    const hour = new Date(order.created_at).getHours()
    return hour >= 18 && hour < 24
  }).length
})

const nightOrders = computed(() => {
  return dailyOrders.value.filter(order => {
    const hour = new Date(order.created_at).getHours()
    return hour >= 0 && hour < 6
  }).length
})

const totalOrdersCount = computed(() => dailyOrders.value.length)

const morningPercent = computed(() => totalOrdersCount.value === 0 ? 0 : (morningOrders.value / totalOrdersCount.value) * 100)
const dayPercent = computed(() => totalOrdersCount.value === 0 ? 0 : (dayOrders.value / totalOrdersCount.value) * 100)
const eveningPercent = computed(() => totalOrdersCount.value === 0 ? 0 : (eveningOrders.value / totalOrdersCount.value) * 100)
const nightPercent = computed(() => totalOrdersCount.value === 0 ? 0 : (nightOrders.value / totalOrdersCount.value) * 100)

const getPieDashArray = (percent: number) => {
  const circumference = 2 * Math.PI * 80
  const value = (percent / 100) * circumference
  return `${value} ${circumference}`
}

const getPieOffset = (accumulatedPercent: number) => {
  const circumference = 2 * Math.PI * 80
  return -((accumulatedPercent / 100) * circumference)
}

const calculateOrderTotal = (order: OrderResponse) => {
  return order.items.reduce((sum, item) => {
    return sum + (parseFloat(item.price_at_time) * item.quantity)
  }, 0)
}

// Получение названия товара из JSON
const getItemName = (item: OrderItemResponse): string => {
  const data = variationMap.get(item.variation_id)
  if (data) {
    return data.merchandise.name
  }
  return `Товар #${item.variation_id}`
}

// Получение вариации товара
const getItemVariation = (item: OrderItemResponse): string => {
  const data = variationMap.get(item.variation_id)
  if (data) {
    return data.variation.variation_text
  }
  return ''
}

// Получение изображения товара
const getItemImage = (item: OrderItemResponse): string => {
  const data = variationMap.get(item.variation_id)
  if (data && data.merchandise.image) {
    return `/src/public/${data.merchandise.image}`
  }
  return '/src/public/hap.png'
}

const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement
  img.src = '/src/public/hap.png'
}

const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const updateOrderStatus = async (orderId: number, status: 'PENDING' | 'COMPLETED') => {
  try {
    // Используем axiosInstance вместо axios
    await axiosInstance.patch(`/api/orders/${orderId}/status`, { status })
    return true
  } catch (error) {
    console.error('Ошибка обновления статуса:', error)
    return false
  }
}

const toggleComplete = async (order: ExtendedOrder) => {
  if (updatingOrderId.value === order.id) return
  
  updatingOrderId.value = order.id
  const newStatus = order.completed ? 'PENDING' : 'COMPLETED'
  
  const success = await updateOrderStatus(order.id, newStatus)
  
  if (success) {
    order.completed = !order.completed
    order.status = newStatus
    
    const originalOrder = allOrders.value.find(o => o.id === order.id)
    if (originalOrder) {
      originalOrder.status = newStatus
      originalOrder.completed = order.completed
    }
    
    saveCompletedStatus()
  }
  
  updatingOrderId.value = null
}

const saveCompletedStatus = () => {
  const completedIds = allOrders.value.filter(o => o.completed).map(o => o.id)
  localStorage.setItem('completedOrders', JSON.stringify(completedIds))
}

const loadCompletedStatus = () => {
  const saved = localStorage.getItem('completedOrders')
  if (saved) {
    const completedIds = JSON.parse(saved) as number[]
    allOrders.value = allOrders.value.map(order => ({
      ...order,
      completed: completedIds.includes(order.id),
      isNew: false
    }))
  }
}

const loadAllOrders = async (): Promise<OrderResponse[]> => {
  try {
    // Используем axiosInstance вместо axios
    const response = await axiosInstance.get<{ orders: OrderResponse[] }>('/api/orders')
    return response.data.orders || []
  } catch (error) {
    console.error('Ошибка загрузки заказов:', error)
    return []
  }
}

const loadOrders = async (isAutoRefresh = false) => {
  if (!isAutoRefresh) loading.value = true
  
  try {
    const orders = await loadAllOrders()
    const currentOrderIds = new Set(orders.map(o => o.id))
    const newOrders = orders.filter(order => !lastOrderIds.has(order.id))
    
    lastOrderIds = currentOrderIds
    
    const mappedOrders = orders.map(order => ({
      ...order,
      completed: order.status === 'COMPLETED',
      isNew: !isAutoRefresh ? false : newOrders.some(n => n.id === order.id)
    }))
    
    const existingCompleted = new Map(allOrders.value.map(o => [o.id, o.completed]))
    mappedOrders.forEach(order => {
      if (existingCompleted.has(order.id)) {
        order.completed = existingCompleted.get(order.id)!
      }
    })
    
    allOrders.value = mappedOrders
    
    if (newOrders.length > 0 && isAutoRefresh) {
      setTimeout(() => {
        allOrders.value = allOrders.value.map(order => ({ ...order, isNew: false }))
      }, 3000)
    }
    
    loadCompletedStatus()
  } catch (error) {
    console.error('Ошибка загрузки заказов:', error)
  } finally {
    if (!isAutoRefresh) loading.value = false
    initialLoading.value = false
  }
}

const manualRefresh = async () => {
  await loadOrders(false)
}

const startAutoRefresh = () => {
  if (refreshInterval) clearInterval(refreshInterval)
  refreshInterval = window.setInterval(() => {
    if (autoRefreshEnabled.value) loadOrders(true)
  }, 10000)
}

const stopAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

const loadOrdersByDate = async (date: string): Promise<OrderResponse[]> => {
  try {
    const allOrdersData = await loadAllOrders()
    const startDate = new Date(date)
    startDate.setHours(0, 0, 0, 0)
    const endDate = new Date(date)
    endDate.setHours(23, 59, 59, 999)
    
    return allOrdersData.filter(order => {
      const orderDate = new Date(order.created_at)
      return orderDate >= startDate && orderDate <= endDate
    })
  } catch (error) {
    console.error('Ошибка загрузки истории:', error)
    return []
  }
}

const openHistoryModal = async () => {
  showHistoryModal.value = true
  await loadHistoryOrders()
}

const closeHistoryModal = () => {
  showHistoryModal.value = false
  historyOrders.value = []
}

const loadHistoryOrders = async () => {
  historyLoading.value = true
  try {
    historyOrders.value = await loadOrdersByDate(selectedDate.value)
  } catch (error) {
    console.error('Ошибка загрузки истории:', error)
    historyOrders.value = []
  } finally {
    historyLoading.value = false
  }
}

onMounted(async () => {
  initMerchandiseData()
  await loadOrders(false)
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
/* Стили остаются без изменений */
.admin-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100vh;
  background: #f5f5f5;
  padding: 20px;
  overflow-y: auto;
  overflow-x: hidden;
}

.bg-circles {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.4;
}

.c1 { width: 400px; height: 400px; background: #E9544E; top: -100px; left: -100px; }
.c2 { width: 500px; height: 500px; background: #FFBF9C; bottom: -150px; right: -150px; }
.c3 { width: 300px; height: 300px; background: #FFBF9C; top: 50%; left: 20%; }
.c4 { width: 350px; height: 350px; background: #ff8c94; top: 20%; right: 10%; }
.c5 { width: 250px; height: 250px; background: #ff8c94; bottom: 30%; left: 10%; }

.admin-container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.stats-section { margin-bottom: 30px; }
.stats-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 15px; }
.stats-title { font-family: 'ChinaCyr', 'Courier New', monospace; font-size: 32px; color: #333; margin: 0; letter-spacing: 2px; }
.history-btn { background: #E9544E; color: white; border: none; padding: 12px 24px; font-size: 14px; font-family: 'Courier New', monospace; font-weight: 700; border-radius: 12px; cursor: pointer; transition: all 0.3s ease; }
.history-btn:hover { background: #d43f39; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(233, 84, 78, 0.3); }
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }
.stat-card { background: rgba(255, 255, 255, 0.92); backdrop-filter: blur(8px); border-radius: 20px; padding: 24px; display: flex; align-items: center; gap: 20px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); transition: transform 0.3s; }
.stat-card:hover { transform: translateY(-5px); }
.stat-icon { font-size: 48px; }
.stat-info { flex: 1; }
.stat-value { font-size: 32px; font-weight: bold; color: #E9544E; font-family: 'Courier New', monospace; }
.stat-label { font-size: 12px; color: #666; font-family: 'Courier New', monospace; margin-top: 5px; letter-spacing: 1px; }
.chart-card { background: rgba(255, 255, 255, 0.92); backdrop-filter: blur(8px); border-radius: 20px; padding: 24px; margin-bottom: 30px; }
.chart-title { font-family: 'ChinaCyr', 'Courier New', monospace; font-size: 20px; color: #333; margin-bottom: 20px; text-align: center; }
.pie-chart-container { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 40px; }
.pie-chart { width: 200px; height: 200px; }
.pie-legend { flex: 1; min-width: 200px; }
.legend-item { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; font-family: 'Courier New', monospace; font-size: 14px; color: #555; }
.legend-color { width: 20px; height: 20px; border-radius: 50%; }
.legend-color.morning { background: #E9544E; }
.legend-color.day { background: #FFBF9C; }
.legend-color.evening { background: #E8A87C; }
.legend-color.night { background: #C38D6F; }

.orders-section { background: rgba(255, 255, 255, 0.92); backdrop-filter: blur(8px); border-radius: 20px; padding: 24px; }
.orders-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 2px solid #f0f0f0; flex-wrap: wrap; gap: 12px; }
.orders-title { font-family: 'ChinaCyr', 'Courier New', monospace; font-size: 24px; color: #333; margin: 0; letter-spacing: 2px; }
.orders-actions { display: flex; align-items: center; gap: 16px; }
.auto-refresh-indicator { display: flex; align-items: center; gap: 8px; font-family: 'Courier New', monospace; font-size: 12px; color: #E9544E; background: rgba(255, 191, 156, 0.1); padding: 6px 12px; border-radius: 20px; }
.refresh-dot { width: 8px; height: 8px; background: #E9544E; border-radius: 50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
.refresh-btn { background: #E9544E; color: white; border: none; padding: 8px 16px; font-size: 12px; font-family: 'Courier New', monospace; font-weight: 700; border-radius: 8px; cursor: pointer; transition: all 0.3s ease; }
.refresh-btn:hover:not(:disabled) { background: #d43f39; transform: scale(1.02); }

.orders-list { display: flex; flex-direction: column; gap: 20px; max-height: 550px; overflow-y: auto; }
.order-card { background: white; border-radius: 20px; padding: 20px; transition: all 0.3s ease; border: 1px solid #e0e0e0; }
.order-card.new-order { animation: highlight 0.5s ease; border-color: #E9544E; box-shadow: 0 0 0 2px rgba(233, 84, 78, 0.3); }
@keyframes highlight { 0% { background: rgba(233, 84, 78, 0.2); } 100% { background: white; } }
.order-card.completed { background: #e8e8e8; opacity: 0.7; }
.order-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #e0e0e0; flex-wrap: wrap; gap: 10px; }
.order-number { font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold; color: #E9544E; }
.order-time { font-family: 'Courier New', monospace; font-size: 14px; color: #999; }
.new-badge { background: #E9544E; color: white; font-size: 10px; font-weight: bold; padding: 2px 8px; border-radius: 12px; }

.order-info { margin-bottom: 20px; }
.info-row { display: flex; margin-bottom: 8px; font-family: 'Courier New', monospace; font-size: 14px; flex-wrap: wrap; }
.info-label { width: 70px; font-weight: bold; color: #666; }
.info-value { flex: 1; color: #333; }

.order-items { margin-bottom: 20px; }
.items-title { font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; color: #333; margin-bottom: 12px; letter-spacing: 1px; }
.merchandise-list { display: flex; flex-direction: column; gap: 12px; }
.merchandise-item { display: flex; gap: 15px; padding: 12px; background: #f9f9f9; border-radius: 12px; border-left: 3px solid #E9544E; }
.merchandise-item.small { padding: 8px; }
.item-img-wrapper { width: 60px; height: 60px; flex-shrink: 0; border-radius: 10px; overflow: hidden; background: #e0e0e0; }
.item-img { width: 100%; height: 100%; object-fit: cover; }
.item-details { flex: 1; }
.item-name { font-family: 'Courier New', monospace; font-size: 15px; font-weight: 700; color: #333; margin-bottom: 4px; }
.item-variation { font-family: 'Courier New', monospace; font-size: 12px; color: #888; margin-bottom: 6px; }
.item-price-row { display: flex; gap: 15px; align-items: center; flex-wrap: wrap; }
.item-quantity { font-family: 'Courier New', monospace; font-size: 13px; background: #e0e0e0; padding: 2px 10px; border-radius: 15px; color: #555; }
.item-price { font-family: 'Courier New', monospace; font-size: 14px; color: #E9544E; font-weight: bold; }
.item-total { font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; color: #333; }
.order-total { text-align: right; font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold; color: #E9544E; margin-top: 15px; padding-top: 12px; border-top: 1px dashed #e0e0e0; }

.complete-btn { width: 100%; background: white; border: 2px solid #E9544E; padding: 12px; font-family: 'Courier New', monospace; font-size: 14px; font-weight: 700; border-radius: 12px; cursor: pointer; transition: all 0.3s ease; color: #E9544E; letter-spacing: 1px; }
.complete-btn:hover:not(:disabled) { background: #E9544E; color: white; transform: translateY(-2px); }
.complete-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.complete-btn.completed { background: #E9544E; border-color: #E9544E; color: white; opacity: 0.6; }

.state-loading { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px; gap: 20px; }
.spinner { width: 48px; height: 48px; border: 3px solid #e0e0e0; border-top-color: #E9544E; border-radius: 50%; animation: spin 0.9s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-orders { text-align: center; padding: 60px; color: #999; font-family: 'Courier New', monospace; }

.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(5px); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.history-modal { background: white; border-radius: 20px; width: 90%; max-width: 800px; max-height: 85vh; display: flex; flex-direction: column; animation: slideIn 0.3s ease; }
@keyframes slideIn { from { transform: translateY(-50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 2px solid #f0f0f0; }
.modal-header h2 { font-family: 'ChinaCyr', 'Courier New', monospace; font-size: 24px; color: #333; margin: 0; }
.modal-close { background: none; border: none; font-size: 32px; cursor: pointer; color: #999; transition: color 0.3s; }
.modal-close:hover { color: #E9544E; }
.modal-body { flex: 1; overflow-y: auto; padding: 24px; }
.date-selector { display: flex; gap: 12px; align-items: center; margin-bottom: 24px; flex-wrap: wrap; }
.date-selector label { font-family: 'Courier New', monospace; font-weight: bold; color: #333; }
.date-selector input { padding: 8px 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-family: 'Courier New', monospace; }
.load-history-btn { background: #E9544E; color: white; border: none; padding: 8px 20px; border-radius: 8px; font-family: 'Courier New', monospace; font-weight: bold; cursor: pointer; }
.load-history-btn:hover:not(:disabled) { background: #d43f39; }
.empty-history { text-align: center; padding: 40px; color: #999; }
.history-list { display: flex; flex-direction: column; gap: 16px; }
.history-order-card { background: #f9f9f9; border-radius: 12px; padding: 16px; border: 1px solid #e0e0e0; }
.history-order-header { display: flex; justify-content: space-between; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #e0e0e0; }
.history-order-number { font-family: 'Courier New', monospace; font-weight: bold; color: #E9544E; }
.history-order-time { font-size: 12px; color: #999; }
.history-order-info { font-family: 'Courier New', monospace; font-size: 13px; margin-bottom: 12px; line-height: 1.6; color: #0a0a0a; }
.history-order-total { color: #E9544E; font-weight: bold; margin-top: 8px; }
.items-title-small { font-family: 'Courier New', monospace; font-size: 12px; font-weight: bold; margin-bottom: 8px; color: #0a0a0a; }

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
  .pie-chart-container { flex-direction: column; }
  .merchandise-item { flex-direction: column; align-items: center; text-align: center; }
  .item-img-wrapper { width: 80px; height: 80px; }
  .info-row { flex-direction: column; }
  .info-label { width: auto; margin-bottom: 4px; }
  .stats-title { font-size: 24px; }
}
</style>