<template>
  <nav class="fixed bottom-0 inset-x-0 bg-purple-50/95 backdrop-blur border-t border-purple-200 safe-bottom z-40">
    <div class="flex items-stretch max-w-lg mx-auto">
      <RouterLink v-for="item in navItems" :key="item.to" :to="item.to"
        class="flex flex-col items-center justify-center flex-1 py-1 text-xs transition-colors"
        :class="item.active ? 'text-purple-800' : 'text-purple-400'">
        <svg class="w-5 h-5 mb-0.5" :class="{ 'text-purple-700': item.active }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" :d="item.icon" />
        </svg>
        <span>{{ item.label }}</span>
      </RouterLink>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'; import { useRoute } from 'vue-router'; const route = useRoute()
const icons = {
  home: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
  notes: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
  import: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12',
  ai: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',
  settings: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z',
}
const items = [
  { to: '/', label: '首页', key: 'home' },
  { to: '/notes', label: '笔记', key: 'notes' },
  { to: '/import', label: '导入', key: 'import' },
  { to: '/chat', label: 'AI', key: 'ai' },
  { to: '/settings', label: '设置', key: 'settings' },
]
const navItems = computed(() => items.map(item => ({ ...item, icon: icons[item.key], active: item.to === '/' ? route.path === '/' : route.path.startsWith(item.to) })))
</script>
