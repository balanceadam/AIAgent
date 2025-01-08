<script lang="ts" setup>
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SplitType from 'split-type'

gsap.registerPlugin(ScrollTrigger)

onMounted(() => {
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: '.fans-protocol',
      start: 'start 50%'
    }
  })

  const text = new SplitType('.intro-wrapper .intro-right .desc', { types: ['words'] })

  tl.from('.intro-wrapper .intro-left .card:nth-child(1)', {
    opacity: 0,
    x: -147,
    duration: 0.8,
    ease: 'circ.out'
  })
    .from(
      '.intro-wrapper .intro-left .card:nth-child(1) .title',
      {
        opacity: 0,
        x: -147,
        duration: 0.8,
        ease: 'circ.out'
      },
      '<'
    )
    .from(
      '.intro-wrapper .intro-left .card:nth-child(1) .desc',
      {
        opacity: 0,
        duration: 0.73,
        ease: 'circ.out'
      },
      '<-=0.07'
    )
    .from(
      '.intro-wrapper .intro-left .card:nth-child(2)',
      {
        opacity: 0,
        x: 148,
        duration: 1,
        ease: 'circ.out'
      },
      '<'
    )
    .from(
      '.intro-wrapper .intro-right .title',
      {
        opacity: 0,
        x: -94,
        duration: 1,
        ease: 'circ.out'
      },
      '-=0.15'
    )
    .from(
      text.words,
      {
        opacity: 0,
        duration: 0.89,
        ease: 'none',
        stagger: 0.05
      },
      '-=0.79'
    )
    .from(
      '.fans-protocol .image-wrapper',
      {
        opacity: 0,
        x: '10%',
        y: '10%',
        duration: 0.5,
        ease: 'none'
      },
      '-=0.43'
    )
})
</script>

<template>
  <div class="fans-protocol">
    <div class="image-wrapper">
      <img src="@/assets/images/index/bg-fans.png" alt="" />
    </div>
    <div class="intro-wrapper">
      <div class="intro-left">
        <div class="card">
          <div class="line"></div>
          <div class="title">Launch and Management Platform</div>
          <div class="desc">
            This platform empowers Epals to launch and manage Fan Tokens, fostering deeper community
            participation and engagement.
          </div>
        </div>
        <div class="card">
          <div class="line"></div>
          <div class="title">Fair Revenue Sharing</div>
          <div class="desc">
            The protocol guarantees transparent and fair revenue sharing among creators and
            contributors, rewarding meaningful activities.
          </div>
        </div>
      </div>
      <div class="intro-right">
        <div class="title">What is Epal Fans Protocol</div>
        <div class="desc">
          Empower game companions to create, manage, and trade personalized fan tokens effortlessly.
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.fans-protocol {
  position: relative;
  width: 100%;
  // height: 1020px;
  padding-top: 180px;

  .image-wrapper {
    position: absolute;
    top: 100px;
    right: 40px;
    width: clamp(450px, 48.23vw, 926px);

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
    }
  }

  .intro-wrapper {
    // margin-top: 100px;
    width: 100%;
    height: 800px;
    padding: 80px clamp(64px, calc(80px - 0.075 * (1920px - 100vw)), 100px);
    display: flex;
    align-items: center;
    align-self: stretch;
    justify-content: space-between;

    .intro-left {
      position: relative;
      width: clamp(600px, 41.771vw, 802px);
      height: clamp(540px, calc(540px + 0.296 * (1920px - 100vw)), 682px);
      flex-shrink: 0;

      .card {
        display: flex;
        width: clamp(380px, calc(580px - 0.4167 * (1920px - 100vw)), 580px);
        height: clamp(294px, calc(294px + 0.296 * (1920px - 100vw)), 362px);
        padding: 32px;
        flex-direction: column;
        justify-content: flex-end;
        align-items: flex-start;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);

        .line {
          width: 66px;
          height: 3px;
          border-radius: 3px;
          opacity: 0.1;
          background: #fff;
          box-shadow: 0px 0px 36.4px 0px #000;
        }

        .title {
          margin-top: 39px;
          color: #fff;
          font-family: Sora;
          font-size: 32px;
          font-style: normal;
          font-weight: 400;
          line-height: 40px; /* 125% */
          opacity: 0.85;
        }

        .desc {
          margin-top: 24px;
          // padding-right: 80px;
          width: min(100%, 435px);
          color: #fff;
          text-shadow: 0px 0px 36.4px #000;
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 300;
          line-height: 28px; /* 175% */
          opacity: 0.3;
        }

        &:last-child {
          position: absolute;
          bottom: 0;
          right: 0;

          .title {
            margin-top: 80px;
          }
        }

        &:first-child {
          position: absolute;
          top: 0;
          left: 0;
          z-index: 1;
        }
      }
    }

    .intro-right {
      display: flex;
      width: clamp(652px, 40.36vw, 775px);
      height: clamp(456px, calc(540px + 0.296 * (1920px - 100vw)), 682px);
      flex-direction: column;
      align-items: flex-start;
      justify-content: center;
      gap: 24px;

      .title {
        color: #fff;
        font-family: Sora;
        font-size: 90px;
        font-style: normal;
        font-weight: 600;
        line-height: 117px; /* 130% */
      }

      .desc {
        width: min(100%, 725px);
        color: #fff;
        text-shadow: 0px 0px 36.4px #000;
        font-family: Sora;
        font-size: 20px;
        font-style: normal;
        font-weight: 300;
        line-height: 30px; /* 150% */
        opacity: 0.3;
      }
    }
  }
}

@media (max-width: 1440px) {
  .fans-protocol .intro-wrapper {
    padding: 80px clamp(40px, calc(64px - 0.15 * (1440px - 100vw)), 64px);
    .intro-right {
      width: auto;
      margin-left: 80px;
    }
  }
}
@media (max-width: 1280px) {
  .fans-protocol .intro-wrapper {
    padding: 80px clamp(24px, calc(40px - 0.0359 * (1280px - 100vw)), 40px);
    .intro-right {
      width: auto;
      margin-left: clamp(40px, calc(80px - 0.3 * (1280px - 100vw)), 80px);
    }
  }
}

@media (max-width: 1114px) {
  .fans-protocol {
    padding-top: 324px;

    .image-wrapper {
      position: absolute;
      top: 100px;
      right: 40px;
      width: 926px;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
      }
    }

    .intro-wrapper {
      padding: 0 24px;
      flex-direction: column-reverse;
      gap: 160px;
      height: auto;

      .intro-left {
        margin-top: 0;
        width: 786px;
        height: 540px;

        .card {
          width: 580px;
          height: 294px;
        }
      }

      .intro-right {
        margin-left: 0;
        height: auto;

        .title {
          text-align: center;
        }

        .desc {
          text-align: center;
        }
      }
    }
  }
}

@media (max-width: 834px) {
  .fans-protocol .intro-wrapper .intro-left {
    width: 100%;
    height: clamp(540px, calc(540px + 0.296 * (834px - 100vw)), 682px);

    .card {
      width: clamp(380px, calc(580px - 0.4167 * (834px - 100vw)), 580px);
      height: clamp(294px, calc(294px + 0.296 * (834px - 100vw)), 362px);
    }
  }
}
</style>
