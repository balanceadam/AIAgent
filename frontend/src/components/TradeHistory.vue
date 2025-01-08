<script lang="ts" setup>
import dayjs from 'dayjs'
import localizedFormat from 'dayjs/plugin/localizedFormat'
import { useAssetsStore } from '@/stores/assets'
import type { Results, Transaction } from '@/types'

dayjs.extend(localizedFormat)

const assetsStore = useAssetsStore()

const isLoading = ref(false)
const count = ref(0)
const next = ref('')
const page = ref(1)
const size = ref(20)
const transactions = ref<Transaction[]>([])

const fetchHistoryList = async (init: boolean = false) => {
  if (next.value) {
    page.value += 1
  }
  if (!init && !next.value) {
    return
  }
  let res: Results<Transaction>
  try {
    isLoading.value = true
    res = await assetsStore.getTransactions(assetsStore.token.id, page.value, size.value)
    count.value = res.count
    next.value = res.next
    transactions.value = transactions.value.concat(res.results)
    isLoading.value = false
  } catch (error) {
    isLoading.value = false
    console.error(error)
  }
}

fetchHistoryList(true)
</script>

<template>
  <empty v-if="!isLoading && !transactions.length" description="No transactions yet"> </empty>
  <n-infinite-scroll
    style="height: 240px"
    :distance="10"
    @load="fetchHistoryList"
    v-if="transactions.length"
  >
    <div class="trade-history">
      <div class="history-header">
        <div class="th-item">account</div>
        <div class="th-item">type</div>
        <div class="th-item">EPT</div>
        <div class="th-item">{{ assetsStore.token.ticker }}</div>
        <div class="th-item date flex-center">date</div>
        <div class="th-item flex-end">transaction</div>
      </div>
      <n-virtual-list :item-size="80" :items="transactions">
        <template #default="{ item }">
          <div :key="item.id" class="item" style="height: 80px">
            <div class="td account">
              <img v-if="item.account.avatar" :src="item.account.avatar" alt="" />
              <img v-else src="https://picsum.photos/350/350" alt="" />
              <div class="name">{{ item.account.name }}</div>
            </div>
            <div class="td symbol" :style="{ color: item.type === 'Buy' ? '#00A878' : '#DA4354' }">
              {{ item.type }}
            </div>
            <div class="td amount">{{ item.amount }}</div>
            <div class="td cics">{{ item.quantity }}</div>
            <div class="td date flex-center">{{ dayjs(item.time).format('MMM D, h:mm:ss a') }}</div>
            <div class="td transaction flex-end">{{ item.hash }}</div>
          </div>
        </template>
      </n-virtual-list>
    </div>
  </n-infinite-scroll>
</template>

<style lang="scss" scoped>
.trade-history {
  display: flex;
  padding: 0px;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  align-self: stretch;

  .history-header {
    display: flex;
    height: 80px;
    padding: 24px 0px;
    // justify-content: space-between;
    align-items: center;
    align-self: stretch;
    gap: 100px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);

    .th-item {
      flex: 1;
      min-width: 100px;
      color: rgba(255, 255, 255, 0.3);

      /* Labels/L/Semibold */
      font-family: Sora;
      font-size: 16px;
      font-style: normal;
      font-weight: 600;
      line-height: 20px; /* 125% */

      &.date {
        min-width: 180px;
      }
    }
  }

  .item {
    display: flex;
    padding: 24px 0px;
    justify-content: space-between;
    align-items: center;
    align-self: stretch;
    gap: 100px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);

    .td {
      flex: 1;
      min-width: 100px;
      color: rgba(255, 255, 255, 0.85);

      /* Paragraphs/M/Light */
      font-family: Sora;
      font-size: 16px;
      font-style: normal;
      font-weight: 300;
      line-height: 24px; /* 150% */

      &.account {
        display: flex;
        align-items: center;
        gap: 8px;

        img {
          width: 24px;
          height: 24px;
          border-radius: 40px;
        }

        .name {
          color: rgba(255, 255, 255, 0.85);

          /* Paragraphs/M/Light */
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 300;
          line-height: 24px; /* 150% */
        }
      }

      &.symbol {
        color: #da4354;

        /* Paragraphs/M/Light */
        font-family: Sora;
        font-size: 16px;
        font-style: normal;
        font-weight: 300;
        line-height: 24px; /* 150% */
        text-transform: capitalize;
      }

      &.date {
        min-width: 180px;
      }

      &.transaction {
        color: #3fd9ff;
        cursor: pointer;
      }
    }
  }

  .flex-center {
    text-align: center !important;
  }

  .flex-end {
    text-align: right !important;
  }
}
</style>
