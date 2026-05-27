<template>
  <div class="px-4 py-4">
    <div v-if="loading" class="text-center py-12 text-slate-400">加载中...</div>
    <template v-else-if="note">
      <div class="bg-white rounded-xl p-5 border border-purple-200 shadow-sm">
        <div class="flex items-center justify-between mb-3"><h1 class="text-xl font-bold text-slate-900">{{ note.title || '无标题' }}</h1><span v-if="note.category" class="text-xs px-2 py-1 bg-purple-100 text-purple-600 rounded-full">{{ cats[note.category]||note.category }}</span></div>
        <p class="text-slate-700 leading-relaxed whitespace-pre-wrap">{{ note.body }}</p>
        <div class="flex items-center gap-2 flex-wrap mt-3"><span v-for="t in note.tags" :key="t" class="text-xs px-2 py-0.5 bg-slate-100 text-slate-500 rounded-full">{{ t }}</span></div>
        <p v-if="note.source" class="text-sm text-slate-500 mt-3">来源：{{ note.source }}</p>
      </div>
      <div class="flex gap-3 mt-8">
        <button @click="$router.push(`/notes/${note.id}/edit`)" class="flex-1 py-2.5 border border-purple-400 text-purple-700 rounded-lg text-sm hover:bg-purple-100">编辑</button>
        <button @click="handleDelete" class="flex-1 py-2.5 border border-rose-500 text-rose-500 rounded-lg text-sm hover:bg-rose-50">删除</button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'; import { useRoute, useRouter } from 'vue-router'; import { useApi } from '../composables/useApi'
const route = useRoute(); const router = useRouter(); const api = useApi(); const note = ref(null); const loading = ref(true)
const cats = { character:'人物设定', plot:'情节构思', dialogue:'对白片段', scene:'场景描写', material:'素材收集', essay:'随感随笔' }
onMounted(async () => { const {data}=await api.get(`/notes/${route.params.id}`); if(data) note.value=data; loading.value=false })
async function handleDelete() { if(!confirm('确定删除？')) return; await api.delete(`/notes/${route.params.id}`); router.push('/notes') }
</script>
