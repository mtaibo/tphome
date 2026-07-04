import { createApp } from 'vue'
import { createPinia } from 'pinia'

import { socket_manager } from './config/socket'

import App from './App.vue'
import router from './router'
import './main.css'

if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
    document.documentElement.classList.add('is-standalone')
}

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.mount('#app')

socket_manager.connect()
