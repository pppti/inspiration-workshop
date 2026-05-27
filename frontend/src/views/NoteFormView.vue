<template>
  <div class="px-4 py-4">
    <div class="flex items-center justify-between mb-4"><h2 class="font-bold text-slate-800">{{ isEdit?'编辑笔记':'新建笔记' }}</h2><button v-if="!isEdit" type="button" @click="showImport=true" class="px-3 py-1.5 text-xs bg-amber-400 text-white rounded-lg hover:bg-amber-500">AI 导入</button></div>
    <!-- AI import modal -->
    <div v-if="showImport" class="fixed inset-0 bg-slate-900/40 z-50 flex items-end sm:items-center justify-center p-4">
      <div class="bg-white rounded-t-2xl sm:rounded-2xl w-full max-w-md p-5 space-y-3">
        <h3 class="font-bold text-slate-800">AI 智能导入</h3>
        <textarea v-model="aiText" rows="4" placeholder="粘贴文字或点击录音..." class="w-full px-4 py-3 rounded-lg border border-purple-200 text-sm focus:outline-none focus:border-purple-500 resize-none"></textarea>
        <button @click="startVoice" type="button" :disabled="voiceActive" class="w-full py-2 border border-purple-300 rounded-lg text-sm text-purple-600 hover:bg-purple-50 disabled:opacity-50">{{ voiceActive?'录音中...点击停止':'🎤 语音输入' }}</button>
        <div class="flex gap-2">
          <button @click="aiImport" :disabled="!aiText.trim()||aiLoading" class="flex-1 py-2 bg-purple-800 text-white rounded-lg text-sm hover:bg-purple-700 disabled:opacity-50">{{ aiLoading?'AI 处理中...':'AI 导入' }}</button>
          <button @click="showImport=false;aiText=''" class="px-4 py-2 border border-purple-200 rounded-lg text-sm text-slate-500">取消</button>
        </div>
      </div>
    </div>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <input v-model="form.title" type="text" placeholder="标题（可选）" class="w-full px-4 py-3 rounded-lg border border-purple-200 focus:outline-none focus:border-purple-500" />
      <textarea v-model="form.body" rows="10" placeholder="记录你的灵感..." required class="w-full px-4 py-3 rounded-lg border border-purple-200 focus:outline-none focus:border-purple-500 resize-none"></textarea>
      <div><p class="text-sm text-slate-500 mb-2">分类</p><div class="flex gap-2 flex-wrap"><button v-for="c in cats" :key="c.value" type="button" @click="form.category=form.category===c.value?null:c.value" class="px-3 py-1.5 rounded-full text-sm border transition-colors" :class="form.category===c.value?'bg-purple-200 border-purple-400 text-purple-800':'bg-white border-purple-200 text-slate-600'">{{c.label}}</button></div></div>
      <div><input v-model="form.source" type="text" placeholder="来源（可选）" class="w-full px-4 py-3 rounded-lg border border-purple-200 focus:outline-none focus:border-purple-500" /></div>
      <div><input v-model="tagInput" @keyup.enter.prevent="addTag" placeholder="添加标签，回车确认" class="w-full px-4 py-3 rounded-lg border border-purple-200 focus:outline-none focus:border-purple-500" /><div v-if="form.tags.length" class="flex gap-1 flex-wrap mt-2"><span v-for="(t,i) in form.tags" :key="i" @click="form.tags.splice(i,1)" class="text-xs px-2 py-1 bg-purple-100 text-purple-600 rounded-full cursor-pointer">{{t}} ✕</span></div></div>
      <p v-if="error" class="text-rose-500 text-sm">{{ error }}</p>
      <button type="submit" :disabled="saving" class="w-full py-3 bg-purple-800 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 font-bold">{{ saving?'保存中...':'保存' }}</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'; import { useRoute, useRouter } from 'vue-router'; import { useApi } from '../composables/useApi'
const route = useRoute(); const router = useRouter(); const api = useApi(); const isEdit = !!route.params.id
const cats = [{value:'character',label:'人物设定'},{value:'plot',label:'情节构思'},{value:'dialogue',label:'对白片段'},{value:'scene',label:'场景描写'},{value:'material',label:'素材收集'},{value:'essay',label:'随感随笔'}]
const form = ref({ title:'', body:'', category:null, source:'', tags:[] }); const tagInput = ref('')
const saving = ref(false); const error = ref(''); const showImport = ref(false); const aiText = ref(''); const aiLoading = ref(false); const voiceActive = ref(false); let recognition = null

function addTag() { const t=tagInput.value.trim(); if(t&&!form.value.tags.includes(t)) form.value.tags.push(t); tagInput.value='' }
async function aiImport() {
  if(!aiText.value.trim()||aiLoading.value) return; aiLoading.value=true
  const {data} = await api.post('/ai/import',{text:aiText.value})
  if(data){ form.value.title=data.title; form.value.body=data.body; form.value.category=data.category; form.value.tags=data.tags||[]; showImport.value=false; aiText.value='' }
  aiLoading.value=false
}
function startVoice() {
  const SR = window.SpeechRecognition||window.webkitSpeechRecognition; if(!SR) return
  if(voiceActive.value){ recognition.stop(); voiceActive.value=false; return }
  recognition = new SR(); recognition.lang='zh-CN'; recognition.interimResults=false
  recognition.onresult = (e) => { aiText.value = e.results[0][0].transcript; voiceActive.value=false }
  recognition.onend = () => { voiceActive.value=false }; recognition.start(); voiceActive.value=true
}
async function handleSubmit() {
  error.value=''; saving.value=true
  try {
    if(isEdit){ await api.put(`/notes/${route.params.id}`,form.value) } else { await api.post('/notes',form.value) }
    router.push('/notes')
  } catch(e) { error.value=e.message } finally { saving.value=false }
}
onMounted(async () => {
  if(isEdit){ const {data}=await api.get(`/notes/${route.params.id}`); if(data) form.value={title:data.title||'',body:data.body,category:data.category,source:data.source||'',tags:data.tags||[]} }
})
</script>
