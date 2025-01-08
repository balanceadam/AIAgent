<script setup lang="ts">
import type { TokenParams, AssetsToken } from '@/types'
import { useAssetsStore } from '@/stores/assets'
import { simpleNotify } from '@/utils'

const { getEpalTokenList } = useAssetsStore()

const isLoading = ref(false)
const isTradingOnFan = ref(false)
const params = ref<TokenParams>({
  bondingCurve: undefined,
  chain: null,
  ordering: 'createdAt',
  page: 1,
  size: 100
})

const handleCheckedChange = (checked: boolean) => {
  params.value.bondingCurve = checked ? 100 : undefined
}

const tokens = ref<AssetsToken[]>([])

// 监听参数变化，如果变动，则更新列表
watch(
  () => params.value,
  () => {
    fetchTokenList()
  },
  {
    deep: true
  }
)

// 获取列表
const fetchTokenList = async () => {
  // fetch token list
  try {
    tokens.value = await getEpalTokenList(params.value)
  } catch (error) {
    console.error(error)
    simpleNotify('Failed to fetch token list', 'fail')
  }
}

// 刷新操作
const handleRefresh = () => {
  fetchTokenList()
}

const init = async () => {
  try {
    isLoading.value = true
    tokens.value = await getEpalTokenList(params.value)
    isLoading.value = false
  } catch (error) {
    isLoading.value = false
    console.error(error)
    simpleNotify('Failed to fetch token list', 'fail')
  }
}

init()
</script>

<template>
  <main class="epal-list-view">
    <div class="epal__header">
      <div class="epal__header-left">
        <FilterSelect v-model="params.ordering"></FilterSelect>
        <n-checkbox
          style="
            --n-color: transparent;
            --n-border: 1px solid rgba(255, 255, 255, 0.3);
            --n-border-focus: 1px solid rgba(255, 255, 255, 0.75);
            --n-border-checked: 1px solid rgba(255, 255, 255, 1);
            --n-color-checked: rgba(255, 255, 255, 1);
            --n-check-mark-color: #1e1e22;
            --n-text-color: rgba(255, 255, 255, 0.3);
            --n-size: 20px;
            --n-font-size: 16px;
          "
          v-model="isTradingOnFan"
          label="Trade on Trading Fan Protocol"
          @update:checked="handleCheckedChange"
        />
      </div>
      <div class="epal__header-right" @click="handleRefresh">
        <SvgIcon name="refresh"></SvgIcon>
      </div>
    </div>
    <div class="epal__content" v-if="!isLoading">
      <div v-if="tokens.length" class="epal__card-list">
        <EpalCard v-for="item in tokens" :key="item.id" :token="item"></EpalCard>
      </div>
      <Empty v-else description="No Epal yet" />
    </div>
  </main>
</template>
<style lang="scss" scoped>
.epal-list-view {
  padding: 40px;

  .epal__header {
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: center;

    &-left {
      display: flex;
      align-items: center;
      gap: 40px;

      .select {
        display: flex;
        width: 218px;
        height: 48px;
        padding: 0px 16px;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        border-radius: 40px;
        border: 1px solid var(---Normal, rgba(255, 255, 255, 0.25));
        background: rgba(255, 255, 255, 0.03);

        color: rgba(255, 255, 255, 0.3);

        /* Labels/L/Regular */
        font-family: Sora;
        font-size: 16px;
        font-style: normal;
        font-weight: 400;
        line-height: 20px; /* 125% */
      }
    }

    &-right {
      display: flex;
      width: 24px;
      height: 24px;
      justify-content: center;
      align-items: center;
      color: rgba(255, 255, 255, 0.3);
      border-radius: 4px;
      border: 1.5px solid rgba(255, 255, 255, 0.25);
      cursor: pointer;
      will-change: border-color, color, box-shadow, transform;
      transition:
        border-color 0.3s ease-out,
        color 0.3s ease-out,
        box-shadow 0.3s ease-out,
        transform 0.5s ease-out;

      &:hover {
        color: rgba(255, 255, 255, 0.28);
        border-color: rgba(255, 255, 255, 0.28);
        box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.1);
      }

      &:active {
        color: rgba(255, 255, 255, 0.5);
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.1);
        .svg-icon {
          transform: rotate(-30deg);
        }
      }
    }
  }

  ::v-deep(.n-checkbox--checked .n-checkbox__label) {
    color: #fff;
  }

  .epal__content {
    margin-top: 40px;

    .epal__card-list {
      display: grid;
      width: 100%;
      grid-template-columns: repeat(4, minmax(200px, 1fr));
      row-gap: 40px;
      column-gap: 16px;

      @media (min-width: 640px) {
        grid-template-columns: repeat(1, minmax(200px, 1fr));
      }
      @media (min-width: 780px) {
        grid-template-columns: repeat(2, minmax(200px, 1fr));
      }
      @media (min-width: 1024px) {
        grid-template-columns: repeat(3, minmax(200px, 1fr));
      }

      @media (min-width: 1280px) {
        grid-template-columns: repeat(4, minmax(200px, 1fr));
      }

      @media (min-width: 1440px) {
        grid-template-columns: repeat(5, minmax(200px, 1fr));
      }
    }
  }
}
</style>
