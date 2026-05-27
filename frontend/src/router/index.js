import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterView.vue'), meta: { guest: true } },
  { path: '/', name: 'Home', component: () => import('../views/HomeView.vue') },
  { path: '/notes', name: 'NoteList', component: () => import('../views/NoteListView.vue') },
  { path: '/notes/new', name: 'NoteNew', component: () => import('../views/NoteFormView.vue') },
  { path: '/notes/:id', name: 'NoteDetail', component: () => import('../views/NoteDetailView.vue') },
  { path: '/notes/:id/edit', name: 'NoteEdit', component: () => import('../views/NoteFormView.vue') },
  { path: '/import', name: 'Import', component: () => import('../views/SmartImportView.vue') },
  { path: '/ai-search', name: 'AiSearch', component: () => import('../views/AiSearchView.vue') },
  { path: '/chat', name: 'Chat', component: () => import('../views/ChatView.vue') },
  { path: '/settings', name: 'Settings', component: () => import('../views/SettingsView.vue') },
]

const router = createRouter({ history: createWebHashHistory(), routes })
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.guest) return auth.token ? next('/') : next()
  if (!auth.token && to.name !== 'Login' && to.name !== 'Register') return next('/login')
  next()
})
export default router
