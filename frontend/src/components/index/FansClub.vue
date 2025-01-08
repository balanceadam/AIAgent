<script lang="ts" setup>
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SplitType from 'split-type'

import type { TokenParams, AssetsToken } from '@/types'
import { useAssetsStore } from '@/stores/assets'
import { simpleNotify } from '@/utils'

gsap.registerPlugin(ScrollTrigger)
const { getEpalTokenList } = useAssetsStore()

let tl: any = null
const tokens = ref<AssetsToken[]>([])
const params = ref<TokenParams>({
  bondingCurve: undefined,
  chain: null,
  ordering: 'marketValue',
  page: 1,
  size: 12
})

// 获取列表
const fetchTokenList = async () => {
  // fetch token list
  try {
    tokens.value = await getEpalTokenList(params.value)

    // 滚动动画
    nextTick(() => {
      const fansItems = fansRef.value.querySelectorAll('.item')
      tl.from(fansItems, {
        opacity: 0,
        x: 158,
        duration: 0.5,
        ease: 'curbic.out',
        stagger: 0.21
      })
    })
  } catch (error) {
    console.error(error)
    simpleNotify('Failed to fetch token list', 'fail')
  }
}

fetchTokenList()

const fansRef = ref()
onMounted(() => {
  tl = gsap.timeline({
    scrollTrigger: {
      trigger: '.fans-club',
      start: 'start 300px'
    }
  })

  const text = new SplitType('.fans-club .fans-info .desc', { types: ['words'] })

  tl.from('.fans-info .title', {
    opacity: 0,
    y: 44,
    duration: 1,
    ease: 'cubic.out'
  }).from(
    text.words,
    {
      opacity: 0,
      duration: 0.93,
      ease: 'none',
      stagger: 0.05
    },
    '-=0.69'
  )
})
</script>

<template>
  <div class="fans-club">
    <div class="fans-info">
      <div class="title">Explore Fans Club</div>
      <div class="desc">
        Engage with exclusive communities, unlock unique content, and participate in collaborative
        activities.
      </div>
    </div>
    <div ref="fansRef" class="fans-list">
      <EpalCard class="item" v-for="item in tokens" :key="item.id" :token="item"></EpalCard>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.fans-club {
  margin-top: 160px;
  display: flex;
  width: 100%;
  padding: 40px 100px;
  flex-direction: column;
  align-items: flex-start;
  gap: 80px;

  .fans-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
    align-self: stretch;

    .title {
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
      width: 725px;
      color: #fff;
      text-align: center;
      text-shadow: 0px 0px 0.5px #4c4c4c;
      font-family: Sora;
      font-size: 20px;
      font-style: normal;
      font-weight: 300;
      line-height: 30px; /* 150% */
      opacity: 0.3;
    }
  }

  .fans-list {
    display: grid;
    width: 100%;
    row-gap: 40px;
    column-gap: 40px;
    justify-content: center;

    @media (min-width: 640px) {
      grid-template-columns: repeat(1, minmax(290px, 1fr));
    }
    @media (min-width: 668px) {
      grid-template-columns: repeat(2, minmax(290px, 1fr));
    }
    @media (min-width: 1030px) {
      grid-template-columns: repeat(3, minmax(290px, 1fr));
    }

    @media (min-width: 1408px) {
      grid-template-columns: repeat(4, minmax(290px, 1fr));
    }

    @media (min-width: 1810px) {
      grid-template-columns: repeat(5, minmax(290px, 1fr));
    }

    @media (min-width: 2224px) {
      grid-template-columns: repeat(6, minmax(290px, 1fr));
    }

    @media (min-width: 2568px) {
      grid-template-columns: repeat(7, minmax(290px, 1fr));
    }
  }
}

@media screen and (max-width: 1920px) {
  .fans-club {
    padding: clamp(64px, 5.208vw, 100px);
  }
}

@media screen and (max-width: 1440px) {
  .fans-club {
    padding: clamp(40px, 4.444vw, 64px);
  }
}

@media screen and (max-width: 1280px) {
  .fans-club {
    padding: clamp(24px, 3.125vw, 40px);
  }
}

@media screen and (max-width: 834px) {
  .fans-club {
    margin-top: 160px;
    padding: 24px;
  }
}
</style>
