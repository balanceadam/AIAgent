<script setup lang="ts">
import { useLaunchStore } from '@/stores/launch'
import Layout from '@/layout/Index.vue'
import LayoutDefault from '@/layout/Default.vue'

const launchStore = useLaunchStore()

// 获取用户是否在白名单
launchStore.getInWhitelist()
</script>

<template>
  <LayoutDefault v-if="$route.path !== '/'" />
  <Layout v-else />
</template>
