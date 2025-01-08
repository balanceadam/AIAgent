import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import('@/views/IndexView.vue')
    },
    {
      path: '/epal',
      name: 'epal',
      component: () => import('@/views/EpalView.vue'),
      children: [
        {
          path: '',
          name: 'epal-list',
          component: () => import('@/views/EpalListView.vue')
        },
        {
          path: ':id',
          name: 'epal-detail',
          component: () => import('@/views/EpalDetailView.vue')
        },
        {
          path: 'edit',
          name: 'epal-edit',
          component: () => import('@/views/EpalEditView.vue')
        }
      ]
    },
    {
      path: '/ranking',
      name: 'ranking',
      component: () => import('@/views/RankingView.vue')
    },
    {
      path: '/earn',
      name: 'earn',
      component: () => import('@/views/EarnView.vue')
    },
    {
      path: '/docs',
      name: 'docs',
      component: () => import('@/views/DocsView.vue')
    },
    {
      path: '/me',
      name: 'me',
      component: () => import('@/views/MeView.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue')
    },
    {
      path: '/launch',
      name: 'launch',
      component: () => import('@/views/LaunchView.vue')
    }
  ]
})

export default router
