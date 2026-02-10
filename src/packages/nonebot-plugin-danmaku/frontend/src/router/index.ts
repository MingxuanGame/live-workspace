import { createRouter, createWebHistory } from 'vue-router'
import DanmakuView from '@/views/DanmakuView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'danmaku',
      component: DanmakuView
    }
  ],
})

export default router
