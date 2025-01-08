<script lang="ts" setup>
import { useWalletStore } from '@/stores/wallet'
import { useLaunchStore } from '@/stores/launch'

const router = useRouter()
const walletStore = useWalletStore()
const launchStore = useLaunchStore()

const isHoving = ref(false)
const goToLaunch = () => {
  router.push({ name: 'launch' })
}

const showWalletModal = ref(false)
const goToMe = () => {
  if (walletStore.accessToken) {
    router.push({ name: 'me' })
  } else {
    showWalletModal.value = true
  }
}
</script>

<template>
  <NLayout class="layout">
    <HeaderDefault></HeaderDefault>
    <NLayout has-sider position="absolute" style="top: 72px; bottom: 0; height: calc(100vh - 72px)">
      <NLayoutSider width="220px" style="background: #000" :native-scrollbar="false">
        <div class="nav-menu-wrapper">
          <div class="nav-list">
            <RouterLink
              class="nav-item"
              :class="{ active: $route.name === 'epal-list' || $route.name === 'epal-detail' }"
              to="/epal"
            >
              <SvgIcon
                v-if="$route.name === 'epal-list' || $route.name === 'epal-detail'"
                name="epal-active"
              />
              <SvgIcon v-else name="epal" />
              <span>Epal Space</span>
            </RouterLink>
            <RouterLink
              class="nav-item"
              :class="{ active: $route.name === 'ranking' }"
              to="/ranking"
            >
              <SvgIcon v-if="$route.name === 'ranking'" name="ranking-active" />
              <SvgIcon v-else name="ranking" />
              <span>Ranking</span>
            </RouterLink>
            <RouterLink class="nav-item" :class="{ active: $route.name === 'earn' }" to="/earn">
              <SvgIcon v-if="$route.name === 'earn'" name="earn-active" />
              <SvgIcon v-else name="earn" />
              <span>Earn</span>
            </RouterLink>
            <div
              class="nav-item"
              :class="{ active: $route.name === 'me' }"
              style="cursor: pointer"
              @click="goToMe"
            >
              <SvgIcon v-if="$route.name === 'me'" name="me-active" />
              <SvgIcon v-else name="me" />
              <span>Me</span>
            </div>
          </div>
        </div>
        <div class="side-wrapper">
          <div
            v-if="walletStore.accessToken && launchStore.isInWhitelist"
            class="launch-button"
            :class="{ active: $route.name === 'launch' }"
            @click="goToLaunch"
            @mouseenter="isHoving = true"
            @mouseleave="isHoving = false"
          >
            <SvgIcon v-if="!isHoving && $route.name !== 'launch'" name="launch"></SvgIcon>
            <SvgIcon v-else name="launch-hover"></SvgIcon>
            <span>Launch Now</span>
          </div>
          <div class="social">
            <a href="https://t.me/Balance_Fun" target="_blank" class="wrapper">
              <SvgIcon name="telegram"></SvgIcon>
            </a>
            <a href="https://discord.com/invite/balance-fun" target="_blank" class="wrapper">
              <SvgIcon name="discord"></SvgIcon>
            </a>
            <a href="https://x.com/Balance_Fun" target="_blank" class="wrapper">
              <SvgIcon name="x"></SvgIcon>
            </a>
          </div>
        </div>
      </NLayoutSider>
      <NLayoutContent :native-scrollbar="false">
        <RouterView />
      </NLayoutContent>
    </NLayout>
    <WalletDialog v-model="showWalletModal"></WalletDialog>
  </NLayout>
</template>

<style lang="scss" scoped>
.layout {
  // margin: 0 auto;
  width: 100%;
  height: 100vh;
}

.n-layout {
  background: #000;

  &-sider {
    display: flex;
    width: 221px;
    padding: 32px 0px;
    flex-direction: column;
    align-items: flex-start;
    gap: 80px;
    flex-shrink: 0;
    border-right: 1px solid rgba(255, 255, 255, 0.15);
    background: rgba(7, 5, 19, 0.2);
    backdrop-filter: blur(20px);

    :deep(.n-scrollbar-content) {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      height: 100%;
    }

    .nav-menu-wrapper {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
      align-self: stretch;

      .nav-list {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 24px;
        align-self: stretch;

        .nav-item {
          display: flex;
          align-items: center;
          width: 100%;
          height: 64px;
          padding-left: 40px;
          gap: 8px;
          text-decoration: none;
          color: rgba(237, 237, 237, 0.3);
          border-right: 1px solid transparent;
          will-change: border-color, color, background;
          transition:
            border-color 0.3s ease-out,
            color 0.3s ease-out,
            background 0.3s ease-out;

          .svg-icon {
            width: 24px;
            height: 24px;
          }

          span {
            /* Labels/L/Semibold */
            font-family: Sora;
            font-size: 16px;
            font-style: normal;
            font-weight: 600;
            line-height: 20px; /* 125% */
          }

          &:hover {
            color: rgba(237, 237, 237, 0.85);
            border-color: rgba(255, 255, 255, 0.1);
            background: linear-gradient(
              270deg,
              rgba(217, 217, 217, 0.1) 0%,
              rgba(217, 217, 217, 0) 1.32%
            );
          }

          &.active,
          &:active {
            color: #fff;
            border-right: 2px solid #fff;
            background: linear-gradient(
              270deg,
              rgba(217, 217, 217, 0.1) 0%,
              rgba(217, 217, 217, 0) 68.01%
            );
          }
        }
      }
    }

    .side-wrapper {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      min-height: 250px;

      .launch-button {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;

        width: 181px;
        height: 64px;
        flex-shrink: 0;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        color: #fff;

        /* Labels/L/Semibold */
        font-family: Sora;
        font-size: 16px;
        font-style: normal;
        font-weight: 600;
        line-height: 20px; /* 125% */

        cursor: pointer;

        .svg-icon {
          width: 30px;
          height: 30px;
          flex-shrink: 0;
        }

        &:hover,
        &.active {
          color: #1e1e22;
          background: #fff;
          box-shadow: 0px 0px 9.9px 0px #111;
        }
      }

      .social {
        margin-top: clamp(50px, 13.54vw, 80px);
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 24px;

        .wrapper {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          cursor: pointer;

          .svg-icon {
            width: 24px;
            height: 24px;
            color: #fff;

            &:hover {
              opacity: 0.85;
            }

            &:active {
              opacity: 0.75;
            }
          }
        }
      }
    }
  }
}
</style>
