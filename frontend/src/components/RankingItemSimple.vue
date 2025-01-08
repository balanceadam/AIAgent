<script lang="ts" setup>
import type { AssetsToken } from '@/types'
import { formatAmountWithUnit } from '@/utils/index'

interface Props {
  index: number
  token: AssetsToken
  currentTab: number
}

defineProps<Props>()

const router = useRouter()
const handleClick = (id: number) => {
  router.push({ name: 'epal-detail', params: { id } })
}
</script>

<template>
  <div class="ranking-item-simple" @click="handleClick(token.id)">
    <div class="index">{{ index }}</div>
    <div class="wrapper">
      <div class="info">
        <div class="avatar">
          <img :src="token.logo" alt="" />
        </div>
        <div class="user">
          <div class="label">Name (Symbol)</div>
          <div class="value">{{ token.name }}</div>
        </div>
      </div>
      <div class="bonding" v-if="currentTab === 0 || currentTab === 2">
        <div class="label">BondingCurve%</div>
        <div class="value">
          <n-progress
            type="line"
            color="#fff"
            :height="8"
            rail-color="rgba(255, 255, 255, 0.04)"
            :percentage="token.protocol.bondingCurve"
            indicator-text-color="#fff"
          />
        </div>
      </div>
      <div class="bonding" v-if="currentTab === 1">
        <div class="label">Market Cap</div>
        <div class="value">
          {{ `$${formatAmountWithUnit(token.protocol.marketValue)}` }}
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.ranking-item-simple {
  display: flex;
  padding: 12px 24px;
  align-items: center;
  align-self: stretch;
  gap: 4px;
  border-radius: 12px;
  border: 1px solid transparent;
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0px 0px 19.2px 0px rgba(77, 77, 77, 0.06);
  font-family: Sora;
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
    width: 40px;
    height: 40px;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 5px;
    color: white;
    font-weight: 400;
  }

  .wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex: 1;

    .info {
      display: flex;
      align-items: center;
      gap: 16px;
      flex: 1 0 0;
      align-self: stretch;
      height: 64px;

      .avatar {
        width: 44px;
        height: 44px;
        border-radius: 8px;
        box-shadow:
          0px 0px 4.693px 0px rgba(0, 0, 0, 0.6),
          0px 0px 8.565px 0px rgba(77, 77, 77, 0.12);

        overflow: hidden;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
      }
    }

    .user {
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 12px;
    }

    .bonding {
      width: 200px;
      align-items: flex-end;
      .label {
        text-align: right;
        margin-bottom: 12px;
      }

      .value {
        text-align: right;
        color: #fff;
      }
    }

    .label {
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
      color: rgba(255, 255, 255, 0.85);
      text-shadow: 0px 0px 36.4px #000;

      /* Labels/L/Light */
      font-family: Sora;
      font-size: 16px;
      font-style: normal;
      font-weight: 300;
      line-height: 20px; /* 125% */
    }
  }
}
</style>
