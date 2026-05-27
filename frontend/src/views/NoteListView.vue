<template>
  <div class="px-4 py-4">
    <div class="flex items-center justify-between mb-4"><h2 class="font-bold text-slate-800">灵感笔记</h2><router-link to="/notes/new" class="bg-purple-800 text-white px-4 py-1.5 rounded-lg text-sm hover:bg-purple-700">新建</router-link></div>
    <div class="flex gap-2 mb-4">
      <input v-model="search" @input="searchDebounced" placeholder="搜索..." class="flex-1 px-3 py-2 rounded-lg border border-purple-200 text-sm focus:outline-none focus:border-purple-500" />
      <select v-model="category" @change="fetchNotes" class="px-3 py-2 rounded-lg border border-purple-200 text-sm bg-white text-slate-600">
        <option value="">全部分类</option><option v-for="(v,k) in cats" :key="k" :value="k">{{ v }}</option>
      </select>
      <button v-if="selectedIds.length" @click="summarizeSelected" class="px-3 py-1.5 bg-amber-400 text-white rounded-lg text-xs hover:bg-amber-500">汇总{{selectedIds.length}}篇</button>
    </div>
    <div v-if="summarizeResult" class="bg-white rounded-xl p-4 border border-amber-300 mb-4"><p class="text-sm text-slate-700 whitespace-pre-wrap">{{ summarizeResult }}</p><button @click="summarizeResult=''" class="text-xs text-slate-400 mt-2">关闭</button></div>
    <div v-if="loading" class="text-center text-slate-400 py-6">加载中...</div>
    <EmptyState v-else-if="notes.length===0" text="还没有灵感笔记" />
    <div v-else class="space-y-2">
      <div v-for="n in notes" :key="n.id" class="bg-white rounded-lg p-3 border transition-colors cursor-pointer" :class="selectedIds.includes(n.id)?'border-amber-400 bg-amber-50':'border-purple-100 hover:border-purple-300'">
        <div class="flex items-center gap-2 mb-1">
          <input type="checkbox" :checked="selectedIds.includes(n.id)" @click.stop @change="toggleSelect(n.id)" class="rounded shrink-0" />
          <span class="font-medium text-sm text-slate-800 flex-1" @click="$router.push(`/notes/${n.id}`)">{{ n.title || '无标题' }}</span>
          <span v-if="n.category" class="text-xs px-2 py-0.5 bg-purple-100 text-purple-600 rounded-full">{{ cats[n.category] || n.category }}</span>
        </div>
        <p class="text-xs text-slate-500 line-clamp-2" @click="$router.push(`/notes/${n.id}`)">{{ n.body }}</p>
        <div class="flex gap-1 mt-1.5 flex-wrap"><span v-for="t in n.tags" :key="t" class="text-xs px-1.5 py-0.5 bg-slate-100 text-slate-500 rounded">{{ t }}</span></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'; import { useApi } from '../composables/useApi'; import EmptyState from '../components/common/EmptyState.vue'
const api = useApi(); const notes = ref([]); const loading = ref(true); const search = ref(''); const category = ref('')
const selectedIds = ref([]); const summarizeResult = ref('')
const cats = { character:'人物设定', plot:'情节构思', dialogue:'对白片段', scene:'场景描写', material:'素材收集', essay:'随感随笔' }
let timer = null
function searchDebounced() { clearTimeout(timer); timer = setTimeout(fetchNotes, 300) }
function toggleSelect(id) { const i = selectedIds.value.indexOf(id); if(i===-1) selectedIds.value.push(id); else selectedIds.value.splice(i,1) }
async function summarizeSelected() {
  if(!selectedIds.value.length) return; summarizeResult.value='AI 汇总中...'
  const { data } = await api.post('/ai/summarize', { note_ids: selectedIds.value })
  summarizeResult.value = data?.summary || '汇总失败'
}
async function fetchNotes() {
  loading.value = true; let url = '/notes?limit=50'
  if(search.value) url += '&search=' + encodeURIComponent(search.value)
  if(category.value) url += '&category=' + category.value
  const { data } = await api.get(url); if(data) notes.value = data.items; loading.value = false
}
onMounted(fetchNotes)
</script>
