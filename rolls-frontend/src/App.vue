// src/App.vue
<script setup lang="ts">
import { ref, onUnmounted, watch, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import ResetPasswordModal from './components/modals/ResetPasswordModal.vue'
import ConfirmModal from './components/modals/ConfirmModal.vue'

import Header from './components/layout/Header.vue'
import MenuOverlay from './components/layout/MenuOverlay.vue'
import CustomCursor from './components/common/CustomCursor.vue'
import AuthModal from './components/modals/AuthModal.vue'
import ForgotPasswordModal from './components/modals/ForgotPasswordModal.vue'
import ProfileModal from './components/modals/ProfileModal.vue'
import CartModal from './components/modals/CartModal.vue'
import SearchModal from './components/modals/SearchModal.vue'
import FilterModal from './components/modals/FilterModal.vue'
import CategorySection from './components/merchandise/CategorySection.vue'

import { api, type Category } from './services/api'

const route = useRoute()
const isAdminPage = computed(() => route.path === '/admin')

const confirmModalRef = ref<InstanceType<typeof ConfirmModal> | null>(null)

// Функции для красивых уведомлений
const showAlert = (message: string, title: string = 'Внимание') => {
  return confirmModalRef.value?.alert(message, title)
}

const showConfirm = (message: string, title: string = 'Подтверждение') => {
  return confirmModalRef.value?.confirm({
    title,
    message,
    type: 'warning',
    confirmText: 'Да',
    cancelText: 'Нет',
    showCancel: true
  })
}

const showError = (message: string, title: string = 'Ошибка') => {
  return confirmModalRef.value?.error(message, title)
}

const showSuccess = (message: string, title: string = 'Успех') => {
  return confirmModalRef.value?.success(message, title)
}

const isMenuOpen             = ref(false)
const cursorX                = ref(0)
const cursorY                = ref(0)
const isOnDarkOverlay        = ref(false)
const showAuthPage           = ref(false)
const showProfilePage        = ref(false)
const showCartPage           = ref(false)
const showForgotPasswordPage = ref(false)
const showSearchPage         = ref(false)
const showFilterPage         = ref(false)
const authMode               = ref<'login' | 'register'>('login')
const currentUser            = ref<any>(null)
const isLoadingAuth          = ref(false)

const loginForm           = ref({ email: '', password: '' })
const registerForm        = ref({ name: '', email: '', phone: '', address: '', password: '', confirmPassword: '' })
const forgotPasswordEmail = ref('')
const searchQuery         = ref('')

const showResetPasswordModal = ref(false)
const resetToken = ref('')
const isResettingPassword = ref(false)

const editProfileForm = ref({
  name: '',
  phone: '',
  email: '',
  address: ''
})
const isEditingProfile = ref(false)
const isLoadingProfile = ref(false)

const availableIngredients = [
  'Лосось', 'Угорь', 'Креветка', 'Огурец', 'Авокадо', 'Рис', 'Нори', 
  'Сыр', 'Икра', 'Тунец', 'Курица', 'Мидии', 'Тофу', 'Краб', 
  'Сливочный сыр', 'Красный лук', 'Каперсы', 'Пепперони', 'Моцарелла',
  'Базилик', 'Говядина', 'Лапша удон', 'Лапша соба', 'Рисовая лапша',
  'Спайси соус', 'Унаги', 'Темпура', 'Салат айсберг', 'Пармезан',
  'Соус цезарь', 'Соус терияки', 'Соус хойсин', 'Соевый соус',
  'Васаби', 'Имбирь', 'Тобико'
]
const selectedIngredients  = ref<string[]>([])

const categories = ref<Category[]>([])
const filteredCategories = ref<Category[]>([])
const filteredAnchorCategories = ref<{ id: string; name: string }[]>([])
const isLoading  = ref(true)
const error      = ref<string | null>(null)

interface CartItem { merchandiseId: number; variationId: number; quantity: number; merchandise: any; variation: any }
const cartItems = ref<CartItem[]>([])
const cartTotal = ref(0)
const isCreatingOrder = ref(false)

const cartQuantities = computed(() => {
  const map: Record<string, number> = {}
  for (const item of cartItems.value) map[`${item.merchandiseId}_${item.variationId}`] = item.quantity
  return map
})

const anchorCategories = ref<{ id: string; name: string }[]>([])
const activeCategory   = ref<string>('')

const isDragging     = ref(false)
const dragStartX     = ref(0)
const dragScrollLeft = ref(0)

const HEADER_H = 80
const ANCHOR_H = 76

const mainContainer = ref<HTMLElement | null>(null)

// Проверка наличия активных фильтров
const hasActiveFilters = computed(() => {
  return searchQuery.value.trim() !== '' || selectedIngredients.value.length > 0
})

const checkResetPasswordToken = () => {
  const urlParams = new URLSearchParams(window.location.search)
  const token = urlParams.get('token')
  
  if (token) {
    resetToken.value = token
    showResetPasswordModal.value = true
    window.history.replaceState({}, document.title, window.location.pathname)
  }
}

const handleResetPassword = async (token: string, newPassword: string) => {
  isResettingPassword.value = true
  
  try {
    await api.resetPassword(token, newPassword)
    await showSuccess('Пароль успешно изменён! Теперь вы можете войти с новым паролем.', 'Успех')
    showResetPasswordModal.value = false
    resetToken.value = ''
    openAuthPage()
  } catch (error: any) {
    console.error('Ошибка сброса пароля:', error)
    await showError(error.response?.data?.detail || 'Ошибка при сбросе пароля. Возможно, ссылка устарела или недействительна.', 'Ошибка')
  } finally {
    isResettingPassword.value = false
  }
}

const showDeliveryAddressModal = ref(false)
const deliveryAddress = ref('')
const tempOrderItems = ref<CartItem[]>([])

const matchesSearch = (merchandise: any): boolean => {
  if (!searchQuery.value.trim()) return true
  const query = searchQuery.value.toLowerCase().trim()
  return merchandise.name.toLowerCase().includes(query)
}

const matchesIngredients = (merchandise: any): boolean => {
  if (selectedIngredients.value.length === 0) return true
  
  const textToSearch = `${merchandise.name} ${merchandise.description || ''}`.toLowerCase()
  
  return selectedIngredients.value.every(ingredient => 
    textToSearch.includes(ingredient.toLowerCase())
  )
}

const applyFilters = () => {
  filteredCategories.value = categories.value
    .map(category => ({
      ...category,
      merchandises: category.merchandises.filter(merchandise => 
        matchesSearch(merchandise) && matchesIngredients(merchandise)
      )
    }))
    .filter(category => category.merchandises.length > 0)
  
  filteredAnchorCategories.value = filteredCategories.value.map(cat => ({ 
    id: cat.slug || `category-${cat.id}`, 
    name: (cat.name || '').toUpperCase() 
  }))
  
  if (filteredAnchorCategories.value.length > 0) {
    const stillExists = filteredAnchorCategories.value.some(cat => cat.id === activeCategory.value)
    if (!stillExists) {
      activeCategory.value = filteredAnchorCategories.value[0].id
    }
  } else {
    activeCategory.value = ''
  }
  
  closeFilterPage()
  closeSearchPage()
}

const resetAllFilters = () => {
  searchQuery.value = ''
  selectedIngredients.value = []
  filteredCategories.value = categories.value
  filteredAnchorCategories.value = anchorCategories.value
  if (anchorCategories.value.length) {
    activeCategory.value = anchorCategories.value[0].id
  }
  closeFilterPage()
  closeSearchPage()
}

const saveSession = (u: any) => {
  if (u) {
    localStorage.setItem('currentUser', JSON.stringify(u))
  } else {
    localStorage.removeItem('currentUser')
  }
}

const loadSession = async () => {
  try {
    const user = await api.getCurrentUser()
    currentUser.value = { 
      name: user.name, 
      email: user.email, 
      phone: user.phone_number, 
      address: user.address,
      registeredAt: new Date(user.created_at).toLocaleDateString('ru-RU') 
    }
    saveSession(currentUser.value)
  } catch (error: any) {
    console.log('Пользователь не авторизован')
    if (error.response?.status === 401) {
      clearSession()
    }
    currentUser.value = null
  }
}

const clearSession = () => {
  localStorage.removeItem('currentUser')
  currentUser.value = null
}

const handleLogin = async () => {
  if (!loginForm.value.email || !loginForm.value.password) {
    await showAlert('Пожалуйста, заполните все поля', 'Внимание')
    return
  }
  
  isLoadingAuth.value = true
  
  try {
    await api.login(loginForm.value.email, loginForm.value.password)
    
    const user = await api.getCurrentUser()
    
    currentUser.value = { 
      name: user.name, 
      email: user.email, 
      phone: user.phone_number, 
      address: user.address,
      registeredAt: new Date(user.created_at).toLocaleDateString('ru-RU') 
    }
    saveSession(currentUser.value)
    closeAuthPage()
    showProfilePage.value = true
    await showSuccess('Вход выполнен успешно!', 'Добро пожаловать')
  } catch (error: any) {
    console.error('Ошибка входа:', error)
    await showError(error.response?.data?.detail || 'Ошибка входа. Проверьте email и пароль.', 'Ошибка входа')
  } finally {
    isLoadingAuth.value = false
  }
}

const handleRegister = async () => {
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    await showAlert('Пароли не совпадают', 'Ошибка')
    return
  }
  if (registerForm.value.password.length < 6) {
    await showAlert('Пароль должен содержать минимум 6 символов', 'Ошибка')
    return
  }
  
  isLoadingAuth.value = true
  
  try {
    await api.register({
      name: registerForm.value.name,
      email: registerForm.value.email,
      phone_number: registerForm.value.phone,
      address: registerForm.value.address,
      password: registerForm.value.password
    })
    await showSuccess('Регистрация успешна! Пожалуйста, подтвердите email. Письмо отправлено на вашу почту.', 'Регистрация')
    authMode.value = 'login'
    registerForm.value = { name: '', email: '', phone: '', address: '', password: '', confirmPassword: '' }
  } catch (error: any) {
    await showError(error.response?.data?.detail || 'Ошибка регистрации', 'Ошибка')
  } finally {
    isLoadingAuth.value = false
  }
}

const handleUpdateProfile = async () => {
  if (!editProfileForm.value.name && !editProfileForm.value.phone && !editProfileForm.value.address) {
    await showAlert('Заполните хотя бы одно поле для обновления', 'Внимание')
    return
  }
  
  isLoadingProfile.value = true
  
  try {
    const updateData: { name?: string; phone_number?: string; address?: string } = {}
    
    if (editProfileForm.value.name && editProfileForm.value.name !== currentUser.value?.name) {
      updateData.name = editProfileForm.value.name
    }
    
    if (editProfileForm.value.phone && editProfileForm.value.phone !== currentUser.value?.phone) {
      updateData.phone_number = editProfileForm.value.phone
    }
    
    if (editProfileForm.value.address && editProfileForm.value.address !== currentUser.value?.address) {
      updateData.address = editProfileForm.value.address
    }
    
    if (Object.keys(updateData).length === 0) {
      await showAlert('Нет изменений для сохранения', 'Внимание')
      return
    }
    
    const updatedUser = await api.updateMe(updateData)
    
    currentUser.value = {
      ...currentUser.value,
      name: updatedUser.name,
      phone: updatedUser.phone_number,
      email: updatedUser.email,
      address: updatedUser.address,
      registeredAt: new Date(updatedUser.created_at).toLocaleDateString('ru-RU')
    }
    
    saveSession(currentUser.value)
    await showSuccess('Профиль успешно обновлен!', 'Успех')
    isEditingProfile.value = false
    editProfileForm.value = { name: '', phone: '', email: '', address: '' }
  } catch (error: any) {
    console.error('Ошибка обновления профиля:', error)
    await showError(error.response?.data?.detail || 'Ошибка при обновлении профиля', 'Ошибка')
  } finally {
    isLoadingProfile.value = false
  }
}

const startEditProfile = () => {
  if (currentUser.value) {
    editProfileForm.value = {
      name: currentUser.value.name,
      phone: currentUser.value.phone,
      email: currentUser.value.email,
      address: currentUser.value.address || ''
    }
    isEditingProfile.value = true
  }
}

const handleForgotPassword = async () => {
  if (!forgotPasswordEmail.value) {
    await showAlert('Пожалуйста, введите email', 'Внимание')
    return
  }
  
  try {
    await api.requestPasswordReset(forgotPasswordEmail.value)
    await showSuccess(`Инструкции отправлены на ${forgotPasswordEmail.value}`, 'Проверьте почту')
    closeForgotPassword()
  } catch (error: any) {
    await showError(error.response?.data?.detail || 'Ошибка отправки письма', 'Ошибка')
  }
}

const logout = async () => {
  const confirmed = await showConfirm('Вы уверены, что хотите выйти из аккаунта?', 'Выход')
  if (!confirmed) return
  
  try {
    await api.logout()
  } catch (error) {
    console.error('Ошибка при выходе:', error)
  } finally {
    clearSession()
    showProfilePage.value = false
    cartItems.value = []
    cartTotal.value = 0
    await showSuccess('Вы вышли из аккаунта', 'До свидания')
  }
}

const toggleMenu         = () => { isMenuOpen.value = !isMenuOpen.value }
const closeMenu          = () => { isMenuOpen.value = false }
const openAuthPage       = () => { showAuthPage.value = true; closeMenu() }
const closeAuthPage      = () => {
  showAuthPage.value = false
  showForgotPasswordPage.value = false
  authMode.value = 'login'
  loginForm.value = { email: '', password: '' }
  registerForm.value = { name: '', email: '', phone: '', address: '', password: '', confirmPassword: '' }
  forgotPasswordEmail.value = ''
}
const openProfile        = () => { 
  if (currentUser.value) {
    showProfilePage.value = true
    isEditingProfile.value = false
    editProfileForm.value = { name: '', phone: '', email: '', address: '' }
  } else {
    openAuthPage()
  }
  closeMenu()
}
const closeProfilePage   = () => { 
  showProfilePage.value = false
  isEditingProfile.value = false
}
const openCart           = () => { showCartPage.value = true; closeMenu() }
const closeCartPage      = () => { showCartPage.value = false }
const openSearch         = () => { showSearchPage.value = true; closeMenu() }
const closeSearchPage    = () => { showSearchPage.value = false }
const openFilter         = () => { showFilterPage.value = true; closeMenu() }
const closeFilterPage    = () => { showFilterPage.value = false }
const openForgotPassword  = () => { showForgotPasswordPage.value = true }
const closeForgotPassword = () => { showForgotPasswordPage.value = false; forgotPasswordEmail.value = '' }
const switchToLogin      = () => { authMode.value = 'login' }
const switchToRegister   = () => { authMode.value = 'register' }

const toggleIngredient = (i: string) => {
  const idx = selectedIngredients.value.indexOf(i)
  idx === -1 ? selectedIngredients.value.push(i) : selectedIngredients.value.splice(idx, 1)
}
const resetFilters = () => { selectedIngredients.value = [] }

const addToCart = (merchandiseId: number, variationId: number, quantityChange: number) => {
  const existing = cartItems.value.find(i => i.merchandiseId === merchandiseId && i.variationId === variationId)
  if (existing) {
    existing.quantity += quantityChange
    if (existing.quantity <= 0)
      cartItems.value = cartItems.value.filter(i => !(i.merchandiseId === merchandiseId && i.variationId === variationId))
  } else if (quantityChange > 0) {
    for (const cat of categories.value) {
      const merch = cat.merchandises.find(m => m.id === merchandiseId)
      if (merch) {
        const v = merch.variations.find(v => v.id === variationId)
        if (v) { cartItems.value.push({ merchandiseId, variationId, quantity: quantityChange, merchandise: merch, variation: v }); break }
      }
    }
  }
  cartTotal.value = cartItems.value.reduce((s, i) => s + (i.variation?.price || 0) * i.quantity, 0)
}

const removeFromCart = (merchandiseId: number, variationId: number) => {
  cartItems.value = cartItems.value.filter(i => !(i.merchandiseId === merchandiseId && i.variationId === variationId))
  cartTotal.value = cartItems.value.reduce((s, i) => s + (i.variation?.price || 0) * i.quantity, 0)
}

const checkout = async () => {
  if (!currentUser.value) {
    await showAlert('Пожалуйста, войдите в аккаунт для оформления заказа', 'Требуется авторизация')
    openAuthPage()
    return
  }
  
  if (cartItems.value.length === 0) {
    await showAlert('Корзина пуста', 'Внимание')
    return
  }
  
  deliveryAddress.value = currentUser.value.address || ''
  tempOrderItems.value = [...cartItems.value]
  showDeliveryAddressModal.value = true
}

const confirmOrderWithAddress = async () => {
  if (!deliveryAddress.value.trim()) {
    await showAlert('Пожалуйста, укажите адрес доставки', 'Адрес не указан')
    return
  }
  
  isCreatingOrder.value = true
  showDeliveryAddressModal.value = false
  
  try {
    if (deliveryAddress.value !== currentUser.value?.address) {
      await api.updateMe({ address: deliveryAddress.value })
      currentUser.value.address = deliveryAddress.value
      saveSession(currentUser.value)
    }
    
    const orderItems = tempOrderItems.value.map(item => ({
      variation_id: item.variationId,
      quantity: item.quantity
    }))
    
    const order = await api.createOrder(orderItems)
    
    await showSuccess(
      `Заказ успешно оформлен! Доставка по адресу: ${deliveryAddress.value}. Статус: ${order.status === 'PENDING' ? 'В обработке' : 'Завершен'}`,
      'Заказ оформлен'
    )
    
    cartItems.value = []
    cartTotal.value = 0
    closeCartPage()
  } catch (error: any) {
    console.error('Ошибка при оформлении заказа:', error)
    await showError(error.response?.data?.detail || 'Ошибка при оформлении заказа', 'Ошибка')
  } finally {
    isCreatingOrder.value = false
    tempOrderItems.value = []
  }
}

const scrollToCategory = (categoryId: string) => {
  activeCategory.value = categoryId
  const el = document.getElementById(categoryId)
  if (!el || !mainContainer.value) return
  
  const containerRect = mainContainer.value.getBoundingClientRect()
  const elementRect = el.getBoundingClientRect()
  const scrollTop = mainContainer.value.scrollTop + elementRect.top - containerRect.top - ANCHOR_H - 150
  
  mainContainer.value.scrollTo({ top: scrollTop, behavior: 'smooth' })
}

const handleScroll = () => {
  if (!mainContainer.value) return
  
  let current = filteredAnchorCategories.value[0]?.id || ''
  const anchorBottom = HEADER_H + ANCHOR_H
  
  for (const cat of filteredAnchorCategories.value) {
    const el = document.getElementById(cat.id)
    if (el) {
      const rect = el.getBoundingClientRect()
      if (rect.top <= anchorBottom + 50 && rect.top >= anchorBottom - 200) {
        current = cat.id
        break
      }
    }
  }
  
  if (current !== activeCategory.value) {
    activeCategory.value = current
  }
}

const startAnchorDrag = (e: MouseEvent) => {
  isDragging.value = true
  const c = e.currentTarget as HTMLElement
  dragStartX.value = e.pageX - c.offsetLeft
  dragScrollLeft.value = c.scrollLeft
  c.style.cursor = 'grabbing'
  c.style.userSelect = 'none'
}
const stopAnchorDrag = (e: MouseEvent) => {
  isDragging.value = false
  const c = e.currentTarget as HTMLElement
  c.style.cursor = 'grab'
  c.style.userSelect = ''
}
const onAnchorDrag = (e: MouseEvent) => {
  if (!isDragging.value) return
  e.preventDefault()
  const c = e.currentTarget as HTMLElement
  c.scrollLeft = dragScrollLeft.value - (e.pageX - c.offsetLeft - dragStartX.value) * 1.5
}
const handleAnchorWheel = (e: WheelEvent) => {
  (e.currentTarget as HTMLElement).scrollLeft += e.deltaY
  e.preventDefault()
}

const handleMouseMove = (e: MouseEvent) => {
  cursorX.value = e.clientX
  cursorY.value = e.clientY
  let onDark = false
  
  const target = e.target as HTMLElement
  
  if (target) {
    const isOnContent = 
      target.closest('.info-modal') ||
      target.closest('.auth-modal') ||
      target.closest('.search-modal') ||
      target.closest('.filter-modal') ||
      target.closest('.forgot-password-modal-content') ||
      target.closest('.side-menu') ||
      target.closest('.cart-modal') ||
      target.closest('.profile-modal') ||
      target.closest('.cart-overlay .cart-items') ||
      target.closest('.profile-overlay .profile-info')
    
    if (isOnContent) {
      onDark = false
    }
    else {
      const isOnOverlay = 
        target.closest('.dark-overlay') ||
        target.closest('.info-modal-overlay') ||
        target.closest('.auth-overlay') ||
        target.closest('.search-modal-overlay') ||
        target.closest('.filter-modal-overlay') ||
        target.closest('.forgot-password-modal') ||
        target.closest('.cart-overlay') ||
        target.closest('.profile-overlay')
      
      if (isOnOverlay) {
        onDark = true
      }
    }
    
    if (onDark && target.closest('.dark-overlay')) {
      const pct = window.innerWidth <= 480 ? 85 : window.innerWidth <= 768 ? 70 : 25
      const isOnRightSide = e.clientX > window.innerWidth * pct / 100
      onDark = isOnRightSide
    }
  }
  
  if (onDark !== isOnDarkOverlay.value) {
    isOnDarkOverlay.value = onDark
    document.body.style.cursor = onDark ? 'none' : ''
  }
}

const scrollToTop = () => {
  if (mainContainer.value) {
    mainContainer.value.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const scrollToMenu = () => {
  if (mainContainer.value) {
    const menuSection = document.querySelector('.menu-title-section')
    if (menuSection) {
      const rect = menuSection.getBoundingClientRect()
      const containerRect = mainContainer.value.getBoundingClientRect()
      const scrollTop = mainContainer.value.scrollTop + rect.top - containerRect.top - HEADER_H - 20
      mainContainer.value.scrollTo({ top: scrollTop, behavior: 'smooth' })
    }
  }
}

watch([isMenuOpen, showAuthPage, showForgotPasswordPage, showProfilePage, showCartPage, showSearchPage, showFilterPage], (vals) => {
  if (vals.some(Boolean)) {
    document.addEventListener('mousemove', handleMouseMove)
  } else {
    document.removeEventListener('mousemove', handleMouseMove)
    document.body.style.cursor = ''
    isOnDarkOverlay.value = false
  }
})

const loadData = async () => {
  isLoading.value = true
  error.value = null
  try {
    const data = await api.getMerchandise()
    categories.value = data
    filteredCategories.value = data
    anchorCategories.value = data.map(c => ({ id: c.slug || `category-${c.id}`, name: c.name.toUpperCase() }))
    filteredAnchorCategories.value = anchorCategories.value
    if (anchorCategories.value.length) activeCategory.value = anchorCategories.value[0].id
  } catch (err) {
    error.value = 'Не удалось загрузить товары. Проверьте соединение с сервером.'
    console.error(err)
    await showError('Не удалось загрузить товары. Проверьте соединение с сервером.', 'Ошибка загрузки')
  } finally {
    isLoading.value = false
  }
}

const handleSearch = () => {
  applyFilters()
}

onMounted(async () => {
  await loadSession()
  await loadData()
  checkResetPasswordToken()
  
  if (mainContainer.value && !isAdminPage.value) {
    mainContainer.value.addEventListener('scroll', handleScroll, { passive: true })
    handleScroll()
  }
})

onUnmounted(() => {
  if (mainContainer.value) {
    mainContainer.value.removeEventListener('scroll', handleScroll)
  }
  document.removeEventListener('mousemove', handleMouseMove)
  document.body.style.cursor = ''
})
</script>

<template>
  <!-- Если страница админки, показываем только router-view -->
  <div v-if="isAdminPage" class="admin-wrapper">
    <router-view />
  </div>
  
  <!-- Иначе показываем обычный сайт -->
  <div v-else>
    <!-- Фоновые круги -->
    <div class="bg-circles" aria-hidden="true">
      <div class="circle c1"></div>
      <div class="circle c2"></div>
      <div class="circle c3"></div>
      <div class="circle c4"></div>
      <div class="circle c5"></div>
    </div>

    <!-- Хедер — фиксирован -->
    <Header :isMenuOpen="isMenuOpen" @toggleMenu="toggleMenu" @openCart="openCart" @openProfile="openProfile" />

    <!-- Основной скроллящийся контейнер -->
    <div ref="mainContainer" class="main-scroll-container">
      <!-- Основной контент -->
      <div class="page-flow">
        <!-- Герой секция -->
        <div class="hero-section">
          <div class="title-container">
            <img src="/src/public/ram.png" alt="" class="frame-image" />
            <div class="blur-circle"></div>
            <img src="/src/public/hap.png" alt="" class="hap-image" />
            <h1>Суши<br>Лавка</h1>
            <div class="sushi-tagline">пожалуй,<br>самые большие<br>роллы</div>
          </div>
        </div>

        <!-- Заголовок МЕНЮ -->
        <div class="menu-title-section">
          <h2 class="menu-title">МЕНЮ</h2>
        </div>

        <!-- Якорная панель — sticky -->
        <div class="anchor-bar">
          <div class="anchor-bar__inner">
            <div class="anchor-icons">
              <!-- Кнопка сброса фильтров (появляется только когда есть активные фильтры) -->
              <div v-if="hasActiveFilters" class="reset-filters-btn" @click="resetAllFilters">
                <img src="/src/public/krest.png" alt="Сбросить" class="reset-icon" />
              </div>
              
              <img
                :src="selectedIngredients.length ? '/src/public/settings1.png' : '/src/public/settings.png'"
                alt="Фильтр"
                class="anchor-icon"
                @click="openFilter"
              />
              <img
                :src="searchQuery ? '/src/public/search1.png' : '/src/public/search.png'"
                alt="Поиск"
                class="anchor-icon"
                @click="openSearch"
              />
            </div>
            <div class="vertical-divider"></div>
            <div class="anchor-buttons-wrapper">
              <div
                class="anchor-buttons-container"
                @mousedown="startAnchorDrag"
                @mouseup="stopAnchorDrag"
                @mouseleave="stopAnchorDrag"
                @mousemove="onAnchorDrag"
                @wheel.prevent="handleAnchorWheel"
              >
                <button
                  v-for="cat in filteredAnchorCategories"
                  :key="cat.id"
                  class="anchor-button"
                  :class="{ active: activeCategory === cat.id }"
                  @click="scrollToCategory(cat.id)"
                >
                  {{ cat.name }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Каталог -->
        <div class="catalog-scroll">
          <div class="catalog-inner">
            <div v-if="isLoading" class="state-loading">
              <div class="spinner"></div>
              <p>Загрузка меню…</p>
            </div>
            <div v-else-if="error && filteredCategories.length === 0" class="state-error">
              <p>{{ error }}</p>
              <button class="retry-btn" @click="loadData">Повторить</button>
            </div>
            <div v-else-if="filteredCategories.length === 0 && (searchQuery || selectedIngredients.length)" class="state-no-results">
              <p>😔 Ничего не найдено</p>
              <button class="retry-btn" @click="resetAllFilters">Сбросить фильтры</button>
            </div>
            <template v-else>
              <CategorySection
                v-for="cat in filteredCategories"
                :key="cat.id"
                :category="cat"
                :cartQuantities="cartQuantities"
                @addToCart="addToCart"
              />
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- Меню и модалки -->
    <MenuOverlay
      :isOpen="isMenuOpen"
      :isLoggedIn="!!currentUser"
      @close="closeMenu"
      @login="openAuthPage"
      @profile="openProfile"
      @scrollToTop="scrollToTop"
      @scrollToMenu="scrollToMenu"
      @cursorChange="(visible) => { isOnDarkOverlay = visible; document.body.style.cursor = visible ? 'none' : '' }"
    />
    
    <ResetPasswordModal
      :isOpen="showResetPasswordModal"
      :token="resetToken"
      :isLoading="isResettingPassword"
      @close="showResetPasswordModal = false"
      @reset="handleResetPassword"
    />

    <AuthModal
      :isOpen="showAuthPage && !showForgotPasswordPage"
      :mode="authMode"
      :loginForm="loginForm"
      :registerForm="registerForm"
      :isLoading="isLoadingAuth"
      @close="closeAuthPage"
      @login="handleLogin"
      @register="handleRegister"
      @forgotPassword="openForgotPassword"
      @switchToLogin="switchToLogin"
      @switchToRegister="switchToRegister"
      @update:loginForm="f => loginForm = f"
      @update:registerForm="f => registerForm = f"
    />
    
    <ForgotPasswordModal
      :isOpen="showForgotPasswordPage"
      :email="forgotPasswordEmail"
      @close="closeForgotPassword"
      @submit="handleForgotPassword"
      @update:email="e => forgotPasswordEmail = e"
    />
    
    <ProfileModal
      :isOpen="showProfilePage"
      :user="currentUser"
      :editForm="editProfileForm"
      :isEditing="isEditingProfile"
      :isLoading="isLoadingProfile"
      :orders="[]"
      @close="closeProfilePage"
      @logout="logout"
      @startEdit="startEditProfile"
      @updateProfile="handleUpdateProfile"
      @cancelEdit="isEditingProfile = false; editProfileForm = { name: '', phone: '', email: '', address: '' }"
    />
    
    <CartModal
      :isOpen="showCartPage"
      :cartItems="cartItems.map(i => ({ merchandiseId: i.merchandiseId, variationId: i.variationId, quantity: i.quantity }))"
      :categories="categories"
      :isLoading="isCreatingOrder"
      @close="closeCartPage"
      @checkout="checkout"
      @increment="(mId, vId) => addToCart(mId, vId, 1)"
      @decrement="(mId, vId) => addToCart(mId, vId, -1)"
      @remove="removeFromCart"
    />
    
    <SearchModal
      :isOpen="showSearchPage"
      :query="searchQuery"
      @close="closeSearchPage"
      @search="handleSearch"
      @update:query="q => searchQuery = q"
    />
    
    <FilterModal
      :isOpen="showFilterPage"
      :ingredients="availableIngredients"
      :selectedIngredients="selectedIngredients"
      @close="closeFilterPage"
      @apply="applyFilters"
      @reset="resetFilters"
      @toggleIngredient="toggleIngredient"
    />
    
    <!-- Модальное окно для адреса доставки -->
    <div v-if="showDeliveryAddressModal" class="delivery-address-overlay" @click.self="showDeliveryAddressModal = false">
      <div class="delivery-address-modal">
        <div class="delivery-address-header">
          <h2>Адрес доставки</h2>
          <button class="close-delivery" @click="showDeliveryAddressModal = false">×</button>
        </div>
        
        <div class="delivery-address-content">
          <div class="delivery-address-info">
            <p class="delivery-label">Укажите адрес, куда доставить заказ:</p>
            <textarea
              v-model="deliveryAddress"
              class="delivery-address-input"
              placeholder="Город, улица, дом, квартира/офис"
              rows="3"
            ></textarea>
            <p class="delivery-hint">* Адрес будет сохранен в вашем профиле для следующих заказов</p>
          </div>
          
          <div class="delivery-address-actions">
            <button class="cancel-delivery-btn" @click="showDeliveryAddressModal = false">Отмена</button>
            <button class="confirm-delivery-btn" @click="confirmOrderWithAddress" :disabled="isCreatingOrder">
              {{ isCreatingOrder ? 'Оформление...' : 'Подтвердить заказ' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <ConfirmModal ref="confirmModalRef" />
    <CustomCursor :visible="isOnDarkOverlay" :x="cursorX" :y="cursorY" />
  </div>
</template>

<style>
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  overflow: hidden;
  font-family: Arial, sans-serif;
  background: #fff;
}

#app {
  height: 100%;
  overflow: hidden;
}

.admin-wrapper {
  height: 100%;
  overflow: auto;
}

.main-scroll-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  z-index: 1;
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
  opacity: 0.6;
}

.c1 {
  width: 400px;
  height: 400px;
  background: #E9544E;
  top: -100px;
  left: -100px;
}

.c2 {
  width: 500px;
  height: 500px;
  background: #FFBF9C;
  bottom: -150px;
  right: -150px;
}

.c3 {
  width: 300px;
  height: 300px;
  background: #FFBF9C;
  top: 50%;
  left: 20%;
}

.c4 {
  width: 350px;
  height: 350px;
  background: #ff8c94;
  top: 20%;
  right: 10%;
}

.c5 {
  width: 250px;
  height: 250px;
  background: #ff8c94;
  bottom: 30%;
  left: 10%;
}

.page-flow {
  position: relative;
  z-index: 1;
  padding-top: 80px;
}

.hero-section {
  height: calc(100vh - 80px - 76px);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: visible;
  position: relative;
}

.title-container {
  position: relative;
  display: inline-block;
  text-align: center;
  min-height: 380px;
}

.frame-image {
  position: absolute;
  top: -150px;
  left: 50%;
  transform: translateX(-50%);
  width: auto;
  height: auto;
  max-width: 1500px;
  z-index: 1;
  pointer-events: none;
}

.blur-circle {
  position: absolute;
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
  width: 550px;
  height: 550px;
  background: #FFBF9C;
  border-radius: 50%;
  filter: blur(50px);
  opacity: 0.9;
  z-index: 2;
  pointer-events: none;
}

.hap-image {
  position: absolute;
  top: 90%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: auto;
  height: auto;
  max-width: 600px;
  z-index: 3;
  pointer-events: none;
}

h1 {
  font-family: 'ChinaCyr', 'Arial', sans-serif;
  color: #333;
  font-size: 96px;
  line-height: 0.9;
  letter-spacing: 2px;
  font-weight: normal;
  text-align: center;
  position: relative;
  z-index: 4;
  margin-top: -100px;
  margin-bottom: 30px;
}

.sushi-tagline {
  position: absolute;
  bottom: 230px;
  right: -155px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 20px;
  font-weight: 900;
  color: #E9544E;
  text-align: left;
  line-height: 1.3;
  white-space: nowrap;
  z-index: 4;
}

.menu-title-section {
  padding: 60px 20px 40px;
  text-align: center;
  background: transparent;
}

.menu-title {
  font-family: 'ChinaCyr', 'Arial', sans-serif;
  font-size: 72px;
  color: #333;
  letter-spacing: 4px;
  font-weight: normal;
  position: relative;
  display: inline-block;
}

.menu-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: #E9544E;
  border-radius: 2px;
}

.anchor-bar {
  position: sticky;
  top: 80px;
  height: 76px;
  z-index: 90;
  display: flex;
  align-items: center;
}

.anchor-bar__inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  width: 100%;
}

.anchor-icons {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-shrink: 0;
}

.anchor-icon {
  width: 40px;
  height: 40px;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.anchor-icon:hover {
  transform: scale(1.1);
  opacity: 0.8;
}

/* Кнопка сброса фильтров */
.reset-filters-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
  animation: fadeInScale 0.3s ease;
}

.reset-filters-btn:hover {
  transform: rotate(90deg) scale(1.1);
}

.reset-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.vertical-divider {
  width: 2px;
  height: 40px;
  background: #E9544E;
  flex-shrink: 0;
  border-radius: 2px;
}

.anchor-buttons-wrapper {
  flex: 1;
  overflow: hidden;
}

.anchor-buttons-container {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;
  -ms-overflow-style: none;
  cursor: grab;
  padding: 5px 0;
  white-space: nowrap;
}

.anchor-buttons-container::-webkit-scrollbar {
  display: none;
}

.anchor-buttons-container:active {
  cursor: grabbing;
}

.anchor-button {
  background: rgba(255, 255, 255);
  border: 1.5px solid rgba(0, 0, 0, 0.15);
  padding: 10px 20px;
  border-radius: 30px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: border-color 0.5s ease, background 0.5s ease, transform 0.2s, box-shadow 0.2s, color 0.5s ease;
}

.anchor-button:hover {
  border-color: #E9544E;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(233, 84, 78, 0.2);
}

.anchor-button.active {
  border-color: #E9544E;
  background: white;
  color: #E9544E;
}

.catalog-scroll {
  min-height: 100vh;
  position: relative;
  z-index: 2;
}

.catalog-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 120px;
}

.state-loading,
.state-error,
.state-no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 40vh;
  gap: 20px;
  font-family: 'Courier New', Courier, monospace;
  color: #666;
}

.state-error p,
.state-no-results p {
  color: #E9544E;
  font-size: 18px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 3px solid #e0e0e0;
  border-top-color: #E9544E;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.retry-btn {
  background: #E9544E;
  color: #fff;
  border: none;
  padding: 10px 28px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border-radius: 8px;
  cursor: pointer;
}

.retry-btn:hover {
  background: #d43f39;
  transform: scale(1.02);
}

.delivery-address-overlay {
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

.delivery-address-modal {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease;
  overflow: hidden;
}

.delivery-address-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 2px solid #f0f0f0;
}

.delivery-address-header h2 {
  font-family: 'Courier New', Courier, monospace;
  font-size: 24px;
  color: #333;
  margin: 0;
}

.close-delivery {
  background: none;
  border: none;
  font-size: 32px;
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

.close-delivery:hover {
  color: #E9544E;
  transform: scale(1.1);
  background-color: rgba(233, 84, 78, 0.1);
}

.delivery-address-content {
  padding: 24px;
}

.delivery-address-info {
  margin-bottom: 24px;
}

.delivery-label {
  font-family: 'Courier New', Courier, monospace;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.delivery-address-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;
  font-family: 'Courier New', Courier, monospace;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  resize: vertical;
  transition: all 0.3s ease;
}

.delivery-address-input:focus {
  outline: none;
  border-color: #E9544E;
  box-shadow: 0 0 0 3px rgba(233, 84, 78, 0.1);
}

.delivery-hint {
  font-family: 'Courier New', Courier, monospace;
  font-size: 12px;
  color: #999;
  margin-top: 8px;
  font-style: italic;
}

.delivery-address-actions {
  display: flex;
  gap: 12px;
}

.cancel-delivery-btn {
  flex: 1;
  padding: 12px 20px;
  font-size: 16px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f0f0f0;
  color: #666;
}

.cancel-delivery-btn:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.confirm-delivery-btn {
  flex: 1;
  padding: 12px 20px;
  font-size: 16px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #E9544E;
  color: white;
}

.confirm-delivery-btn:hover:not(:disabled) {
  background: #d43f39;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(233, 84, 78, 0.3);
}

.confirm-delivery-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

@media (max-width: 950px) {
  .sushi-tagline {
    position: static;
    margin-top: 14px;
    text-align: center;
    white-space: normal;
  }
  
  .title-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .menu-title {
    font-size: 56px;
  }
}

@media (max-width: 768px) {
  .frame-image {
    max-width: 600px;
  }
  
  .blur-circle {
    width: 350px;
    height: 350px;
    top: 120px;
  }
  
  .hap-image {
    max-width: 350px;
  }
  
  h1 {
    font-size: 72px;
  }
  
  .sushi-tagline {
    font-size: 16px;
  }
  
  .menu-title {
    font-size: 48px;
  }
  
  .menu-title-section {
    padding: 40px 20px 30px;
  }
  
  .anchor-icon {
    width: 32px;
    height: 32px;
  }
  
  .reset-filters-btn {
    width: 32px;
    height: 32px;
  }
  
  .vertical-divider {
    height: 32px;
  }
  
  .anchor-button {
    background: white;
    font-size: 12px;
    padding: 8px 16px;
  }
  
  .delivery-address-header h2 {
    font-size: 20px;
  }
  
  .delivery-address-input {
    font-size: 14px;
    padding: 10px 14px;
  }
  
  .cancel-delivery-btn,
  .confirm-delivery-btn {
    padding: 10px 16px;
    font-size: 14px;
  }
}

@media (max-width: 600px) {
  h1 {
    font-size: 60px;
  }
  
  .menu-title {
    font-size: 40px;
    letter-spacing: 2px;
  }
}

@media (max-width: 480px) {
  .frame-image {
    max-width: 350px;
    top: -50px;
  }
  
  .blur-circle {
    width: 220px;
    height: 220px;
    top: 80px;
  }
  
  .hap-image {
    max-width: 220px;
  }
  
  h1 {
    font-size: 48px;
  }
  
  .sushi-tagline {
    font-size: 12px;
  }
  
  .menu-title {
    font-size: 32px;
    letter-spacing: 2px;
  }
  
  .menu-title-section {
    padding: 30px 20px 20px;
  }
  
  .menu-title::after {
    width: 50px;
    height: 2px;
    bottom: -6px;
  }
  
  .anchor-icon {
    width: 28px;
    height: 28px;
  }
  
  .reset-filters-btn {
    width: 28px;
    height: 28px;
  }
  
  .vertical-divider {
    height: 28px;
  }
  
  .anchor-button {
    font-size: 10px;
    padding: 6px 12px;
  }
}
</style>