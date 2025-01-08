<script lang="ts" setup>
export type Direction = 'left' | 'right' | 'up' | 'down'

interface Props {
  direction?: Direction
  speed?: number
  isForceScroll?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  direction: 'left',
  speed: 60,
  isForceScroll: true
})

const contentStyle = reactive({
  '--animation-end': '',
  animation: ''
})

const marqueeRef = ref()
const contentRef = ref()

const setScrollAnimation = () => {
  // 获取文本滚动实际显示宽度高度以及滚动内容宽度高度
  let marqueeWidth = marqueeRef.value.offsetWidth
  let marqueeHeight = marqueeRef.value.offsetHeight
  let contentWidth = contentRef.value.offsetWidth
  let contentHeight = contentRef.value.offsetHeight

  // 不强制滚动判断内容是否超出，未超出则不滚动
  if (!props.isForceScroll) {
    if (props.direction === 'left' || props.direction === 'right') {
      if (contentWidth <= marqueeWidth) {
        contentStyle['--animation-end'] = ''
        contentStyle.animation = ''
        return
      }
    } else {
      if (contentWidth <= marqueeWidth) {
        contentStyle['--animation-end'] = ''
        contentStyle.animation = ''
        return
      }
    }
  }

  let scrollLength, time

  // 根据滚动方向来设置不同的滚动动画
  switch (props.direction) {
    case 'left':
      contentStyle['--animation-end'] = `-${contentWidth}px`
      scrollLength = contentWidth + marqueeWidth
      time = scrollLength / props.speed
      contentStyle.animation = `scroll-left linear ${time}s infinite`
      break
    case 'right':
      contentStyle['--animation-end'] = `-${contentWidth}px`
      scrollLength = contentWidth + marqueeWidth
      time = scrollLength / props.speed
      contentStyle.animation = `scroll-left linear ${time}s infinite reverse`
      break

    case 'up':
      contentStyle['--animation-end'] = `-${contentHeight}px`
      scrollLength = contentHeight + marqueeHeight
      time = scrollLength / props.speed
      contentStyle.animation = `scroll-up linear ${time}s infinite`
      break
    case 'down':
      contentStyle['--animation-end'] = `-${contentHeight}px`
      scrollLength = contentHeight + marqueeHeight
      time = scrollLength / props.speed
      contentStyle.animation = `scroll-up linear ${time}s infinite reverse`
      break
  }
}

onMounted(() => {
  setScrollAnimation()
})

onUpdated(() => {
  setScrollAnimation()
})
</script>

<template>
  <div class="marquee" ref="marqueeRef">
    <div class="content" ref="contentRef" :style="contentStyle">
      <slot></slot>
    </div>
  </div>
</template>

<style lang="scss">
@keyframes scroll-up {
  0% {
    top: 100%;
  }

  100% {
    top: var(--animation-end);
  }
}

@keyframes scroll-left {
  0% {
    left: 0;
  }

  100% {
    left: var(--animation-end);
  }
}
</style>
