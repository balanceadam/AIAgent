<script lang="ts" setup>
import type { AssetsToken } from '@/types'

interface Props {
  token: AssetsToken
}

defineProps<Props>()

const router = useRouter()
const handleClick = (id: number) => {
  router.push({ name: 'epal-detail', params: { id } })
}
</script>

<template>
  <div class="epal-card" @click="handleClick(token.id)">
    <div class="epal-card__info">
      <div class="img-wrapper">
        <img v-if="token.epal" :src="token.epal" alt="" />
        <img v-else src="https://picsum.photos/350/350" alt="" />
      </div>
      <div class="info-wrapper">
        <div class="name">
          {{ (token.epalName ?? '').replace(/([A-Z][a-z]*)([A-Z].*)/g, '$1 $2') }}
        </div>
        <div class="tags">
          <span
            class="tag"
            v-for="tag in token.labels
              ?.split('#')
              .filter((item) => !!item)
              .map((item) => item.trim())"
            :key="tag"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </div>
    <div class="epal-card__token">
      <div class="token-top">
        <div class="info">
          <div class="logo-wrapper">
            <img v-show="token.logo" :src="token.logo" alt="" />
            <SvgIcon :name="`${token.chain.symbol.toLowerCase()}-2`"></SvgIcon>
          </div>
          <div class="right-wrapper">
            <div class="name">{{ `$ ${token.ticker}` }}</div>
            <div class="token-price">
              <span class="label">Market Cap</span>
              <span class="value">{{ `$ ${+token.protocol.bondingCurve}` }}</span>
            </div>
          </div>
        </div>
        <div class="token-change">
          {{
            ` ${token.protocol.dayIncrease > 0 ? '+' : token.protocol.dayIncrease < 0 ? '-' : ''} ${(+token.protocol.dayIncrease).toFixed(2)}%`
          }}
        </div>
      </div>
      <div class="progress-wrapper">
        <div class="label">
          <span>bonding curve progress</span>
          <span>{{ `${(+token.protocol.bondingCurve).toFixed(2)}%` }}</span>
        </div>
        <n-progress
          type="line"
          :percentage="+token.protocol.bondingCurve"
          :show-indicator="false"
          color="#00A878"
          rail-color="rgba(0, 168, 120, 0.05)"
          :height="4"
        />
      </div>
      <div class="token-tags">
        <div class="token-tag" v-for="item in token.fillingServices" :key="item.id">
          <img :src="item.logo" />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.epal-card {
  display: flex;
  padding: 4px 0px 28px 0px;
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
  align-self: stretch;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  box-shadow: 0px 0px 1.9px 0px #080808;
  border: 1px solid transparent;
  overflow: hidden;
  cursor: pointer;
  will-change: border-color;
  transition: border-color 0.3s ease-out;

  &:hover {
    border-color: rgba(255, 255, 255, 0.28);
  }

  &:active {
    border-color: rgba(255, 255, 255, 0.55);
  }

  &__info {
    position: relative;
    display: flex;
    // padding: 0px 4px;
    align-items: center;
    align-self: stretch;

    .img-wrapper {
      position: relative;
      width: 100%;
      height: 304px;
      border-radius: 12px 12px;
      overflow: hidden;
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
      }

      &::after {
        content: '';
        position: absolute;
        left: 0;
        right: 0;
        height: 100%;
        opacity: 0.75;
        background: rgba(0, 0, 0, 0.5);
      }
    }

    .info-wrapper {
      position: absolute;
      bottom: 0;
      display: flex;
      width: 100%;
      padding: 0px 16px 16px 16px;
      flex-direction: column;
      align-items: flex-start;
      gap: 10px;

      .name {
        width: 159px;
        color: #fff;
        text-shadow: 0px 0px 3px #000;
        font-size: 36px;
        font-style: normal;
        font-weight: 800;
        line-height: 36px; /* 100% */
      }

      .tags {
        display: flex;
        align-items: center;
        gap: 8px;
        width: 100%;
        min-height: 22px;

        .tag {
          display: flex;
          height: 22px;
          padding: 0px 6px;
          justify-content: center;
          align-items: center;
          gap: 4px;
          border-radius: 4px;
          background: rgba(255, 255, 255, 0.03);
          backdrop-filter: blur(5px);
          color: #fff;
          text-shadow: 0px 0px 2.9px #000;
          font-size: 12px;
          font-style: normal;
          font-weight: 600;
          line-height: 16px; /* 133.333% */
          opacity: 0.65;
          text-transform: capitalize;
        }
      }
    }
  }

  &__token {
    display: flex;
    padding: 0px 12px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    align-self: stretch;

    .token-top {
      display: flex;
      align-items: center;
      width: 100%;
      justify-content: space-between;

      .info {
        display: flex;
        align-items: center;
        gap: 18px;

        .logo-wrapper {
          position: relative;
          width: 54px;
          height: 54px;
          flex-shrink: 0;

          img {
            object-fit: cover;
            object-position: center;
            width: 100%;
            height: 100%;
            box-shadow: 0px 0px 2.5px 0px #4d264c;
            border-radius: 100%;
          }

          .svg-icon {
            position: absolute;
            right: -6px;
            top: -6px;
            width: 24px;
            height: 24px;
          }
        }

        .name {
          color: #fff;
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 600;
          line-height: 20px; /* 125% */
        }

        .token-price {
          margin-top: 2px;
          display: flex;
          flex-direction: column;

          .label {
            color: #828282;
            font-family: Sora;
            font-size: 10px;
            font-style: normal;
            font-weight: 400;
            line-height: 16px; /* 160% */
          }

          .value {
            color: #fff;
            font-family: Sora;
            font-size: 10px;
            font-style: normal;
            font-weight: 600;
            line-height: 20px; /* 200% */
          }
        }
      }

      .token-change {
        display: flex;
        min-width: 60px;
        height: 28px;
        padding: 4px 8px;
        justify-content: center;
        align-items: center;
        border-radius: 40px;
        background: rgba(0, 168, 120, 0.05);
        box-shadow: 0px 0px 5.4px 0px rgba(14, 14, 14, 0.39);
        color: var(--BL-green, #00a878);
        text-shadow: 0px 0px 0.6px #00a878;
        font-family: Sora;
        font-size: 12px;
        font-style: normal;
        font-weight: 600;
        line-height: 20px; /* 166.667% */
      }
    }

    .progress-wrapper {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      width: 100%;
      gap: 8px;
      align-self: stretch;

      .label {
        display: flex;
        align-items: center;
        gap: 8px;

        span {
          display: block;

          &:first-child {
            color: #fff;
            text-shadow: 0px 0px 0.5px #828282;
            font-family: Sora;
            font-size: 12px;
            font-style: normal;
            font-weight: 400;
            line-height: 20px; /* 166.667% */
            opacity: 0.5;
          }

          &:last-child {
            color: #00a878;
            text-shadow: 0px 0px 0.6px #00a878;
            font-family: Sora;
            font-size: 12px;
            font-style: normal;
            font-weight: 600;
            line-height: 16px; /* 133.333% */
          }
        }
      }
    }

    .token-tags {
      display: flex;
      align-items: center;
      gap: 8px;

      .token-tag {
        display: flex;
        padding: 6px;
        justify-content: center;
        align-items: center;
        border-radius: 4px;
        background: rgba(255, 255, 255, 0.03);
        width: 24px;
        height: 24px;

        img {
          width: 100%;
          height: 100%;
          object-fit: contain;
          object-position: center;
          fill: #fff;
          opacity: 0.3;
          filter: drop-shadow(0px 0px 1px #555);
        }
      }
    }
  }
}
</style>
