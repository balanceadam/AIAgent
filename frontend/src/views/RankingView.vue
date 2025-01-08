<script setup lang="ts">
import type { AssetsToken, TokenParams } from '@/types'
import { useAssetsStore } from '@/stores/assets'
import { simpleNotify } from '@/utils'

const { getEpalTokenList } = useAssetsStore()

const activedTab = ref(0)

const params = ref<TokenParams>({
  bondingCurve: undefined,
  chain: null,
  ordering: '-marketValue',
  page: 1,
  size: 10
})

const tokens = ref<AssetsToken[]>([])

const tabTokenList = reactive<{ [key: string]: AssetsToken[] }>({
  '-marketValue': [],
  '-dayIncrease': [],
  '-dayTradingVolume': []
})

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
    tabTokenList[params.value.ordering as string] = await getEpalTokenList(params.value)
  } catch (error) {
    console.error(error)
    simpleNotify('Failed to fetch token list', 'fail')
  }
}

const handleToggle = (index: number) => {
  activedTab.value = index
  tokens.value = []
  switch (index) {
    case 1:
      params.value.ordering = '-marketValue'
      break
    case 2:
      params.value.ordering = '-dayIncrease'
      break
    case 3:
      params.value.ordering = '-dayTradingVolume'
      break
  }
}

const timeNow = ref(Date.now())

const init = async () => {
  try {
    tabTokenList[params.value.ordering as string] = await getEpalTokenList(params.value)
  } catch (error) {
    console.error(error)
    simpleNotify('Failed to fetch token list', 'fail')
  }
}

init()
</script>
<template>
  <div class="page-view">
    <div class="header">
      <div class="header-left">
        <div class="title">Fans Protocol Ranking</div>
        <div class="tabs">
          <div class="tab" :class="{ active: activedTab === 0 }" @click="handleToggle(0)">
            Market Cap Ranking
          </div>
          <div class="tab" :class="{ active: activedTab === 1 }" @click="handleToggle(1)">
            24H Price Increase
          </div>
          <div class="tab" :class="{ active: activedTab === 2 }" @click="handleToggle(2)">
            24H Trading Volume
          </div>
          <!-- <ChainSelect v-model="params.chain" :show-fee="false"></ChainSelect> -->
        </div>
        <div class="tips">
          <span v-if="activedTab === 0">Progress reaches 100%, token deploys on SunswapV2</span>
        </div>
      </div>
      <div class="header-right">
        <div class="wrapper">
          <SvgIcon name="updated"></SvgIcon>
          <div class="desc">
            The data was last updated<br />
            at
            {{
              Intl.DateTimeFormat('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                timeZone: 'Asia/Shanghai',
                hour12: false
              }).format(timeNow) + ' (UTC+8)'
            }}
          </div>
        </div>
      </div>
    </div>
    <div class="list">
      <div class="column">
        <RankingItemComplex
          v-for="(token, index) in tabTokenList[params.ordering as string].slice(0, 3)"
          :key="index"
          :token="token"
          :index="index"
        ></RankingItemComplex>
      </div>
      <div class="column">
        <RankingItemSimple
          v-for="(token, index) in tabTokenList[params.ordering as string].slice(
            3,
            tabTokenList[params.ordering as string].length
          )"
          :token="token"
          :index="index + 4"
          :current-tab="activedTab"
          :key="index"
        ></RankingItemSimple>
      </div>
    </div>
  </div>
</template>

<style>
.page-view {
  .header {
    display: flex;
    padding: 40px;
    justify-content: space-between;
    align-items: center;
    align-self: stretch;

    .header-left {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 24px;
      flex-shrink: 0;
      align-self: stretch;

      .title {
        color: #fff;
        font-family: Sora;
        font-size: 52px;
        font-style: normal;
        font-weight: 600;
        line-height: 64px; /* 123.077% */
      }

      .tabs {
        display: flex;
        align-items: center;

        .tab {
          display: flex;
          padding: 8px 16px;
          height: 38px;
          justify-content: center;
          align-items: center;
          border-radius: 40px;
          border: 1px solid transparent;
          cursor: pointer;

          /* Labels/M/Regular */
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 400;
          line-height: 20px; /* 125% */
          color: rgba(255, 255, 255, 0.3);
          will-change: border-color, color;
          transition:
            border-color 0.3s ease-in-out,
            color 0.3s ease-in-out;

          &:hover {
            color: rgba(255, 255, 255, 0.75);
          }

          &.active {
            border-color: rgba(255, 255, 255, 0.25);
            color: #fff;
          }
        }

        .select-wrapper {
          margin-left: 40px;
          width: 218px;
        }
      }

      .tips {
        height: 26px;
        span {
          color: #828282;
          text-shadow: 0px 0px 36.4px #000;

          /* Paragraphs/XS/Light */
          font-family: Sora;
          font-size: 12px;
          font-style: normal;
          font-weight: 300;
          line-height: 20px; /* 166.667% */
          opacity: 0.7;
        }
      }
    }

    .header-right {
      width: 238px;
      .wrapper {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 8px;
        flex: 1 0 0;
        align-self: stretch;

        .svg-icon {
          width: 100px;
          height: 100px;
          color: #fff;
        }

        .desc {
          color: rgba(255, 255, 255, 0.3);
          text-align: center;

          /* Paragraphs/XS/Light */
          font-family: Sora;
          font-size: 12px;
          font-style: normal;
          font-weight: 300;
          line-height: 20px; /* 166.667% */

          .svg-icon {
            color: #fff;
          }
        }
      }
    }
  }

  .list {
    display: flex;
    gap: 40px;
    padding: 0px 40px 40px 40px;

    .column {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }
  }
}
</style>
