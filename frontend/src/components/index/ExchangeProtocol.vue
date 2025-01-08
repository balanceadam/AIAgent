<script lang="ts" setup>
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { useRouter } from 'vue-router'
import SplitType from 'split-type'

gsap.registerPlugin(ScrollTrigger)

const router = useRouter()
const goToExplore = () => {
  router.push('/epal')
}

onMounted(() => {
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: '.exchange-protocol',
      start: 'top 300px'
    }
  })

  const text = new SplitType('.exchange-protocol .desc', { types: ['words'] })

  tl.from('.exchange-protocol .title', {
    opacity: 0,
    y: 99,
    duration: 0.8,
    ease: 'circ.out'
  })
    .from(
      text.words,
      {
        opacity: 0,
        duration: 0.38,
        ease: 'none',
        stagger: 0.05
      },
      '-=0.21'
    )
    .from(
      '.exchange-protocol .button',
      {
        opacity: 0,
        y: 28,
        duration: 0.8,
        ease: 'circ.out'
      },
      '-=0.26'
    )
    .from(
      '.exchange-protocol .card',
      {
        opacity: 0,
        y: 168,
        duration: 0.8,
        ease: 'circ.out',
        stagger: 0.49
      },
      '-=0.54'
    )
})
</script>

<template>
  <div class="exchange-protocol">
    <div class="intro-wrapper">
      <div class="title">All-in-One Epal FT Exchange Protocol</div>
      <div class="desc">
        Seamlessly trade fan tokens with dynamic pricing, powered by veAMM for optimal liquidity and
        user engagement.
      </div>
    </div>
    <div class="button button-create" @click="goToExplore">
      <span>Explore</span>
      <SvgIcon name="arrow-right"></SvgIcon>
    </div>
    <div class="card-list">
      <div class="card">
        <div class="icon-wrapper">
          <SvgIcon name="exchange"></SvgIcon>
        </div>

        <div class="intro-wrapper">
          <div class="intro-title">Fan Token Exchange</div>
          <div class="intro-desc">
            Facilitating seamless trading of Fan Tokens, ensuring liquidity and preserving value.
          </div>
        </div>
      </div>
      <div class="card">
        <div class="icon-wrapper">
          <SvgIcon name="secure"></SvgIcon>
        </div>

        <div class="intro-wrapper">
          <div class="intro-title">Secure Trading Environment</div>
          <div class="intro-desc">
            Providing a transparent, secure space for transactions, empowering fans and investors to
            make informed decisions.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.exchange-protocol {
  margin-top: 160px;
  display: flex;
  width: 100%;
  min-height: 1050px;
  padding: 40px 100px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 80px;
  flex-shrink: 0;

  .intro-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
    align-self: stretch;

    .title {
      padding: 0 100px;
      color: #fff;
      text-align: center;
      text-shadow: 0px 0px 1px #fff;
      font-family: Sora;
      font-size: 90px;
      font-style: normal;
      font-weight: 600;
      line-height: 124.8px; /* 138.667% */
    }

    .desc {
      padding: 0 15px;
      max-width: 725px;
      color: #fff;
      text-align: center;
      text-shadow: 0px 0px 36.4px #000;
      font-family: Sora;
      font-size: 22px;
      font-style: normal;
      font-weight: 300;
      line-height: 30px; /* 136.364% */
      opacity: 0.3;
    }
  }

  .button-create {
    width: 200px;
  }

  .card-list {
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 64px;
    align-self: stretch;

    .card {
      display: flex;
      padding: 32px;
      flex-direction: column;
      align-items: flex-start;
      flex: 1 0 0;
      gap: 56px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.03);

      .icon-wrapper {
        display: flex;
        width: 96px;
        height: 96px;
        justify-content: center;
        align-items: center;
        gap: 10px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.03);

        .svg-icon {
          width: 56px;
          height: 56px;
          flex-shrink: 0;
        }
      }

      .intro-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 24px;
        align-self: stretch;

        .intro-title {
          color: #fff;
          font-family: Sora;
          font-size: 32px;
          font-style: normal;
          font-weight: 400;
          line-height: 40px; /* 125% */
          opacity: 0.85;
        }

        .intro-desc {
          // width: 564px;
          color: #fff;
          text-align: left;
          text-shadow: 0px 0px 36.4px #000;
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 300;
          line-height: 28px; /* 175% */
          opacity: 0.3;
        }
      }
    }
  }
}

@media screen and (max-width: 1920px) {
  .exchange-protocol {
    padding: clamp(64px, 5.208vw, 100px);
  }
}

@media screen and (max-width: 1440px) {
  .exchange-protocol {
    padding: clamp(40px, 4.444vw, 64px);
  }
}

@media screen and (max-width: 1280px) {
  .exchange-protocol {
    padding: clamp(24px, 3.125vw, 40px);
  }
}

@media screen and (max-width: 834px) {
  .exchange-protocol {
    margin-top: 160px;
    padding: 24px;
  }
}

@media screen and (max-width: 728px) {
  .card-list {
    flex-direction: column;
  }
}
</style>
