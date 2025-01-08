<script lang="ts" setup>
import { useWallet } from '@/hooks/useWallet'
import { useWalletStore } from '@/stores/wallet'
import type { AssetsToken, Position } from '@/types'
import { useAssetsStore } from '@/stores/assets'
import { useSocialStore } from '@/stores/social'

const { getMyPosition, getMineTokens } = useAssetsStore()

const wallet = useWallet()
const walletStore = useWalletStore()
const socialStore = useSocialStore()
const router = useRouter()

const disconnectWallet = () => {
  // 断开钱包连接
  wallet.disconnectWallet()
  router.push({ name: 'index' })
}

const showEditModal = ref(false)

const fansCount = ref(0)
const followingCount = ref(0)
const activeTab = ref(0)
const tabItems = ref([
  {
    name: 0,
    label: 'Coins Held'
  },
  {
    name: 1,
    label: 'Coins Created'
  },
  {
    name: 2,
    label: 'Fans'
  },
  {
    name: 3,
    label: 'Following'
  }
])

const isLoading = ref(false)
const positions = ref<Position[]>([])
const tokens = ref<AssetsToken[]>([])

const init = async () => {
  try {
    updateSocialCount()
    if (activeTab.value === 0) {
      positions.value = await getMyPosition()
    } else if (activeTab.value === 1) {
      tokens.value = await getMineTokens()
    }
    isLoading.value = false
  } catch (error) {
    isLoading.value = false
    console.error(error)
  }
}

// 更新关注数和粉丝数
const updateSocialCount = async () => {
  try {
    isLoading.value = true
    const userId = walletStore.userInfo.id
    const { fansCount: fsNum, followingCount: flwingCount } =
      await socialStore.getFollowInfo(userId)
    fansCount.value = fsNum
    followingCount.value = flwingCount
    tabItems.value[2].label = `Fans(${fansCount.value})`
    tabItems.value[3].label = `Followed(${followingCount.value})`
  } catch (error) {
    console.error(error)
  }
}

// 监听tab切换，重新请求数据
watch(
  activeTab,
  async () => {
    // 未登录，则不请求接口
    if (!walletStore.accessToken) return

    init()
  },
  { immediate: true }
)

// 监听钱包地址变化，重新请求数据
watch(
  () => walletStore.accessToken,
  () => {
    walletStore.accessToken && init()
  }
)
</script>

<template>
  <div class="profile-view">
    <div class="header-wrapper">
      <div class="profile-left">
        <div class="profile-avatar">
          <img v-if="walletStore.userInfo.avatar" :src="walletStore.userInfo.avatar as string" />
        </div>
        <div class="wrapper">
          <div class="info__wrapper">
            <div class="info__name">
              <span>{{ walletStore.userInfo.name }}</span>
            </div>
            <SvgIcon name="edit" @click="showEditModal = true" />
          </div>
          <div class="wallet-wrapper">
            <div class="address">{{ walletStore.wallet.address }}</div>
            <a :href="`https://basescan.org/token/${walletStore.wallet.address}`" target="_blank">
              <SvgIcon name="scan"></SvgIcon>
              <span>View on EtherScan</span>
            </a>
          </div>
        </div>
      </div>
      <div class="button button-create button-disconnect" @click="disconnectWallet">
        Disconnect Wallet
      </div>
    </div>
    <div class="profile__tabs">
      <Tabs v-model:model-value="activeTab" :tab-items="tabItems"></Tabs>
    </div>
    <div class="epal__content" v-if="!isLoading">
      <template v-if="activeTab === 0">
        <div class="epal__card-list" v-if="positions.length">
          <PositionCard v-for="item in positions" :key="item.id" :position="item"></PositionCard>
        </div>
        <Empty v-else description="No Positions yet" />
      </template>
      <template v-if="activeTab === 1">
        <div class="epal__card-list" v-if="tokens.length">
          <EpalCard v-for="item in tokens" :key="item.id" :token="item"></EpalCard>
        </div>
        <Empty v-else description="No token has been created yet" />
      </template>
      <template v-if="activeTab === 2">
        <Friends
          v-if="fansCount"
          :account-id="walletStore.userInfo.id"
          :friend-type="'fans'"
          :show-follow="true"
          @after-follow="init"
        />
        <Empty v-else description="No Fans yet" />
      </template>
      <template v-if="activeTab === 3">
        <Friends
          v-if="followingCount"
          :account-id="walletStore.userInfo.id"
          :friend-type="'following'"
          :show-follow="false"
        />
        <Empty v-else description="No Followed yet" />
      </template>
    </div>
    <ProfileEditDialog v-model="showEditModal"></ProfileEditDialog>
  </div>
</template>

<style lang="scss" scoped>
.header-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: 40px;

  .profile-left {
    display: flex;
    align-items: center;
    gap: 32px;

    .profile-avatar {
      width: 120px;
      height: 120px;
      border-radius: 12px;
      background: #2471d9;
      overflow: hidden;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
      }
    }

    .wrapper {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      flex: 1;
      align-self: stretch;

      .info__wrapper {
        display: flex;
        align-items: center;
        gap: 16px;
        color: #fff;
        cursor: pointer;

        .info__name {
          font-size: 52px;
          font-style: normal;
          font-weight: 800;
          line-height: 64px; /* 123.077% */
        }

        .svg-icon {
          width: 40px;
          height: 40px;
        }
      }

      .wallet-wrapper {
        display: flex;
        height: 42px;
        padding: 0px 16px;
        align-items: center;
        gap: 24px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);

        .address {
          color: rgba(255, 255, 255, 0.3);

          /* Labels/L/Regular */
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 400;
          line-height: 20px; /* 125% */
        }

        a {
          display: flex;
          gap: 4px;
          color: rgba(255, 255, 255, 0.65);

          /* Labels/S/Regular */
          font-family: Sora;
          font-size: 12px;
          font-style: normal;
          font-weight: 400;
          line-height: 16px; /* 133.333% */
          text-decoration: none;

          .svg-icon {
            width: 16px;
            height: 16px;
          }

          &:hover {
            color: rgba(#fff, 0.85);
          }
        }
      }
    }
  }

  .button-disconnect {
    width: 172px;
    height: 36px;
    padding: 0px 12px;
    border-radius: 8px;
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.25);

    color: rgba(255, 255, 255, 0.3);

    /* Labels/M/Regular */
    font-size: 14px;
    line-height: 18px; /* 128.571% */

    &:hover {
      color: rgba(255, 255, 255, 0.5);
      border-color: rgba(255, 255, 255, 0.5);
    }
  }
}

.profile__tabs {
  display: flex;
  padding: 0px 40px;
  justify-content: flex-start;
  align-items: center;
  gap: 12px;
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
</style>
