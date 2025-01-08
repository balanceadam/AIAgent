<script lang="ts" setup>
import type { AssetsToken } from '@/types'

interface Props {
  index: number
  token: AssetsToken
}

const props = defineProps<Props>()

const indexMapping = ref<Record<number, string>>({
  0: 'first',
  1: 'second',
  2: 'third'
} as const)

const goToUrl = (url: string | undefined) => {
  if (url) window.open(url, '_blank')
}

const router = useRouter()
const handleClick = (id: number) => {
  router.push({ name: 'epal-detail', params: { id } })
}

const labels = ref<string[]>([])

if (props.token.labels) {
  props.token.labels?.split('#').forEach((label) => {
    if (label.length > 0) labels.value.push(label.trim())
  })
}
</script>

<template>
  <div class="ranking-item" @click="handleClick(token.id)">
    <div class="index">
      <SvgIcon :name="indexMapping[index]"></SvgIcon>
    </div>
    <div class="wrapper">
      <div class="top">
        <div class="info">
          <div class="avatar">
            <img :src="token.logo" alt="" />
          </div>
          <div>
            <div class="name">{{ token.name }}</div>
            <div class="tag-wrapper">
              <span class="tag" v-for="(l, i) in labels" :key="i">{{ l }}</span>
            </div>
          </div>
        </div>
        <div class="social">
          <div class="group">
            <SvgIcon name="x" @click.stop="goToUrl(token.twitter)"></SvgIcon>
            <SvgIcon name="telegram" @click.stop="goToUrl(token.telegram)"></SvgIcon>
            <SvgIcon name="website" @click.stop="goToUrl(token.website)"></SvgIcon>
          </div>
          <div class="user">
            <img :src="token.epal" alt="" />
            <div class="name">{{ token.epalName }}</div>
          </div>
        </div>
      </div>
      <div class="desc">
        {{ token.description }}
      </div>
      <div class="bottom">
        <div class="price">
          <div class="label">
            <span>Market cap(EPT)</span>
            <SvgIcon name="transfer"></SvgIcon>
          </div>
          <div class="value">
            <span class="num">{{ token.protocol.marketValue.toFixed(3) }}</span>
            <span class="percent">
              {{
                ` ${token.protocol.dayIncrease > 0 ? '+' : token.protocol.dayIncrease < 0 ? '-' : ''} ${(+token.protocol.dayIncrease).toFixed(2)}%`
              }}
            </span>
          </div>
        </div>
        <div class="bonding">
          <div class="label">BondingCurve%</div>
          <div class="value">
            <n-progress
              type="line"
              color="#00EBA8"
              :height="8"
              rail-color="rgba(255, 255, 255, 0.05)"
              :percentage="token.protocol.bondingCurve"
              indicator-text-color="#00EBA8"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.ranking-item {
  display: flex;
  height: 237px;
  padding: 16px;
  align-items: flex-start;
  gap: 16px;
  flex-shrink: 0;
  align-self: stretch;
  border-radius: 20px;
  border: 1px solid transparent;
  background: #101010;
  box-shadow: 0px 0px 19.2px 0px rgba(77, 77, 77, 0.06);
  cursor: pointer;
  will-change: border-color;
  transition: border-color 0.3s ease-out;

  &:hover {
    border-color: rgba(255, 255, 255, 0.28);
  }

  &:active {
    border-color: rgba(255, 255, 255, 0.5);
  }

  .index {
    display: flex;
    width: 56px;
    height: 56px;
    align-items: center;
    padding: 14px;

    .svg-icon {
      width: 28px;
      height: 40px;
      flex-shrink: 0;
    }
  }

  .wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    flex: 1;
    height: 100%;

    .top {
      display: flex;
      justify-content: space-between;

      .info {
        display: flex;
        gap: 20px;

        .avatar {
          width: 64px;
          height: 64px;
          border-radius: 6.4px;
          box-shadow:
            0px 0px 6.113px 0px rgba(0, 0, 0, 0.6),
            0px 0px 11.157px 0px rgba(77, 77, 77, 0.12);
          overflow: hidden;

          img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
          }
        }

        .name {
          color: #fff;
          text-shadow: 0px 0px 36.4px #000;

          /* H5/Regular */
          font-family: Sora;
          font-size: 24px;
          font-style: normal;
          font-weight: 400;
          line-height: 32px; /* 133.333% */
        }

        .tag-wrapper {
          margin-top: 12px;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .tag {
          display: flex;
          height: 22px;
          padding: 0px 6px;
          justify-content: center;
          align-items: center;
          gap: 4px;
          border-radius: 4px;
          background: #1d1d1d;
          backdrop-filter: blur(5px);
          color: #fff;
          text-shadow: 0px 0px 2.9px #000;
          font-size: 12px;
          font-style: normal;
          font-weight: 600;
          line-height: 16px; /* 133.333% */
          opacity: 0.65;
        }
      }

      .social {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: flex-end;
        align-self: stretch;

        .group {
          display: flex;
          height: 36px;
          align-items: center;
          gap: 10px;

          .svg-icon {
            width: 16px;
            height: 16px;
            color: #ededed;
            cursor: pointer;
          }
        }

        .user {
          display: flex;
          height: 32px;
          justify-content: flex-end;
          align-items: center;
          gap: 4px;

          img {
            width: 16px;
            height: 16px;
            flex-shrink: 0;
            border-radius: 8px;
          }

          .name {
            color: var(--icon-Normal, #ededed);
            text-shadow: 0px 0px 36.4px #000;

            /* Labels/S/Regular */
            font-family: Sora;
            font-size: 12px;
            font-style: normal;
            font-weight: 400;
            line-height: 16px; /* 133.333% */
          }
        }
      }
    }

    .desc {
      flex: 1;
      margin-top: 12px;
      color: rgba(255, 255, 255, 0.3);
      text-shadow: 0px 0px 36.4px #000;

      /* Paragraphs/XS/Light */
      font-family: Sora;
      font-size: 12px;
      font-style: normal;
      font-weight: 300;
      line-height: 20px; /* 166.667% */
      opacity: 0.7;
    }

    .bottom {
      margin-top: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;

      .price,
      .bonding {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .bonding {
        align-items: flex-end;
      }

      .label {
        display: flex;
        align-items: center;
        gap: 8px;
        color: rgba(255, 255, 255, 0.3);
        text-shadow: 0px 0px 36.4px #000;

        /* Labels/S/Regular */
        font-family: Sora;
        font-size: 12px;
        font-style: normal;
        font-weight: 400;
        line-height: 16px; /* 133.333% */
      }

      .value {
        display: flex;
        align-items: center;
        gap: 8px;
        flex: 1 0 0;
        align-self: stretch;

        .num {
          color: var(--GB-GB-White, #fff);
          text-shadow: 0px 0px 36.4px #000;

          /* H6/Regular */
          font-family: Sora;
          font-size: 20px;
          font-style: normal;
          font-weight: 400;
          line-height: 28px; /* 140% */
        }

        .percent {
          color: var(--BL-Green2, #00eba8);
          text-shadow: 0px 0px 15.5px rgba(0, 0, 0, 0.5);

          /* Labels/L/Regular */
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 400;
          line-height: 20px; /* 125% */
        }

        .n-progress {
          width: 298px;

          :deep(.n-progress-content) > div:last-child {
            margin-left: 12px;
            height: 28px;
            line-height: 28px;
          }

          :deep(.n-progress-icon) {
            color: var(--BL-Green2, #00eba8);
            text-align: right;
            text-shadow: 0px 0px 36.4px #000;

            /* H6/Regular */
            font-family: Sora;
            font-size: 20px;
            font-style: normal;
            font-weight: 400;
            line-height: 28px; /* 140% */
          }
        }
      }
    }
  }
}
</style>
