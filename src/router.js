import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from './views/Dashboard.vue'
import Settings from './views/Settings.vue'

export default createRouter({

  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/settings', component: Settings },
  ]
})