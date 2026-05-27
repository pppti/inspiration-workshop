<template>
  <header class="sticky top-0 bg-purple-50/90 backdrop-blur border-b border-purple-200 z-40">
    <div class="flex items-center justify-between px-4 h-12">
      <button v-if="showBack" @click="$router.back()" class="text-purple-700 p-1 -ml-1">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      </button>
      <div v-else class="w-7" />
      <h1 class="text-base font-bold text-purple-900">{{ title }}</h1>
      <div class="w-7" />
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'; import { useRoute } from 'vue-router'
const route = useRoute()
const showBack = computed(() => { const n = route.name; return n && !['Home','Login','Register'].includes(n) })
const titles = { Home:'灵感工坊', Login:'登录', Register:'注册', NoteList:'灵感笔记', NoteNew:'新建笔记', NoteEdit:'编辑笔记', NoteDetail:'笔记详情', Import:'智能导入', AiSearch:'AI 搜索', Chat:'AI 对话', Settings:'设置' }
const title = computed(() => titles[route.name] || '灵感工坊')
</script>
