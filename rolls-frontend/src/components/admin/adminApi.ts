// src/services/adminApi.ts
import axios from 'axios'
import type { OrderResponse } from './api'

const ADMIN_API_BASE_URL = '/api/admin'

export const adminApi = {
  // Get all orders (for admin)
  async getAllOrders(): Promise<OrderResponse[]> {
    const response = await axios.get(`${ADMIN_API_BASE_URL}/orders`)
    return response.data.orders || []
  },

  // Get orders by date
  async getOrdersByDate(date: string): Promise<OrderResponse[]> {
    const response = await axios.get(`${ADMIN_API_BASE_URL}/orders`, {
      params: { date }
    })
    return response.data.orders || []
  },

  // Update order status
  async updateOrderStatus(orderId: number, status: string): Promise<void> {
    await axios.patch(`${ADMIN_API_BASE_URL}/orders/${orderId}`, { status })
  },

  // Get order statistics
  async getStatistics(): Promise<{
    dailyOrders: number
    dailyRevenue: number
    avgOrderValue: number
    timeDistribution: { morning: number; day: number; evening: number; night: number }
  }> {
    const response = await axios.get(`${ADMIN_API_BASE_URL}/statistics`)
    return response.data
  },

  // Get daily revenue chart data
  async getDailyRevenue(days: number = 7): Promise<{ date: string; revenue: number; orders: number }[]> {
    const response = await axios.get(`${ADMIN_API_BASE_URL}/statistics/daily`, {
      params: { days }
    })
    return response.data
  }
}