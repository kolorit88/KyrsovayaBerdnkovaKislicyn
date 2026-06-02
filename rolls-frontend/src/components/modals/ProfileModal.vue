// FILE: src/components/modals/ProfileModal.vue
<script setup lang="ts">
// Удаляем неиспользуемую функцию getStatusClass, так как секция заказов удаляется
// const getStatusClass = (status: string) => {
//   const statusMap: Record<string, string> = {
//     'Доставлен': 'delivered',
//     'В обработке': 'in-progress',
//     'Отменен': 'cancelled'
//   }
//   return statusMap[status] || ''
// }

defineProps<{
  isOpen: boolean
  user: any
  editForm: { name: string; phone: string; email: string; address: string }
  isEditing: boolean
  isLoading?: boolean
  orders: any[]  // prop остается для совместимости, но не используется
}>()

defineEmits<{
  close: []
  logout: []
  startEdit: []
  updateProfile: []
  cancelEdit: []
}>()
</script>

<template>
  <div v-if="isOpen && user" class="profile-overlay" @click.self="$emit('close')">
    <div class="profile-modal">
      <div class="profile-content">
        <div class="profile-header">
          <div class="profile-avatar">
            <div class="avatar-circle">
              {{ (editForm.name || user.name).charAt(0).toUpperCase() }}
            </div>
          </div>
          
          <div v-if="isEditing" class="profile-edit-header">
            <input 
              v-model="editForm.name"
              type="text"
              class="edit-input"
              placeholder="Ваше имя"
            />
            <input 
              v-model="editForm.phone"
              type="tel"
              class="edit-input"
              placeholder="Номер телефона"
            />
            <textarea
              v-model="editForm.address"
              class="edit-input edit-textarea"
              placeholder="Адрес доставки"
              rows="2"
            ></textarea>
          </div>
          <div v-else>
            <h2 class="profile-name">{{ user.name }}</h2>
            <p class="profile-phone">{{ user.phone }}</p>
            <p class="profile-address">{{ user.address || 'Адрес не указан' }}</p>
          </div>
          
          <div class="profile-actions">
            <button v-if="!isEditing" class="profile-edit-btn" @click="$emit('startEdit')">
              Редактировать
            </button>
            <div v-else class="edit-buttons">
              <button class="profile-save-btn" :disabled="isLoading" @click="$emit('updateProfile')">
                {{ isLoading ? 'Сохранение...' : 'Сохранить' }}
              </button>
              <button class="profile-cancel-btn" @click="$emit('cancelEdit')">
                Отмена
              </button>
            </div>
            <button class="profile-logout-btn" @click="$emit('logout')">Выйти</button>
          </div>
        </div>

        <div class="profile-info">
          <h3>Информация профиля</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Email:</span>
              <span class="info-value">{{ user.email }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Дата регистрации:</span>
              <span class="info-value">{{ user.registeredAt }}</span>
            </div>
          </div>
        </div>

        <!-- Секция истории заказов полностью удалена -->
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-overlay {
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
  overflow-y: auto;
  padding: 20px;
}

.profile-modal {
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

.profile-modal::-webkit-scrollbar {
  width: 8px;
}

.profile-modal::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.profile-modal::-webkit-scrollbar-thumb {
  background: #E9544E;
  border-radius: 10px;
}

.profile-content {
  padding: 20px 40px 40px 40px;
}

.profile-header {
  text-align: center;
  margin-bottom: 40px;
  padding-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-avatar {
  margin-bottom: 20px;
}

.avatar-circle {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #E9544E 0%, #FFBF9C 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  font-size: 48px;
  font-weight: bold;
  color: white;
  font-family: 'Courier New', Courier, monospace;
}

.profile-name {
  font-family: 'Courier New', Courier, monospace;
  font-size: 32px;
  color: #333;
  margin-bottom: 5px;
  text-align: center;
}

.profile-phone {
  font-family: 'Courier New', Courier, monospace;
  font-size: 16px;
  color: #666;
  margin-top: 5px;
}

.profile-address {
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  color: #888;
  margin-top: 8px;
  max-width: 300px;
  word-wrap: break-word;
}

.profile-actions {
  display: flex;
  gap: 12px;
  margin-top: 15px;
  flex-wrap: wrap;
  justify-content: center;
}

.profile-edit-btn {
  background: #E9544E;
  color: white;
  border: none;
  padding: 10px 25px;
  font-size: 14px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.profile-edit-btn:hover {
  background: #d43f39;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(233, 84, 78, 0.3);
}

.edit-buttons {
  display: flex;
  gap: 10px;
}

.profile-save-btn {
  background: #E9544E;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 14px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.profile-save-btn:hover:not(:disabled) {
  background: #d43f39;
  transform: translateY(-2px);
}

.profile-save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.profile-cancel-btn {
  background: #999;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 14px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.profile-cancel-btn:hover {
  background: #777;
  transform: translateY(-2px);
}

.profile-logout-btn {
  background: #E9544E;
  color: white;
  border: none;
  padding: 10px 25px;
  font-size: 14px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.profile-logout-btn:hover {
  background: #d43f39;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(233, 84, 78, 0.3);
}

.profile-info {
  margin-bottom: 20px;
}

.profile-info h3 {
  font-family: 'Courier New', Courier, monospace;
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #E9544E;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-label {
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
}

.info-value {
  font-family: 'Courier New', Courier, monospace;
  font-size: 18px;
  color: #333;
  font-weight: 500;
}

.profile-edit-header {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 15px;
  width: 100%;
  max-width: 300px;
}

.edit-input {
  padding: 10px 15px;
  font-size: 16px;
  font-family: 'Courier New', Courier, monospace;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  text-align: center;
  transition: border-color 0.3s;
}

.edit-textarea {
  text-align: left;
  resize: vertical;
}

.edit-input:focus {
  outline: none;
  border-color: #E9544E;
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
  .profile-content {
    padding: 20px;
  }
  
  .profile-name {
    font-size: 24px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .profile-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .edit-buttons {
    flex-direction: column;
    width: 100%;
    max-width: 200px;
  }
}

@media (max-width: 480px) {
  .avatar-circle {
    width: 70px;
    height: 70px;
    font-size: 32px;
  }
  
  .profile-name {
    font-size: 20px;
  }
  
  .profile-info h3 {
    font-size: 20px;
  }
  
  .info-value {
    font-size: 16px;
  }
  
  .edit-input {
    font-size: 14px;
    padding: 8px 12px;
  }
}
</style>