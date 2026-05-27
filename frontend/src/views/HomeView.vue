<template>
  <div class="px-4 py-4 space-y-6">
    <div class="bg-white rounded-xl p-5 border border-purple-200 shadow-sm">
      <h2 class="font-bold text-purple-900 mb-3">AI 灵感生成</h2>
      <form @submit.prevent="getInspire" class="flex gap-2">
        <input v-model="direction" placeholder="我想要一个...的灵感" class="flex-1 px-4 py-2.5 rounded-lg border border-purple-200 text-sm focus:outline-none focus:border-purple-500" />
        <button type="submit" :disabled="!direction.trim() || inspireLoading" class="px-4 py-2.5 bg-purple-800 text-white rounded-lg text-sm hover:bg-purple-700 disabled:opacity-40">生成</button>
      </form>
      <div v-if="inspireResult" class="mt-3 p-3 bg-purple-50 rounded-lg text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">{{ inspireResult }}</div>
    </div>

    <div class="grid grid-cols-2 gap-3">
      <button @click="$router.push('/notes/new')" class="p-4 bg-white rounded-xl border border-purple-200 hover:border-purple-400 text-left transition-colors">
        <span class="text-lg">📝</span><p class="font-medium text-sm mt-1 text-slate-700">写笔记</p>
      </button>
      <button @click="$router.push('/import')" class="p-4 bg-white rounded-xl border border-purple-200 hover:border-purple-400 text-left transition-colors">
        <span class="text-lg">📥</span><p class="font-medium text-sm mt-1 text-slate-700">智能导入</p>
      </button>
      <button @click="$router.push('/ai-search')" class="p-4 bg-white rounded-xl border border-purple-200 hover:border-purple-400 text-left transition-colors">
        <span class="text-lg">🔍</span><p class="font-medium text-sm mt-1 text-slate-700">AI 搜索</p>
      </button>
      <button @click="$router.push('/chat')" class="p-4 bg-white rounded-xl border border-purple-200 hover:border-purple-400 text-left transition-colors">
        <span class="text-lg">💡</span><p class="font-medium text-sm mt-1 text-slate-700">AI 对话</p>
      </button>
    </div>

    <div>
      <div class="flex items-center justify-between mb-3"><h2 class="font-bold text-slate-800">最近灵感</h2><router-link to="/notes" class="text-xs text-purple-500">全部</router-link></div>
      <div v-if="loading" class="text-center text-purple-400 py-6">加载中...</div>
      <EmptyState v-else-if="notes.length===0" text="还没有灵感笔记" />
      <div v-else class="space-y-2">
        <div v-for="n in notes" :key="n.id" @click="$router.push(`/notes/${n.id}`)" class="bg-white rounded-lg p-3 border border-purple-100 hover:border-purple-300 cursor-pointer transition-colors">
          <div class="flex items-center justify-between mb-1"><span class="font-medium text-sm text-slate-800">{{ n.title || '无标题' }}</span><span v-if="n.category" class="text-xs px-2 py-0.5 bg-purple-100 text-purple-600 rounded-full">{{ catNames[n.category] || n.category }}</span></div>
          <p class="text-xs text-slate-500 line-clamp-2">{{ n.body }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'; import { useApi } from '../composables/useApi'; import EmptyState from '../components/common/EmptyState.vue'
const api = useApi(); const notes = ref([]); const loading = ref(true)
const direction = ref(''); const inspireLoading = ref(false); const inspireResult = ref('')
const catNames = { character:'人物', plot:'情节', dialogue:'对白', scene:'场景', material:'素材', essay:'随笔' }

async function getInspire() {
  inspireLoading.value = true; inspireResult.value = ''
  const { data } = await api.post('/ai/inspire', { direction: direction.value })
  if (data) inspireResult.value = data.suggestions
  inspireLoading.value = false
}

onMounted(async () => {
  const { data } = await api.get('/notes?limit=5')
  if (data) notes.value = data.items
  loading.value = false
})
</script>
