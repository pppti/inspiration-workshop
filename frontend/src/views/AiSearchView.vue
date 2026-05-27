<template>
  <div class="px-4 py-4">
    <h2 class="font-bold text-slate-800 mb-4">AI 搜索</h2>
    <p class="text-sm text-slate-500 mb-4">用自然语言描述你想找的灵感内容</p>
    <form @submit.prevent="doSearch" class="flex gap-2 mb-4">
      <input v-model="query" placeholder="例如：关于雨天的场景描写" class="flex-1 px-4 py-2.5 rounded-lg border border-purple-200 text-sm focus:outline-none focus:border-purple-500" />
      <button type="submit" :disabled="!query.trim()||searching" class="px-5 py-2.5 bg-purple-800 text-white rounded-lg text-sm hover:bg-purple-700 disabled:opacity-40">{{searching?'搜索中...':'搜索'}}</button>
    </form>
    <p v-if="searchSummary" class="text-sm text-slate-600 mb-4">{{ searchSummary }}</p>
    <div v-if="searchResults.length" class="space-y-3">
      <div v-for="r in searchResults" :key="r.id" @click="$router.push(`/notes/${r.id}`)" class="bg-white rounded-lg p-4 border border-purple-100 hover:border-purple-300 cursor-pointer transition-colors">
        <p class="font-medium text-sm text-slate-800">{{ r.title }}</p>
        <p class="text-xs text-slate-500 mt-1">{{ r.snippet }}</p>
        <p class="text-xs text-amber-600 mt-1">{{ r.relevance }}</p>
      </div>
    </div>
    <EmptyState v-if="!searching&&query&&!searchResults.length" text="没有找到匹配的灵感" />
  </div>
</template>

<script setup>
import { ref } from 'vue'; import { useApi } from '../composables/useApi'; import EmptyState from '../components/common/EmptyState.vue'
const api = useApi(); const query = ref(''); const searching = ref(false); const searchResults = ref([]); const searchSummary = ref('')
async function doSearch() {
  if(!query.value.trim()||searching.value) return; searching.value=true; searchResults.value=[]; searchSummary.value=''
  const {data}=await api.post('/ai/search',{query:query.value})
  if(data){ searchResults.value=data.results||[]; searchSummary.value=data.summary }
  searching.value=false
}
</script>
