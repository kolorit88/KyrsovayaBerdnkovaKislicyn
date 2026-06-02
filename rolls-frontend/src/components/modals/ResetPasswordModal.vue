// FILE: src/components/modals/ResetPasswordModal.vue
<template>
  <div v-if="isOpen" class="reset-overlay" @click.self="$emit('close')">
    <div class="reset-modal">
      <button class="close-reset" @click="$emit('close')">×</button>
      
      <div class="reset-content">
        <h2 class="reset-title">Сброс пароля</h2>
        
        <div class="reset-form">
          <div class="input-group">
            <input 
              type="password" 
              v-model="localNewPassword"
              placeholder="Новый пароль"
              class="reset-input"
              @keyup.enter="submitReset"
            />
          </div>
          <div class="input-group">
            <input 
              type="password" 
              v-model="confirmPassword"
              placeholder="Подтвердите пароль"
              class="reset-input"
              @keyup.enter="submitReset"
            />
          </div>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <button class="reset-submit" :disabled="isLoading" @click="submitReset">
            {{ isLoading ? 'Сохранение...' : 'Сохранить пароль' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  isOpen: boolean
  token: string
  isLoading?: boolean
}>()

const emit = defineEmits<{
  close: []
  reset: [token: string, newPassword: string]
}>()

const localNewPassword = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')

watch(() => props.isOpen, (open) => {
  if (!open) {
    localNewPassword.value = ''
    confirmPassword.value = ''
    errorMessage.value = ''
  }
})

const submitReset = () => {
  errorMessage.value = ''
  
  if (localNewPassword.value.length < 6) {
    errorMessage.value = 'Пароль должен содержать минимум 6 символов'
    return
  }
  
  if (localNewPassword.value !== confirmPassword.value) {
    errorMessage.value = 'Пароли не совпадают'
    return
  }
  
  emit('reset', props.token, localNewPassword.value)
}
</script>

<style scoped>
.reset-overlay {
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
}

.reset-modal {
  position: relative;
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 450px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease;
}

.close-reset {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 32px;
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
  transition: all 0.3s ease;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-reset:hover {
  color: #E9544E;
  transform: scale(1.1);
  background-color: rgba(233, 84, 78, 0.1);
}

.reset-content {
  text-align: center;
}

.reset-title {
  font-family: 'Courier New', Courier, monospace;
  font-size: 28px;
  color: #333;
  margin-bottom: 30px;
  font-weight: 700;
}

.reset-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  width: 100%;
}

.reset-input {
  width: 100%;
  padding: 14px 18px;
  font-size: 16px;
  font-family: 'Courier New', Courier, monospace;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  transition: all 0.3s ease;
  outline: none;
}

.reset-input:focus {
  border-color: #E9544E;
  box-shadow: 0 0 0 3px rgba(233, 84, 78, 0.1);
}

.reset-submit {
  background: #E9544E;
  color: white;
  border: none;
  padding: 14px 28px;
  font-size: 18px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.reset-submit:hover:not(:disabled) {
  background: #d43f39;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(233, 84, 78, 0.3);
}

.reset-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #E9544E;
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  margin-top: -10px;
  text-align: center;
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
  .reset-modal {
    padding: 30px 25px;
    width: 95%;
  }
  
  .reset-title {
    font-size: 24px;
    margin-bottom: 25px;
  }
  
  .reset-input {
    padding: 12px 16px;
    font-size: 14px;
  }
  
  .reset-submit {
    padding: 12px 24px;
    font-size: 16px;
  }
}
</style>