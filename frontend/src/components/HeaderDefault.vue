<script lang="ts" setup>
import { useWalletStore } from '@/stores/wallet'
import { formatAddress } from '@/utils/index'

const walletStore = useWalletStore()

const router = useRouter()
const goToIndex = () => {
  router.push({ name: 'index' })
}

const showProfileModal = ref(false)

const showWalletModal = ref(false)
</script>

<template>
  <n-layout-header class="header" position="absolute">
    <div class="band-wrapper" @click="goToIndex">
      <svg-icon name="logo" class="logo" />
    </div>
    <div class="carousel">
      <!-- <Marquee direction="left" :is-force-scroll="false">
        <div class="list">
          <Remind action="create"></Remind>
          <Remind action="buy"></Remind>
          <Remind action="sold"></Remind>
          <Remind action="buy"></Remind>
        </div>
      </Marquee> -->
    </div>
    <div class="right">
      <template v-if="walletStore.wallet.address">
        <div class="wallet">
          <SvgIcon name="metamask" />
          <span>{{ formatAddress(walletStore.wallet.address) }}</span>
        </div>
        <RouterLink class="profile" to="/profile">Profile</RouterLink>
        <!-- <div class="profile" @click="showProfileModal = true">Profile</div>
        <ProfileDialog v-model="showProfileModal"></ProfileDialog> -->
      </template>
      <template v-else>
        <div class="button" @click="showWalletModal = true">
          <SvgIcon name="wallet" />
          <span>Connect Wallet</span>
        </div>
        <WalletDialog v-model="showWalletModal"></WalletDialog>
      </template>
    </div>
  </n-layout-header>
</template>

<style lang="scss" scoped>
.header {
  display: flex;
  width: 100%;
  height: 72px;
  padding: 0px 40px;
  row-gap: 40px;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  color: var(--color-text-primary);
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(7, 5, 19, 0.2);
  backdrop-filter: blur(20px);
  z-index: 999;

  .band-wrapper {
    width: 139.5px;
    height: 39.997px;
    flex-shrink: 0;
    cursor: pointer;

    .svg-icon {
      width: 100%;
      height: 100%;
    }
  }

  .carousel {
    margin-left: 40px;
    display: flex;
    width: 1020px;
    height: 100px;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex: 1;
    // border-right: 1px solid rgba(255, 255, 255, 0.15);
    // border-left: 1px solid rgba(255, 255, 255, 0.15);

    :deep(.marquee) {
      width: 100%;
      height: 100%;
      overflow: hidden;
      position: relative;
      display: flex;
      align-items: center;

      & > .content {
        width: fit-content;
        height: fit-content;
        position: absolute;
        white-space: nowrap;
      }
    }

    .list {
      display: flex;
      align-items: center;
      gap: 24px;
    }
  }

  .right {
    display: flex;
    color: var(--color-text-primary);
    flex-shrink: 0;
    padding-left: 40px;
    gap: 24px;

    .button {
      display: flex;
      width: 190px;
      height: 42px;
      justify-content: center;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
      color: var(--icon-Normal, #ededed);
      cursor: pointer;
      border-radius: 8px;
      border: 1px solid var(---Normal, rgba(255, 255, 255, 0.3));

      .svg-icon {
        width: 24px;
        height: 24px;
      }

      &:hover {
        opacity: 0.85;
      }

      &:active {
        opacity: 0.75;
      }
    }

    .wallet {
      display: flex;
      width: 190px;
      height: 42px;
      justify-content: center;
      align-items: center;
      gap: 8px;
      border-radius: 8px;
      border: 1px solid var(---Normal, rgba(255, 255, 255, 0.3));
      cursor: pointer;

      .svg-icon {
        width: 24px;
        height: 24px;
      }

      span {
        color: #888;

        /* Labels/L/Regular */
        font-family: Sora;
        font-size: 16px;
        font-style: normal;
        font-weight: 400;
        line-height: 20px; /* 125% */
      }
    }

    .profile {
      display: flex;
      height: 42px;
      padding: 0px 12px;
      justify-content: center;
      align-items: center;
      border-radius: 8px;
      border: 1px solid var(---Normal, rgba(255, 255, 255, 0.3));
      color: #888;
      cursor: pointer;
      text-decoration: none;

      /* Labels/L/Regular */
      font-family: Sora;
      font-size: 16px;
      font-style: normal;
      font-weight: 400;
      line-height: 20px; /* 125% */
    }
  }
}
</style>
