import { createApp } from 'vue'

import { createPinia } from 'pinia'
import { socket_manager } from './config/socket'

import App from './App.vue'
import router from './router'
import './main.css'

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.mount('#app')

socket_manager.connect()