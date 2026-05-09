import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { socket_manager } from './db/socket'
import './main.css'
import App from './App.vue'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')

socket_manager.connect()