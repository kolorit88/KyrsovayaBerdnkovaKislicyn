<template>
  <div v-if="isOpen" class="menu-overlay">
    <div class="side-menu">
      <div class="menu-content">
        <button class="menu-login-btn" @click="onProfileClick">
          {{ isLoggedIn ? 'Мой аккаунт' : 'Войти' }}
        </button>
        
        <div class="menu-items">
          <div class="menu-item" @click="scrollToTop">Главная</div>
          <div class="menu-item" @click="scrollToMenu">Меню</div>
          <div class="menu-item" @click="openModal('promo')">Акции</div>
          <div class="menu-item" @click="openModal('about')">О нас</div>
          <div class="menu-item" @click="openModal('delivery')">Доставка</div>
          <div class="menu-item" @click="openModal('howto')">Как заказать</div>
          <div class="menu-item" @click="openModal('contacts')">Контакты</div>
        </div>
      </div>
    </div>
    
    <div class="dark-overlay" @click="$emit('close')"></div>
  </div>

  <!-- Модальное окно -->
<Teleport to="body">
  <div 
    v-if="activeModal" 
    class="info-modal-overlay"
    @click.self="closeModal"
  >
    <div class="info-modal" @click.stop>
      <div class="info-modal-header">
        <h2>{{ modalTitle }}</h2>
      </div>
      <div class="info-modal-content" v-html="modalContent"></div>
    </div>
  </div>
</Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  isOpen: boolean
  isLoggedIn: boolean
}>()

const emit = defineEmits<{
  close: []
  login: []
  profile: []
  scrollToTop: []
  scrollToMenu: []
}>()

const activeModal = ref<string | null>(null)

const modalTitle = ref('')
const modalContent = ref('')

const onProfileClick = () => {
  if (props.isLoggedIn) {
    emit('profile')
  } else {
    emit('login')
  }
  emit('close')
}

const scrollToTop = () => {
  emit('scrollToTop')
  emit('close')
}

const scrollToMenu = () => {
  emit('scrollToMenu')
  emit('close')
}

const openModal = (type: string) => {
  activeModal.value = type
  
  switch(type) {
    case 'promo':
      modalTitle.value = 'Акции'
      modalContent.value = `
        <div class="info-content">
          <div class="info-block">
            <p class="promo-item"><strong>Акция 1.</strong> Забери заказ сам в нашем магазине и получи скидку <strong>10%</strong></p>
            <p class="promo-item"><strong>Акция 2.</strong> Поздравляем с Днем Рождения и дарим скидку <strong>15%</strong><br>
            <em>Скидка действует в течении 5 дней после дня рождения, при предъявлении паспорта.</em></p>
          </div>
        </div>
      `
      break
    case 'about':
      modalTitle.value = 'О нас'
      modalContent.value = `
        <div class="info-content">
          <p class="greeting">Рады приветствовать Вас в нашем магазине японской кухни.</p>
          
          <div class="info-block">
            <p class="block-title"><strong>Почему Суши Лавка:</strong></p>
            <p><strong>1.</strong> МЫ используем только качественное и дорогое сырье!</p>
            <p><strong>2.</strong> МЫ разработали оптимальное соотношение ингредиентов!</p>
            <p><strong>3.</strong> МЫ предлагаем самые большие роллы в Кемерово!</p>
            <p><strong>4.</strong> Если вы посетите наш магазин японской кухни, повар приготовит заказ на ваших глазах!</p>
            <p><strong>5.</strong> МЫ - это молодая амбициозная команда, работающая для ВАС!</p>
          </div>
        </div>
      `
      break
    case 'delivery':
      modalTitle.value = 'Доставка'
      modalContent.value = `
        <div class="info-content">
          <div class="info-block">
            <p class="block-title"><strong>Расписание работы:</strong></p>
            <p><strong>пн. - вс.</strong> 10:00 - 22:00</p>
          </div>
          
          <div class="info-block">
            <p class="block-title"><strong>Условия бесплатной доставки:</strong></p>
            <p><em>Доставка производится бесплатно, если сумма Вашего заказа превышает минимальную сумму, а именно:</em></p>
            <p><strong>500₽</strong> - Ленинский, ФПК, Заводский до Кузнецкого, Центральный до Кузнецкого, Южный до 1 линии</p>
            <p><strong>600₽</strong> - Заводский за Кузнецкий, Центральный за Кузнецкий, Южный за 1 линию, Суховский, Металлплощадка, Рудничный</p>
            <p><strong>800₽</strong> - Лесная поляна</p>
            <p><strong>1000₽</strong> - Комиссарово, РТС, Кировский, Осиновка, Пригородный, Ягуновский, Боровой</p>
            <p><strong>1500₽</strong> - Ягуново, Андреевка, Новостройка, Березово, п.Пионер</p>
            <p><strong>2000₽</strong> - Кедровка, Промышленовский, Елыкаево, Мазурово, Ясногорский</p>
          </div>
          
          <div class="info-block">
            <p class="block-title"><strong>Оплата</strong></p>
            <p><strong>Наличная или безналичная оплата</strong> курьеру при получении заказа.</p>
            <p><em>Безналичная оплата заказов на доставку не принимается за полчаса до закрытия.</em></p>
            <p><strong>Заказы на сумму свыше 4000 рублей</strong> принимаются по предоплате 50%</p>
          </div>
          
          <div class="info-block">
            <p class="block-title"><strong>Как нас найти?</strong></p>
            <p><strong>Суши Лавка</strong><br>
            г. Кемерово, ул. Тухачевского, 22А</p>
          </div>
        </div>
      `
      break
    case 'howto':
      modalTitle.value = 'Как заказать'
      modalContent.value = `
        <div class="info-content">
          <p class="greeting">Совершить заказ можно тремя способами:</p>
          
          <div class="info-block">
            <p><strong>Способ 1.</strong> Позвонить по телефону <strong>67-16-06</strong> и сделать заказ.</p>
            <p><strong>Способ 2.</strong> Добавить необходимые вам товары в корзину сайта и в течении <strong>15 мин.</strong> с вами свяжется оператор.</p>
            <p><strong>Способ 3.</strong> Посетить наш магазин и купить продукцию с <strong>10% скидкой</strong>.</p>
          </div>
        </div>
      `
      break
    case 'contacts':
      modalTitle.value = 'Контакты'
      modalContent.value = `
        <div class="info-content">
          <div class="info-block">
            <p><strong>Телефон магазина:</strong><br>
            <span class="contact-phone">67-16-06</span></p>
            
            <p><strong>Сайт:</strong><br>
            <a href="http://сушилавка42.рф" target="_blank" class="contact-link">сушилавка42.рф</a></p>
            
            <p><strong>ВКонтакте:</strong><br>
            <a href="http://vk.com/club64910804" target="_blank" class="contact-link">vk.com/club64910804</a></p>
            
            <p><strong>Связь с директором:</strong><br>
            <span class="contact-phone">+7-904-570-9926</span></p>
          </div>
        </div>
      `
      break
  }
}

const closeModal = () => {
  activeModal.value = null
}
</script>

<style scoped>
.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2000;
  display: flex;
}

.side-menu {
  position: relative;
  width: 25%;
  height: 100%;
  background-color: white;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
  z-index: 2002;
  padding: 80px 20px 20px 20px;
  overflow-y: auto;
  cursor: auto;
}

.dark-overlay {
  position: relative;
  width: 75%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 2001;
  cursor: pointer;
}

.menu-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100%;
  gap: 0;
}

.menu-items {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
  width: 100%;
}

.menu-item {
  font-family: 'Courier New', Courier, monospace;
  font-size: 22px;
  font-weight: 700;
  color: #333;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 8px 20px;
  border-radius: 8px;
  width: 100%;
  max-width: 250px;
}

.menu-item:hover {
  color: #E9544E;
  transform: scale(1.05);
  background-color: rgba(233, 84, 78, 0.1);
}

.menu-login-btn {
  background: #E9544E;
  color: white;
  border: none;
  padding: 12px 30px;
  font-size: 22px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 250px;
  letter-spacing: 1px;
}

.menu-login-btn:hover {
  background: #d43f39;
  transform: scale(1.02);
  box-shadow: 0 3px 10px rgba(233, 84, 78, 0.3);
}

/* Стили для модального окна */
.info-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2100;
}

.info-modal {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 650px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  animation: slideIn 0.3s ease-out;
  cursor: default;
}

@keyframes slideIn {
  from {
    transform: translateY(-30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.info-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 16px 24px;
  border-bottom: 2px solid #f0f0f0;
}

.info-modal-header h2 {
  font-family: 'Courier New', Courier, monospace;
  color: #E9544E;
  font-size: 32px;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 40px;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
  line-height: 1;
}

.close-btn:hover {
  color: #E9544E;
}

.info-modal-content {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 16px;
  line-height: 1.8;
  color: #333;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-block {
  margin-bottom: 10px;
}

.info-block p {
  margin-bottom: 12px;
}

.greeting {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}

.block-title {
  font-size: 18px;
  margin-bottom: 15px;
  margin-top: 10px;
  border-left: 3px solid #E9544E;
  padding-left: 12px;
}

.promo-item {
  margin-bottom: 20px;
}

.promo-item strong {
  font-size: 17px;
}

.promo-item em {
  display: inline-block;
  margin-top: 5px;
  margin-left: 20px;
  font-size: 15px;
}

.contact-phone {
  font-size: 18px;
  font-weight: bold;
  color: #E9544E;
}

.contact-link {
  color: #E9544E;
  text-decoration: none;
  font-size: 16px;
  font-weight: bold;
  transition: color 0.2s;
  cursor: pointer;
}

.contact-link:hover {
  color: #d43f39;
  text-decoration: underline;
}

strong {
  color: #E9544E;
}

em {
  color: #666;
  font-style: italic;
}

@media (max-width: 768px) {
  .side-menu {
    width: 70%;
  }
  
  .dark-overlay {
    width: 30%;
  }
  
  .menu-item {
    font-size: 18px;
  }
  
  .menu-login-btn {
    font-size: 18px;
    padding: 10px 25px;
    max-width: 220px;
  }
  
  .menu-items {
    gap: 15px;
    margin-top: 35px;
  }
  
  .info-modal {
    width: 95%;
    max-height: 85vh;
  }
  
  .info-modal-header h2 {
    font-size: 26px;
  }
  
  .info-modal-content {
    font-size: 14px;
    padding: 20px;
  }
  
  .greeting,
  .block-title {
    font-size: 16px;
  }
  
  .contact-phone {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .side-menu {
    width: 85%;
  }
  
  .dark-overlay {
    width: 15%;
  }
  
  .menu-item {
    font-size: 16px;
  }
  
  .menu-login-btn {
    font-size: 16px;
    padding: 8px 20px;
    max-width: 200px;
  }
  
  .menu-items {
    gap: 12px;
    margin-top: 30px;
  }
  
  .info-modal-header h2 {
    font-size: 22px;
  }
  
  .info-modal-content {
    font-size: 13px;
    padding: 16px;
  }
  
  .greeting,
  .block-title {
    font-size: 15px;
  }
  
  .contact-phone {
    font-size: 15px;
  }
}
</style>