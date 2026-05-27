<template>
  <div class="min-h-screen flex items-center justify-center px-6 bg-purple-50">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8"><h1 class="text-3xl font-bold text-purple-900 mb-2">灵感工坊</h1><p class="text-purple-500 text-sm">捕捉每一个灵感闪光</p></div>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <input v-model="username" type="text" placeholder="用户名" required class="w-full px-4 py-3 rounded-lg border border-purple-200 bg-white focus:outline-none focus:border-purple-500" />
        <input v-model="password" type="password" placeholder="密码" required class="w-full px-4 py-3 rounded-lg border border-purple-200 bg-white focus:outline-none focus:border-purple-500" />
        <p v-if="error" class="text-rose-500 text-sm text-center">{{ error }}</p>
        <button type="submit" :disabled="loading" class="w-full py-3 bg-purple-800 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors font-bold">{{ loading ? '登录中...' : '登录' }}</button>
      </form>
      <p class="text-center mt-6 text-purple-500 text-sm">还没有账号？<router-link to="/register" class="text-purple-700 underline">注册</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'; import { useRouter } from 'vue-router'; import { useAuthStore } from '../stores/auth'
const router = useRouter(); const auth = useAuthStore()
const username = ref(''); const password = ref(''); const error = ref(''); const loading = ref(false)
async function handleLogin() {
  error.value = ''; loading.value = true
  try { await auth.login(username.value, password.value); router.push('/') }
  catch (e) { error.value = e.message } finally { loading.value = false }
}
</script>
