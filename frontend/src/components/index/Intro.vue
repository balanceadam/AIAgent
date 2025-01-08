<script lang="ts" setup>
import { gsap } from 'gsap'
import { useRouter } from 'vue-router'
import { useWalletStore } from '@/stores/wallet'
import { useLaunchStore } from '@/stores/launch'
import SplitType from 'split-type'

const router = useRouter()
const walletStore = useWalletStore()
const launchStore = useLaunchStore()

const goToLaunch = () => {
  router.push('/launch')
}

const goToExplore = () => {
  router.push('/epal')
}

const introRef = ref()
const videoRef = ref()
onMounted(() => {
  const header = document.querySelector('.header') as HTMLElement
  const layout = document.getElementById('layout') as HTMLElement
  window.addEventListener('scroll', () => {
    nextTick(() => {
      const scrollHeight = window.scrollY
      const introHeight = introRef.value?.offsetHeight

      if (!introHeight) return

      if (scrollHeight > introHeight) {
        header.style.width = `${layout.clientWidth}px`
      } else {
        header.style.width = `${introRef.value.offsetWidth + 1}px`
      }
    })
  })

  window.addEventListener('resize', () => {
    nextTick(() => {
      const header = document.querySelector('.header') as HTMLElement
      const layout = document.getElementById('layout') as HTMLElement
      const offsetHeight = window.scrollY
      const introHeight = introRef.value?.offsetHeight

      if (!offsetHeight) return
      if (offsetHeight && offsetHeight > introHeight) {
        // 如果滚动高度大于 intro 的高度，则header设置宽度设置为100%
        header.style.width = `${layout.clientWidth}px`
        header.style.left = `${(window.innerWidth - layout.clientWidth) / 2}px`
      } else {
        // 否则，设置宽度为 intro 的宽度
        header.style.width = `${introRef.value.offsetWidth + 1}px`
        header.style.left = `${(window.innerWidth - layout.clientWidth) / 2}px`
      }
    })
  })

  const tl = gsap.timeline()
  const text = new SplitType('.intro .intro-wrapper .desc', { types: ['words'] })

  tl.from('.intro .title', {
    opacity: 0,
    x: -96.65,
    duration: 1,
    ease: 'circ.out',
    delay: 0.57
  })
    .from(
      text.words,
      {
        opacity: 0,
        duration: 0.77,
        ease: 'none',
        stagger: 0.05
      },
      '-=0.51'
    )
    .from(
      '.intro .action',
      {
        opacity: 0,
        y: '28',
        duration: 1,
        ease: 'circ.out'
      },
      '-=0.46'
    )
    .from(
      '.intro .services',
      {
        opacity: 0,
        y: '75',
        duration: 1,
        ease: 'circ.out'
      },
      '-=0.54'
    )
    .from(
      videoRef.value,
      {
        opacity: 0,
        duration: 1,
        ease: 'circ.out'
      },
      '<'
    )
})
</script>

<template>
  <div class="intro">
    <video
      class="video"
      ref="videoRef"
      src="@/assets/images/index/intro.mp4"
      preload="auto"
      :controls="false"
      :playbackRate="0.5"
      autoplay
      muted
      loop
      poster="@/assets/images/index/post.png"
    ></video>
    <div ref="introRef" class="intro-content">
      <div class="intro-wrapper">
        <div class="title">Get Ready to Buy Exclusive Fan Tokens</div>
        <div class="desc">
          Start with the most secure and user-friendly platform to buy and collect Fan Tokens.
          Explore over 1000 unique Epal Fan Clubs powered by Balance Labs.
        </div>
        <div class="action">
          <div class="button button-create" @click="goToExplore">
            <span>Explore</span>
            <SvgIcon name="arrow-right"></SvgIcon>
          </div>
          <div
            v-if="walletStore.accessToken && launchStore.isInWhitelist"
            class="button button-create button-more"
            @click="goToLaunch"
          >
            <span>Launch</span>
            <SvgIcon name="play"></SvgIcon>
          </div>
        </div>
      </div>
      <div class="services">
        <div class="tag">
          <div class="icon-wrapper">
            <SvgIcon name="content"></SvgIcon>
          </div>
          <div class="tag-wrapper">
            <div class="title">Connect wallet</div>
            <div class="desc">Easily connect your wallet from the main page.</div>
          </div>
        </div>
        <div class="tag">
          <div class="icon-wrapper">
            <SvgIcon name="rewards"></SvgIcon>
          </div>
          <div class="tag-wrapper">
            <div class="title">Collect Fan Tokens</div>
            <div class="desc">Acquire fan tokens effortlessly after connecting your wallet.</div>
          </div>
        </div>
        <div class="tag">
          <div class="icon-wrapper">
            <SvgIcon name="companion"></SvgIcon>
          </div>
          <div class="tag-wrapper">
            <div class="title">Earn Profits</div>
            <div class="desc">Receive rewards directly to your wallet.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.intro {
  position: relative;

  .video {
    position: absolute;
    right: -2px;
    width: auto;
    height: 1050px;
  }

  .intro-content {
    display: flex;
    width: 1186px;
    height: 1050px;
    padding: 240px 100px 0px 100px;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;
    flex-shrink: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(20px);

    .intro-wrapper {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      align-self: stretch;

      .title {
        color: #fff;
        font-family: Sora;
        font-size: 90px;
        font-style: normal;
        font-weight: 600;
        line-height: 124px; /* 137.778% */
      }

      .desc {
        margin-top: 24px;
        color: #fff;
        text-shadow: 0px 0px 36.4px #000;
        font-family: Sora;
        font-size: 20px;
        font-style: normal;
        font-weight: 300;
        line-height: 30px; /* 150% */
        opacity: 0.3;
      }

      .action {
        margin-top: 64px;
        display: flex;
        height: 56px;
        align-items: flex-start;
        gap: 24px;

        .button-create {
          width: 200px;
        }

        .button-more {
          border: 1px solid rgba(255, 255, 255, 0.3);
          background: transparent;
          color: #fff;
        }
      }
    }

    .services {
      display: flex;
      height: 150px;
      justify-content: space-between;
      align-items: center;
      align-self: stretch;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      gap: 40px;

      .tag {
        display: flex;
        align-items: center;
        gap: 8px;

        .icon-wrapper {
          display: flex;
          width: 40px;
          height: 40px;
          padding: 4px 0px;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          gap: 10px;
          flex-shrink: 0;

          .svg-icon {
            width: 30px;
            height: 30px;
            flex-shrink: 0;
          }
        }

        .tag-wrapper {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          gap: 4px;
          flex: 1 0 0;

          .title {
            color: #fff;
            font-family: Sora;
            font-size: 18px;
            font-style: normal;
            font-weight: 600;
            line-height: 16px; /* 88.889% */
            opacity: 0.85;
          }

          .desc {
            color: #fff;
            font-family: Sora;
            font-size: 10px;
            font-style: normal;
            font-weight: 400;
            line-height: 16px; /* 160% */
            opacity: 0.3;
          }
        }
      }
    }
  }
}

@media screen and (min-width: 1921px) {
  .intro {
    padding-right: 40px;

    .video {
      right: 40px;
    }

    .intro-content {
      width: calc(100% - 720px);
      padding: 240px 100px 0px 100px;

      .intro-wrapper {
        width: min(100%, 1352px);

        .desc {
          width: min(100%, 896px);
        }
      }
    }
  }
}

@media (max-width: 1920px) {
  .intro {
    .intro-content {
      width: clamp(945px, calc(1186px - 0.502 * (1920px - 100vw)), 1186px);
      padding: 240px clamp(64px, 4.44vw, 100px) 0px clamp(64px, 4.44vw, 100px);
    }
  }
}

@media (max-width: 1440px) {
  .intro {
    .intro-content {
      width: clamp(840px, calc(945px - 0.65625 * (1440px - 100vw)), 945px);
      padding: 240px clamp(40px, calc(64px - 0.15 * (1440px - 100vw)), 64px) 0px;
    }
  }
}

@media (max-width: 834px) {
  .intro {
    height: 1700px;
    padding-top: 780px;

    .video {
      top: -0px;
    }

    .intro-content {
      padding: 100px 24px 0;
      width: 100%;
      height: 920px;

      .intro-wrapper .desc {
        padding-right: 150px;
      }
    }
  }
}
</style>
