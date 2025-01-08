<script lang="ts" setup>
import { gsap } from 'gsap'

const router = useRouter()
const goTo = (path: string) => {
  if (path === '/docs') {
    window.open('https://balancefun.gitbook.io/balance')
    return
  }
  router.push(path)
}

const initAnimation = () => {
  gsap
    .timeline()
    .from('.header', {
      opacity: 0,
      y: -30,
      duration: 1,
      ease: 'power1.inOut'
    })
    .from(
      '.right',
      {
        opacity: 0,
        duration: 1,
        ease: 'power1.inOut'
      },
      '-=0.2'
    )
}

onMounted(() => {
  initAnimation()
})
</script>

<template>
  <div class="header">
    <div class="band-wrapper">
      <svg-icon name="logo" class="logo" />
    </div>

    <div class="right">
      <nav class="nav-menu">
        <div class="nav-item" @click="goTo('/epal')">Epal Space</div>
        <div class="nav-item" @click="goTo('/ranking')">Ranking</div>
        <div class="nav-item" @click="goTo('/earn')">Earn</div>
        <div class="nav-item" @click="goTo('/docs')">Docs</div>
      </nav>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.header {
  position: fixed;
  display: flex;
  width: 1186px;
  height: 72px;
  padding-left: 100px;
  row-gap: 40px;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  color: var(--color-text-primary);
  backdrop-filter: blur(20px);
  z-index: 9;

  .band-wrapper {
    width: 139.5px;
    height: 39.997px;
    flex-shrink: 0;

    .svg-icon {
      width: 100%;
      height: 100%;
    }
  }

  .right {
    display: flex;
    color: rgba(255, 255, 255, 0.3);
    flex-shrink: 0;

    .nav-menu {
      display: flex;
      padding: 0px 40px;
      justify-content: space-between;
      align-items: center;
      width: 500px;

      .nav-item {
        display: flex;
        min-width: 80px;
        justify-content: center;
        align-items: center;
        gap: 4px;
        flex-shrink: 0;
        cursor: pointer;

        &:hover {
          color: rgba(255, 255, 255, 0.85);
        }

        &:active {
          color: rgba(255, 255, 255, 0.85);
        }
      }
    }
  }

  @media (max-width: 1920px) {
    width: clamp(945px, calc(1186px - 0.502 * (1920px - 100vw)), 1186px);
    padding-left: clamp(64px, 4.44vw, 100px);
  }

  @media (max-width: 1440px) {
    width: clamp(840px, calc(945px - 0.65625 * (1440px - 100vw)), 945px);
    padding-left: clamp(40px, calc(64px - 0.15 * (1440px - 100vw)), 64px);
  }
}
</style>
