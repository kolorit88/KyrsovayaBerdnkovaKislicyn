<template>
  <div v-if="isOpen" class="auth-overlay" @click.self="$emit('close')">
    <div class="auth-modal">
      <button class="close-auth" @click="$emit('close')">×</button>
      
      <div class="auth-content">
        <h2 class="auth-title">Добро пожаловать</h2>
        
        <!-- Форма входа -->
        <div v-if="mode === 'login'" class="auth-form">
          <div class="input-group">
            <input 
              type="email" 
              :value="loginForm.email"
              @input="$emit('update:loginForm', { ...loginForm, email: ($event.target as HTMLInputElement).value })"
              placeholder="Email"
              class="auth-input"
              @keyup.enter="$emit('login')"
            />
          </div>
          <div class="input-group">
            <input 
              type="password" 
              :value="loginForm.password"
              @input="$emit('update:loginForm', { ...loginForm, password: ($event.target as HTMLInputElement).value })"
              placeholder="Пароль"
              class="auth-input"
              @keyup.enter="$emit('login')"
            />
          </div>
          <div class="forgot-password-link" @click="$emit('forgotPassword')">
            Забыли пароль?
          </div>
          <button class="auth-submit" :disabled="isLoading" @click="$emit('login')">
            {{ isLoading ? 'Вход...' : 'Войти' }}
          </button>
          <p class="auth-switch">
            Нет аккаунта? 
            <span class="auth-link" @click="$emit('switchToRegister')">Зарегистрироваться</span>
          </p>
        </div>
        
        <!-- Форма регистрации -->
        <div v-else class="auth-form">
          <div class="input-group">
            <input 
              type="text" 
              :value="registerForm.name"
              @input="$emit('update:registerForm', { ...registerForm, name: ($event.target as HTMLInputElement).value })"
              placeholder="Имя"
              class="auth-input"
            />
          </div>
          <div class="input-group">
            <input 
              type="email" 
              :value="registerForm.email"
              @input="$emit('update:registerForm', { ...registerForm, email: ($event.target as HTMLInputElement).value })"
              placeholder="Email"
              class="auth-input"
            />
          </div>
          <div class="input-group">
            <input 
              type="tel" 
              :value="registerForm.phone"
              @input="$emit('update:registerForm', { ...registerForm, phone: ($event.target as HTMLInputElement).value })"
              placeholder="Номер телефона"
              class="auth-input"
            />
          </div>
          <div class="input-group">
            <input 
              type="text" 
              :value="registerForm.address"
              @input="$emit('update:registerForm', { ...registerForm, address: ($event.target as HTMLInputElement).value })"
              placeholder="Адрес доставки"
              class="auth-input"
            />
          </div>
          <div class="input-group">
            <input 
              type="password" 
              :value="registerForm.password"
              @input="$emit('update:registerForm', { ...registerForm, password: ($event.target as HTMLInputElement).value })"
              placeholder="Пароль"
              class="auth-input"
            />
          </div>
          <div class="input-group">
            <input 
              type="password" 
              :value="registerForm.confirmPassword"
              @input="$emit('update:registerForm', { ...registerForm, confirmPassword: ($event.target as HTMLInputElement).value })"
              placeholder="Подтвердите пароль"
              class="auth-input"
            />
          </div>
          <button class="auth-submit" :disabled="isLoading" @click="$emit('register')">
            {{ isLoading ? 'Регистрация...' : 'Зарегистрироваться' }}
          </button>
          <p class="auth-switch">
            Уже есть аккаунт? 
            <span class="auth-link" @click="$emit('switchToLogin')">Войти</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  isOpen: boolean
  mode: 'login' | 'register'
  loginForm: { email: string; password: string }
  registerForm: { name: string; email: string; phone: string; address: string; password: string; confirmPassword: string }
  isLoading?: boolean
}>()

defineEmits<{
  close: []
  login: []
  register: []
  forgotPassword: []
  switchToLogin: []
  switchToRegister: []
  'update:loginForm': [form: { email: string; password: string }]
  'update:registerForm': [form: { name: string; email: string; phone: string; address: string; password: string; confirmPassword: string }]
}>()
</script>

<style scoped>
.auth-overlay {
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

.auth-modal {
  position: relative;
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 450px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease;
}

.close-auth {
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

.close-auth:hover {
  color: #E9544E;
  transform: scale(1.1);
  background-color: rgba(233, 84, 78, 0.1);
}

.auth-content {
  text-align: center;
}

.auth-title {
  font-family: 'Courier New', Courier, monospace;
  font-size: 32px;
  color: #333;
  margin-bottom: 40px;
  font-weight: 700;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  width: 100%;
}

.auth-input {
  width: 100%;
  padding: 14px 18px;
  font-size: 16px;
  font-family: 'Courier New', Courier, monospace;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  transition: all 0.3s ease;
  outline: none;
}

.auth-input:focus {
  border-color: #E9544E;
  box-shadow: 0 0 0 3px rgba(233, 84, 78, 0.1);
}

.auth-submit {
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

.auth-submit:hover:not(:disabled) {
  background: #d43f39;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(233, 84, 78, 0.3);
}

.auth-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.forgot-password-link {
  text-align: right;
  margin-top: -10px;
  margin-bottom: 10px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  color: #E9544E;
  cursor: pointer;
  transition: all 0.3s ease;
}

.forgot-password-link:hover {
  color: #d43f39;
  text-decoration: underline;
}

.auth-switch {
  margin-top: 20px;
  font-family: 'Courier New', Courier, monospace;
  color: #666;
  font-size: 14px;
}

.auth-link {
  color: #E9544E;
  cursor: pointer;
  font-weight: 700;
  text-decoration: underline;
  transition: all 0.3s ease;
}

.auth-link:hover {
  color: #d43f39;
  transform: scale(1.05);
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
  .auth-modal {
    padding: 30px 25px;
    width: 95%;
  }
  
  .auth-title {
    font-size: 28px;
    margin-bottom: 30px;
  }
  
  .auth-input {
    padding: 12px 16px;
    font-size: 14px;
  }
  
  .auth-submit {
    padding: 12px 24px;
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .auth-modal {
    padding: 25px 20px;
  }
  
  .auth-title {
    font-size: 24px;
    margin-bottom: 25px;
  }
  
  .auth-input {
    padding: 10px 14px;
    font-size: 13px;
  }
  
  .auth-submit {
    padding: 10px 20px;
    font-size: 14px;
  }
}
</style>