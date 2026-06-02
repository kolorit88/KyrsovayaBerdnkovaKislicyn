<template>
  <Teleport to="body">
    <Transition name="confirm-fade">
      <div v-if="isOpen" class="confirm-overlay" @click.self="handleCancel">
        <div class="confirm-modal" @click.stop>
          <div class="confirm-decoration" :class="type">
            <div class="confirm-icon" :class="type">
              <svg v-if="type === 'warning'" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 9v4M12 17h.01" stroke="currentColor" stroke-linecap="round"/>
                <path d="M12 2L2 20h20L12 2z" stroke="currentColor" stroke-linejoin="round"/>
              </svg>
              <svg v-else-if="type === 'error'" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" stroke="currentColor"/>
                <path d="M15 9l-6 6M9 9l6 6" stroke="currentColor" stroke-linecap="round"/>
              </svg>
              <svg v-else-if="type === 'success'" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" stroke="currentColor"/>
                <path d="M8 12l3 3 6-6" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <svg v-else width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" stroke="currentColor"/>
                <path d="M12 8v4M12 16h.01" stroke="currentColor" stroke-linecap="round"/>
              </svg>
            </div>
          </div>
          
          <div class="confirm-content">
            <h3 class="confirm-title">{{ title }}</h3>
            <p class="confirm-message">{{ message }}</p>
            
            <div class="confirm-actions">
              <button 
                v-if="showCancel" 
                class="confirm-btn cancel" 
                @click="handleCancel"
              >
                {{ cancelText }}
              </button>
              <button 
                class="confirm-btn confirm" 
                :class="type"
                @click="handleConfirm"
              >
                {{ confirmText }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'

type ConfirmType = 'info' | 'warning' | 'error' | 'success'

interface ConfirmOptions {
  title?: string
  message: string
  type?: ConfirmType
  confirmText?: string
  cancelText?: string
  showCancel?: boolean
  onConfirm?: () => void | Promise<void>
  onCancel?: () => void
}

const isOpen = ref(false)
let resolvePromise: ((value: boolean) => void) | null = null
let onConfirmCallback: (() => void | Promise<void>) | null = null
let onCancelCallback: (() => void) | null = null

const title = ref('Подтверждение')
const message = ref('')
const type = ref<ConfirmType>('info')
const confirmText = ref('OK')
const cancelText = ref('Отмена')
const showCancel = ref(true)

const handleConfirm = async () => {
  if (onConfirmCallback) {
    await onConfirmCallback()
  }
  if (resolvePromise) {
    resolvePromise(true)
  }
  isOpen.value = false
}

const handleCancel = () => {
  if (onCancelCallback) {
    onCancelCallback()
  }
  if (resolvePromise) {
    resolvePromise(false)
  }
  isOpen.value = false
}

const confirm = (options: ConfirmOptions): Promise<boolean> => {
  return new Promise((resolve) => {
    title.value = options.title || 'Подтверждение'
    message.value = options.message
    type.value = options.type || 'info'
    confirmText.value = options.confirmText || 'OK'
    cancelText.value = options.cancelText || 'Отмена'
    showCancel.value = options.showCancel !== false
    onConfirmCallback = options.onConfirm || null
    onCancelCallback = options.onCancel || null
    resolvePromise = resolve
    isOpen.value = true
  })
}

const alert = (message: string, title: string = 'Внимание') => {
  return confirm({
    title,
    message,
    type: 'info',
    confirmText: 'OK',
    showCancel: false
  })
}

const warning = (message: string, title: string = 'Предупреждение') => {
  return confirm({
    title,
    message,
    type: 'warning',
    confirmText: 'OK',
    showCancel: false
  })
}

const error = (message: string, title: string = 'Ошибка') => {
  return confirm({
    title,
    message,
    type: 'error',
    confirmText: 'OK',
    showCancel: false
  })
}

const success = (message: string, title: string = 'Успех') => {
  return confirm({
    title,
    message,
    type: 'success',
    confirmText: 'OK',
    showCancel: false
  })
}

defineExpose({
  confirm,
  alert,
  warning,
  error,
  success
})
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 20000;
}

.confirm-fade-enter-active,
.confirm-fade-leave-active {
  transition: all 0.3s ease;
}

.confirm-fade-enter-from,
.confirm-fade-leave-to {
  opacity: 0;
}

.confirm-fade-enter-from .confirm-modal,
.confirm-fade-leave-to .confirm-modal {
  transform: scale(0.9);
}

.confirm-modal {
  width: 90%;
  max-width: 420px;
  background: white;
  border-radius: 28px;
  overflow: hidden;
  animation: modalBounce 0.4s cubic-bezier(0.34, 1.2, 0.64, 1);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

@keyframes modalBounce {
  0% {
    transform: scale(0.9);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.confirm-decoration {
  padding: 32px 0 16px;
  text-align: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #f1f3f5 100%);
}

.confirm-decoration.warning {
  background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
}

.confirm-decoration.error {
  background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
}

.confirm-decoration.success {
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
}

.confirm-decoration.info {
  background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
}

.confirm-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.confirm-icon.warning svg {
  stroke: #ff9800;
}

.confirm-icon.error svg {
  stroke: #f44336;
}

.confirm-icon.success svg {
  stroke: #4caf50;
}

.confirm-icon.info svg {
  stroke: #2196f3;
}

.confirm-content {
  padding: 24px 28px 32px;
  text-align: center;
}

.confirm-title {
  font-family: 'Courier New', Courier, monospace;
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 12px;
}

.confirm-message {
  font-family: 'Courier New', Courier, monospace;
  font-size: 15px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 28px;
}

.confirm-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.confirm-btn {
  flex: 1;
  padding: 12px 24px;
  border: none;
  border-radius: 40px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.confirm-btn.cancel {
  background: #f0f0f0;
  color: #666;
}

.confirm-btn.cancel:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.confirm-btn.confirm {
  background: #E9544E;
  color: white;
  box-shadow: 0 4px 12px rgba(233, 84, 78, 0.3);
}

.confirm-btn.confirm:hover {
  background: #d43f39;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(233, 84, 78, 0.4);
}

.confirm-btn.confirm.warning {
  background: #ff9800;
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);
}

.confirm-btn.confirm.warning:hover {
  background: #f57c00;
}

.confirm-btn.confirm.error {
  background: #f44336;
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.confirm-btn.confirm.error:hover {
  background: #e53935;
}

.confirm-btn.confirm.success {
  background: #4caf50;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.confirm-btn.confirm.success:hover {
  background: #45a049;
}

@media (max-width: 480px) {
  .confirm-modal {
    max-width: 340px;
  }
  
  .confirm-content {
    padding: 20px 24px 28px;
  }
  
  .confirm-title {
    font-size: 20px;
  }
  
  .confirm-message {
    font-size: 14px;
  }
  
  .confirm-btn {
    padding: 10px 20px;
    font-size: 14px;
  }
  
  .confirm-icon {
    width: 64px;
    height: 64px;
  }
  
  .confirm-icon svg {
    width: 32px;
    height: 32px;
  }
}
</style>