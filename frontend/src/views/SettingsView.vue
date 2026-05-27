<template>
  <div class="px-4 py-4"><h2 class="font-bold text-slate-800 mb-6">设置</h2>
    <div class="space-y-3">
      <div class="bg-white rounded-xl p-4 border border-purple-200"><p class="text-sm text-slate-500">当前用户</p><p class="font-medium text-slate-800">{{user?.username}}</p></div>
      <router-link to="/chat" class="block bg-white rounded-xl p-4 border border-purple-200 hover:border-purple-400"><span class="text-slate-800">AI 对话</span></router-link>
      <router-link to="/ai-search" class="block bg-white rounded-xl p-4 border border-purple-200 hover:border-purple-400"><span class="text-slate-800">AI 搜索</span></router-link>
      <button @click="exportData" class="w-full bg-white rounded-xl p-4 border border-purple-200 hover:border-purple-400 text-left"><span class="text-slate-800">导出数据 (JSON)</span></button>
      <button @click="handleLogout" class="w-full mt-8 py-3 border border-rose-500 text-rose-500 rounded-lg hover:bg-rose-50">退出登录</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'; import { useRouter } from 'vue-router'; import { useAuthStore } from '../stores/auth'; import { useApi } from '../composables/useApi'
const router = useRouter(); const auth = useAuthStore(); const api = useApi(); const user = ref(null)
onMounted(async ()=>{ user.value=auth.user })
async function exportData() {
  const {data}=await api.get('/notes?limit=10000')
  const d={exported_at:new Date().toISOString(),notes:data?.items||[]}
  const blob=new Blob([JSON.stringify(d,null,2)],{type:'application/json'}); const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download=`inspiration-backup-${new Date().toISOString().slice(0,10)}.json`; a.click(); URL.revokeObjectURL(url)
}
function handleLogout(){ auth.logout(); router.push('/login') }
</script>
