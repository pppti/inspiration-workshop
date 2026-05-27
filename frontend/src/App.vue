<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1 pb-20 safe-bottom">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in"><component :is="Component" /></transition>
      </router-view>
    </main>
    <BottomNav v-if="showNav" />
  </div>
</template>

<script setup>
import { computed } from 'vue'; import { useRoute } from 'vue-router'
import AppHeader from './components/common/AppHeader.vue'; import BottomNav from './components/common/BottomNav.vue'
const route = useRoute()
const showNav = computed(() => !['Login', 'Register'].includes(route.name))
</script>
