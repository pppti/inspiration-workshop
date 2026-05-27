<template>
  <div class="px-4 py-4">
    <h2 class="font-bold text-slate-800 mb-4">智能导入</h2>
    <div class="flex gap-2 mb-4">
      <button v-for="t in tabs" :key="t.key" @click="mode=t.key" class="flex-1 py-2 text-sm rounded-lg transition-colors" :class="mode===t.key?'bg-purple-200 text-purple-800 font-medium':'bg-white border border-purple-200 text-slate-500'">{{t.label}}</button>
    </div>

    <div v-if="mode==='text'" class="space-y-3">
      <textarea v-model="inputText" rows="8" placeholder="在此粘贴或输入文字..." class="w-full px-4 py-3 rounded-xl border border-purple-200 focus:outline-none focus:border-purple-500 resize-none text-sm"></textarea>
      <button @click="processText" :disabled="!inputText.trim()||loading" class="w-full py-3 bg-purple-800 text-white rounded-xl hover:bg-purple-700 disabled:opacity-40 font-bold">{{loading?'AI 整理中...':'AI 整理'}}</button>
    </div>

    <div v-if="mode==='voice'" class="space-y-3">
      <div class="bg-white rounded-xl p-6 border border-purple-200 text-center">
        <button @click="toggleRecording" class="w-20 h-20 rounded-full mx-auto flex items-center justify-center transition-all" :class="recording?'bg-rose-500 animate-pulse':'bg-purple-800 hover:bg-purple-700'">
          <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24"><path v-if="!recording" d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path v-if="!recording" d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/><rect v-if="recording" x="6" y="6" width="12" height="12" rx="2"/></svg>
        </button>
        <p class="text-sm text-slate-500 mt-3">{{recording?'录音中...点击停止':'点击开始录音'}}</p>
      </div>
      <textarea v-if="inputText" v-model="inputText" rows="5" class="w-full px-4 py-3 rounded-xl border border-purple-200 focus:outline-none focus:border-purple-500 resize-none text-sm"></textarea>
      <div v-if="inputText" class="flex gap-2">
        <button @click="processText" :disabled="loading" class="flex-1 py-3 bg-purple-800 text-white rounded-xl hover:bg-purple-700 disabled:opacity-40 font-bold text-sm">{{loading?'AI 整理中...':'AI 整理'}}</button>
        <button @click="inputText=''" class="px-4 py-3 border border-purple-200 rounded-xl text-sm text-slate-500">清除</button>
      </div>
    </div>

    <div v-if="result" class="mt-6 space-y-4">
      <div class="bg-amber-50 rounded-xl p-4 border border-amber-200">
        <label class="text-xs text-slate-500">标题</label><input v-model="result.title" class="w-full px-3 py-2 rounded-lg border border-purple-200 text-sm mb-3 focus:outline-none focus:border-purple-500" />
        <label class="text-xs text-slate-500">正文</label><textarea v-model="result.body" rows="6" class="w-full px-3 py-2 rounded-lg border border-purple-200 text-sm mb-3 focus:outline-none focus:border-purple-500 resize-none"></textarea>
        <label class="text-xs text-slate-500">分类</label>
        <select v-model="result.category" class="w-full px-3 py-2 rounded-lg border border-purple-200 text-sm bg-white mb-3"><option v-for="c in cats" :key="c.value" :value="c.value">{{c.label}}</option></select>
        <div v-if="result.tags?.length" class="flex gap-1 flex-wrap"><span v-for="t in result.tags" :key="t" class="text-xs px-2 py-0.5 bg-white rounded-full border border-amber-200 text-amber-700">{{t}}</span></div>
      </div>
      <button @click="saveNote" :disabled="saving" class="w-full py-3 bg-purple-800 text-white rounded-xl hover:bg-purple-700 disabled:opacity-40 font-bold">{{saving?'保存中...':'保存为笔记'}}</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'; import { useRouter } from 'vue-router'; import { useApi } from '../composables/useApi'
const router = useRouter(); const api = useApi()
const tabs = [{key:'text',label:'文字'},{key:'voice',label:'语音'}]; const mode = ref('text')
const inputText = ref(''); const loading = ref(false); const saving = ref(false); const result = ref(null)
const cats = [{value:'character',label:'人物设定'},{value:'plot',label:'情节构思'},{value:'dialogue',label:'对白片段'},{value:'scene',label:'场景描写'},{value:'material',label:'素材收集'},{value:'essay',label:'随感随笔'}]
let recognition = null; const recording = ref(false)

async function processText() {
  if(!inputText.value.trim()||loading.value) return; loading.value=true
  const {data}=await api.post('/ai/import',{text:inputText.value})
  if(data) result.value={title:data.title||'',body:data.body||inputText.value,category:data.category,tags:data.tags||[]}
  loading.value=false
}
function toggleRecording() {
  if(recording.value){ recognition?.stop(); recording.value=false; return }
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition; if(!SR){ inputText.value='[浏览器不支持语音识别]'; return }
  recognition=new SR(); recognition.lang='zh-CN'; recognition.interimResults=true; recognition.continuous=true
  let final=''; recognition.onresult=(e)=>{ let interim=''; for(let i=e.resultIndex;i<e.results.length;i++){if(e.results[i].isFinal) final+=e.results[i][0].transcript; else interim+=e.results[i][0].transcript} inputText.value=final+interim }
  recognition.onend=()=>{ recording.value=false }; recognition.start(); recording.value=true
}
async function saveNote() {
  if(!result.value) return; saving.value=true
  const {error}=await api.post('/notes',{title:result.value.title,body:result.value.body,category:result.value.category,tags:result.value.tags||[]})
  saving.value=false; if(!error){ result.value=null; inputText.value=''; router.push('/notes') }
}
</script>
