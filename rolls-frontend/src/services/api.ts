import axios from 'axios'

// Единый источник конфигурации API
const API_BASE_URL = ''

export interface Variation {
  id: number
  merchandise_id: number
  quantity: number
  price: number
  variation_text: string
  weight_gram: number
}

export interface Merchandise {
  id: number
  category_id: number
  name: string
  description: string
  image: string
  variations: Variation[]
}

export interface Category {
  id: number
  name: string
  slug: string
  description: string
  merchandises: Merchandise[]
}

export interface OrderItemRequest {
  variation_id: number
  quantity: number
}

export interface CreateOrderRequest {
  items: OrderItemRequest[]
}

export interface OrderResponse {
  id: number
  user_name: string
  user_email: string
  user_phone_number: string
  user_address: string
  created_at: string
  items: OrderItemResponse[]
  status: string
}

export interface OrderItemResponse {
  id: number
  variation_id: number
  quantity: number
  price_at_time: string
}

export interface MessageResponse {
  message: string
}

export interface RegisterRequest {
  name: string
  email: string
  phone_number: string
  address: string
  password: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface UserResponse {
  id: string
  name: string
  email: string
  phone_number: string
  address: string
  role: string
  is_active: boolean
  created_at: string
}

// Флаг для предотвращения множественных refresh запросов
let isRefreshing = false
let failedQueue: Array<{
  resolve: (value: unknown) => void
  reject: (reason?: unknown) => void
}> = []

const processQueue = (error: Error | null, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

// Базовый URL для изображений
export const getImageUrl = (imagePath: string | null | undefined): string => {
  if (!imagePath) return '/src/public/hap.png'
  
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath
  }
  
  const cleanPath = imagePath.replace(/^\/+/, '')
  
  if (import.meta.env.DEV) {
    return `/api/${cleanPath}`
  } else {
    const API_HOST = import.meta.env.VITE_API_HOST || 'http://26.22.194.105:8000'
    return `${API_HOST}/${cleanPath}`
  }
}

// Создаем экземпляр axios с базовыми настройками
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true
})

// Интерцептор для логирования запросов
axiosInstance.interceptors.request.use((config) => {
  console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
  if (config.url && !config.url.startsWith('/api') && !config.url.startsWith('http')) {
    config.url = `/api${config.url}`
  }
  return config
})

// Интерцептор для обработки ошибок и refresh токена
axiosInstance.interceptors.response.use(
  (response) => {
    console.log(`[API] Response:`, response.status)
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    // Если ошибка 401 и это не запрос на refresh и не повторный запрос
    if (error.response?.status === 401 && 
        !originalRequest._retry && 
        originalRequest.url !== '/api/auth/refresh' &&
        originalRequest.url !== '/api/auth/login' &&
        originalRequest.url !== '/api/auth/register') {
      
      if (isRefreshing) {
        // Если уже идет refresh, добавляем запрос в очередь
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then(() => {
            return axiosInstance(originalRequest)
          })
          .catch((err) => {
            return Promise.reject(err)
          })
      }
      
      originalRequest._retry = true
      isRefreshing = true
      
      try {
        // Пытаемся обновить токен
        await axiosInstance.post('/auth/refresh')
        console.log('Токен успешно обновлен')
        
        // Обрабатываем очередь запросов
        processQueue(null)
        
        // Повторяем исходный запрос
        return axiosInstance(originalRequest)
      } catch (refreshError) {
        console.error('Ошибка обновления токена:', refreshError)
        
        // Обрабатываем очередь с ошибкой
        processQueue(refreshError as Error)
        
        // Если refresh не удался, разлогиниваем пользователя
        // Удаляем данные пользователя из localStorage
        localStorage.removeItem('currentUser')
        
        // Генерируем событие для приложения, что пользователь вышел
        window.dispatchEvent(new CustomEvent('auth:unauthorized'))
        
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }
    
    console.error(`[API] Error:`, error.response?.status, error.response?.data)
    return Promise.reject(error)
  }
)

export const api = {
  // ========== Товары ==========
  async getMerchandise(): Promise<Category[]> {
    try {
      const response = await axiosInstance.get('/merchandise')
      
      if (response.data && Array.isArray(response.data)) {
        const categoriesWithItems = response.data.filter(cat => 
          cat.merchandises && cat.merchandises.length > 0
        )
        return categoriesWithItems.length > 0 ? categoriesWithItems : response.data
      } else {
        throw new Error('Неверный формат данных от бэкенда')
      }
    } catch (error) {
      console.error('Ошибка при загрузке данных:', error)
      throw error
    }
  },

  // ========== Авторизация ==========
  async register(data: RegisterRequest): Promise<MessageResponse> {
    const response = await axiosInstance.post('/auth/register', data)
    return response.data
  },

  async login(email: string, password: string): Promise<MessageResponse> {
    const response = await axiosInstance.post('/auth/login', { login: email, password })
    return response.data
  },

  async verifyEmail(token: string): Promise<MessageResponse> {
    const response = await axiosInstance.get(`/auth/verify-email?token=${token}`)
    return response.data
  },
  
  async refreshToken(): Promise<MessageResponse> {
    const response = await axiosInstance.post('/auth/refresh')
    return response.data
  },

  async logout(): Promise<MessageResponse> {
    const response = await axiosInstance.post('/auth/logout')
    return response.data
  },

  async getCurrentUser(): Promise<UserResponse> {
    const response = await axiosInstance.get('/users/me')
    return response.data
  },

  async updateMe(data: { name?: string | null; phone_number?: string | null; address?: string | null }): Promise<UserResponse> {
    const response = await axiosInstance.patch('/users/me', data)
    return response.data
  },

  async changePassword(oldPassword: string, newPassword: string): Promise<MessageResponse> {
    const response = await axiosInstance.post('/users/me/password/change', {
      old_password: oldPassword,
      new_password: newPassword
    })
    return response.data
  },

  async requestPasswordReset(email: string): Promise<MessageResponse> {
    const response = await axiosInstance.post('/users/me/reset-password', { email })
    return response.data
  },

  async resetPassword(token: string, newPassword: string): Promise<MessageResponse> {
    const response = await axiosInstance.post('/users/me/reset-password/confirm', {
      token,
      new_password: newPassword
    })
    return response.data
  },

  // ========== Заказы ==========
  async createOrder(items: OrderItemRequest[]): Promise<OrderResponse> {
    const response = await axiosInstance.post('/orders', { items })
    return response.data
  },

  async getMyOrders(): Promise<OrderResponse[]> {
    const response = await axiosInstance.get('/orders')
    return response.data.orders || []
  },

  async getOrder(orderId: number): Promise<OrderResponse> {
    const response = await axiosInstance.get(`/orders/${orderId}`)
    return response.data
  },

  async checkConnection(): Promise<boolean> {
    try {
      await axiosInstance.get('/merchandise', { timeout: 3000 })
      return true
    } catch {
      return false
    }
  }
}

// Экспортируем сам axiosInstance на случай прямого использования
export { axiosInstance }