<template>
  <div class="h-[calc(100vh-7rem)] flex flex-col">
    <div class="flex-1 overflow-y-auto px-4 py-3 space-y-3" ref="chatContainer">
      <div v-if="messages.length===0" class="text-center py-12">
        <p class="text-slate-400 text-sm mb-2">和 AI 助手聊聊创作灵感</p>
        <div class="flex flex-wrap gap-2 justify-center"><button v-for="q in suggestions" :key="q" @click="sendMessage(q)" class="px-3 py-1.5 text-xs bg-purple-100 text-purple-600 rounded-full hover:bg-purple-200">{{q}}</button></div>
      </div>
      <div v-for="(msg,i) in messages" :key="i" class="flex" :class="msg.role==='user'?'justify-end':'justify-start'">
        <div class="max-w-[85%] rounded-xl px-4 py-2.5 text-sm leading-relaxed" :class="msg.role==='user'?'bg-purple-800 text-white':'bg-white border border-purple-200 text-slate-700'">{{msg.content}}</div>
      </div>
      <div v-if="loading" class="flex justify-start"><div class="bg-white border border-purple-200 rounded-xl px-4 py-3"><span class="inline-flex gap-1"><span class="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce" style="animation-delay:0s"></span><span class="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce" style="animation-delay:0.15s"></span><span class="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce" style="animation-delay:0.3s"></span></span></div></div>
    </div>
    <div class="px-4 py-3 border-t border-purple-100"><form @submit.prevent="sendMessage()" class="flex gap-2"><input v-model="input" type="text" placeholder="说说你想写什么..." class="flex-1 px-4 py-2.5 rounded-xl border border-purple-200 text-sm focus:outline-none focus:border-purple-500" :disabled="loading" /><button type="submit" :disabled="!input.trim()||loading" class="px-5 py-2.5 bg-purple-800 text-white rounded-xl text-sm hover:bg-purple-700 disabled:opacity-40">发送</button></form></div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'; import { useApi } from '../composables/useApi'
const api = useApi(); const input = ref(''); const loading = ref(false); const messages = ref([]); const conversationId = ref(null); const chatContainer = ref(null)
const suggestions = ref(['帮我设计一个反派角色','给我一些奇幻世界的设定','描写一段雨夜离别的场景','怎么写好故事的开头'])
async function sendMessage(text) {
  const msg=text||input.value.trim(); if(!msg||loading.value) return
  messages.value.push({role:'user',content:msg}); input.value=''; loading.value=true
  await nextTick(); if(chatContainer.value) chatContainer.value.scrollTop=chatContainer.value.scrollHeight
  const {data}=await api.post('/ai/chat',{conversation_id:conversationId.value,message:msg})
  if(data){ conversationId.value=data.conversation_id; messages.value.push({role:'assistant',content:data.reply}) }
  else messages.value.push({role:'assistant',content:'抱歉，出了点问题。'})
  loading.value=false; await nextTick(); if(chatContainer.value) chatContainer.value.scrollTop=chatContainer.value.scrollHeight
}
onMounted(async ()=>{})
</script>

<style scoped>
@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}.animate-bounce{animation:bounce 1.4s infinite}
</style>
