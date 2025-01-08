<script setup lang="ts">
import EpalDetail from '@/components/EpalDetail.vue'
import { useAssetsStore } from '@/stores/assets'
import { useWalletStore } from '@/stores/wallet'
import type { AssetsToken } from '@/types'

const assetsStore = useAssetsStore()
const walletStore = useWalletStore()

const isLoading = ref(true)
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

const activeTab = ref(1)
const tabItems = [
  {
    name: 0,
    label: 'Epal'
  },
  {
    name: 1,
    label: 'Fan Tokens'
  },
  {
    name: 2,
    label: 'Fans(0)'
  },
  {
    name: 3,
    label: 'Followed(0)'
  }
]

watch(
  () => walletStore.accessToken,
  async (newV) => {
    if (newV) {
      isLoading.value = true
      const tokens = await assetsStore.getMineTokens()
      if (tokens[0]) token.value = tokens[0]
      isLoading.value = false
    }
  },
  { immediate: true }
)
</script>
<template>
  <div class="me-view" v-if="!isLoading">
    <EpalDetail v-if="token.logo" :token="token"></EpalDetail>
    <div class="me-view__empty" v-else>
      <div class="header-wrapper">
        <n-breadcrumb
          separator=">"
          style="
            --n-item-text-color: rgba(255, 255, 255, 0.3);
            --n-item-text-color-active: rgba(255, 255, 255, 0.85);
            --n-item-text-color-hover: rgba(255, 255, 255, 0.3);
            --n-item-text-color-pressed: rgba(255, 255, 255, 0.3);
          "
        >
          <n-breadcrumb-item :clickable="false"> Me </n-breadcrumb-item>
          <n-breadcrumb-item> -- </n-breadcrumb-item>
        </n-breadcrumb>
        <div class="me-view__empty-info">
          <div class="user-info">
            <div class="user-info__avatar">
              <SvgIcon name="default-avatar"></SvgIcon>
            </div>
            <div class="info-wrapper">
              <div class="name">--</div>
              <div class="desc">--</div>
              <div class="social"></div>
            </div>
          </div>
          <div class="token">
            <div class="top-wrapper">
              <div class="top-left">
                <div class="logo-wrapper">
                  <div class="tag"></div>
                  <div class="avatar">
                    <SvgIcon name="default-token"></SvgIcon>
                  </div>
                </div>
                <div class="name-wrapper">
                  <div class="name">--</div>
                  <div class="ticker">--</div>
                </div>
              </div>
              <div class="top-center">
                <div class="name">--</div>
                <div class="ticker">--</div>
              </div>
              <div class="top-right">
                <div class="avatar">--</div>
              </div>
            </div>
            <div class="center-wrapper">--</div>
            <div class="bottom-wrapper">--</div>
          </div>
        </div>
      </div>
      <div class="me__tabs">
        <Tabs v-model:model-value="activeTab" :tab-items="tabItems"></Tabs>
      </div>
      <div class="content">
        <div class="no-data">
          <!-- <SvgIcon name="no-data"></SvgIcon> -->
          <img src="@/assets/images/no-data.svg" />
          <div class="text">No token has been created yet</div>
        </div>
      </div>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.header-wrapper {
  display: flex;
  padding: 40px;
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
  align-self: stretch;

  .me-view__empty-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    align-self: stretch;

    .user-info {
      display: flex;
      align-items: center;
      gap: 32px;

      &__avatar {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 192px;
        height: 192px;
        background: #ffffff26;
        border-radius: 12px;

        .svg-icon {
          width: 128px;
          height: 128px;
          flex-shrink: 0;
        }
      }

      .name {
        color: #fff;
        font-size: 52px;
        font-style: normal;
        font-weight: 800;
        line-height: 64px; /* 123.077% */
      }

      .desc {
        margin-top: 16px;
        display: flex;
        height: 32px;
        padding: 8px;
        justify-content: center;
        align-items: center;
        border-radius: 4px;
        background: var(--icon, rgba(255, 255, 255, 0.05));
        box-shadow: 0px 0px 3.8px 0px rgba(0, 0, 0, 0.2);
      }
      .social {
        margin-top: 32px;
        display: flex;
        width: 24px;
        height: 24px;
        padding: 3.75px 3px;
        justify-content: center;
        align-items: center;
      }
    }
  }

  .token {
    display: flex;
    width: 670px;
    padding: 16px 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.03);

    .top-wrapper {
      display: flex;
      justify-content: space-between;
      align-items: center;
      align-self: stretch;

      .top-left {
        display: flex;
        align-items: center;
        gap: 12px;

        .logo-wrapper {
          position: relative;
          display: flex;
          align-items: flex-end;
          width: 60px;
          height: 60px;

          .avatar {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 54px;
            height: 54px;
            background: #ffffff26;
            border-radius: 100%;

            .svg-icon {
              width: 24px;
              height: 24px;
            }
          }

          .tag {
            position: absolute;
            right: 0;
            top: 0;
            width: 24px;
            height: 24px;
            background: #050505;
            border-radius: 100%;
          }
        }

        .name-wrapper {
          color: rgba(255, 255, 255, 0.3);
          text-shadow: 0px 0px 36.4px #000;

          /* Paragraphs/S/Regular */
          font-family: Sora;
          font-size: 14px;
          font-style: normal;
          font-weight: 400;
          line-height: 22px; /* 157.143% */
          opacity: 0.7;

          .ticker {
            color: var(--GB-GB-White, #fff);
            text-shadow: 0px 0px 36.4px #000;
            font-size: 20px;
            font-style: normal;
            font-weight: 400;
            line-height: 28px; /* 140% */
          }
        }
      }

      .top-center {
        width: 123px;

        .name {
          color: rgba(255, 255, 255, 0.3);
          text-shadow: 0px 0px 36.4px #000;

          /* Paragraphs/S/Regular */
          font-family: Sora;
          font-size: 14px;
          font-style: normal;
          font-weight: 400;
          line-height: 22px; /* 157.143% */
        }

        .ticker {
          color: var(--GB-GB-White, #fff);
          text-shadow: 0px 0px 36.4px #000;
          font-family: Sora;
          font-size: 20px;
          font-style: normal;
          font-weight: 400;
          line-height: 28px; /* 140% */
        }
      }

      .top-right {
        display: flex;
        padding: 8px;
        width: 36px;
        height: 36px;
        justify-content: center;
        align-items: center;
        border-radius: 40px;
        background: var(--BL-green-BG, rgba(0, 168, 120, 0.05));
        box-shadow: 0px 0px 5.4px 0px rgba(14, 14, 14, 0.39);
        flex-shrink: 0;
        color: var(--BL-green, #00a878);
        text-shadow: 0px 0px 15.5px rgba(0, 0, 0, 0.5);
        font-family: Sora;
        font-size: 16px;
        font-style: normal;
        font-weight: 600;
        line-height: 20px; /* 125% */
      }
    }

    .center-wrapper {
      margin-top: 12px;
      color: rgba(255, 255, 255, 0.3);
      text-shadow: 0px 0px 36.4px #000;

      /* Paragraphs/XS/Light */
      font-family: Sora;
      font-size: 12px;
      font-style: normal;
      font-weight: 300;
      line-height: 20px; /* 166.667% */
      opacity: 0.7;
    }

    .bottom-wrapper {
      display: flex;
      padding: 4px;
      align-items: center;
      gap: 6px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.03);
      color: #fff;
      text-shadow: 1px 1px 4px #0c0c0c;
      font-family: Sora;
      font-size: 14px;
      font-style: normal;
      font-weight: 400;
      line-height: 16px; /* 114.286% */
      opacity: 0.3;
    }
  }
}

.me__tabs {
  display: flex;
  padding: 0px 40px;
  justify-content: flex-start;
  align-items: center;
  gap: 12px;
}

.content {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  .no-data {
    margin-top: 180px;
    margin-bottom: 180px;
    display: flex;
    // width: 214px;
    flex-direction: column;
    align-items: center;
    gap: 24px;

    .svg-icon {
      width: 128px;
      height: 128px;
    }

    .text {
      color: rgba(255, 255, 255, 0.3);

      /* Labels/M/Light */
      font-family: Sora;
      font-size: 14px;
      font-style: normal;
      font-weight: 300;
      line-height: 18px; /* 128.571% */
    }
  }
}
</style>
