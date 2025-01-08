<script setup lang="ts">
import { useAssetsStore } from '@/stores/assets'
import { useSocialStore } from '@/stores/social'
import type { AssetsToken } from '@/types'
import { useRoute } from 'vue-router'

const { getEpalToken } = useAssetsStore()
const { getCommentList } = useSocialStore()
const route = useRoute()

const token = ref<AssetsToken>({
  id: 0,
  account: 0,
  chain: {
    id: 0,
    name: '',
    fee: 0,
    symbol: ''
  },
  fillingServices: [],
  games: [],
  protocol: {
    address: '',
    price: 0,
    protocolId: 0,
    symbol: '',
    id: 0,
    bondingCurve: 0,
    marketValue: 0,
    dayIncrease: 0,
    dayTradingVolume: 0,
    createdAt: '',
    updatedAt: ''
  },
  name: '',
  ticker: '',
  website: '',
  twitter: '',
  telegram: '',
  description: '',
  labels: '',
  logo: '',
  epal: '',
  isEnabled: false,
  createdAt: '',
  updatedAt: ''
})

const init = async () => {
  try {
    const id = Number(route.params.id)
    token.value = await getEpalToken(id)
    await getCommentList(id)
  } catch (error) {
    window.$message.error('Something went wrong, please try again later')
  }
}

init()
</script>
<template>
  <div class="epal">
    <EpalDetail v-if="token.logo" :token="token"></EpalDetail>
  </div>
</template>
