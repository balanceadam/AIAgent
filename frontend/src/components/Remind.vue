<script lang="ts" setup>
export type Action = 'buy' | 'sold' | 'create'
interface RemindItemProps {
  avatar?: string
  name?: string
  action: Action
}

const props = defineProps<RemindItemProps>()
</script>

<template>
  <div class="remind-item">
    <div class="avatar">
      <img src="@/assets/images/avatar.png" alt="" />
    </div>
    <div class="name">Team Wang</div>
    <div class="action">
      <span v-if="props.action === 'buy'" class="buy">Bought 0.010 BTC</span>
      <span v-else-if="props.action === 'sold'" class="sold">Sold 0.010 BTC</span>
      <span v-else class="create">Created</span>
      <span v-if="props.action !== 'create'" class="other">of</span>
    </div>
    <div class="avatar">
      <img src="@/assets/images/avatar.png" alt="" />
    </div>
    <div class="name">MEGA</div>
  </div>
</template>

<style lang="scss" scoped>
.remind-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  gap: 8px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0px 0px 19.2px 0px rgba(77, 77, 77, 0.06);

  .avatar {
    width: 32px;
    height: 32px;
    border-radius: 4px;
    background: url(<path-to-image>) lightgray 50% / cover no-repeat;
    box-shadow:
      0px 0px 3.413px 0px rgba(0, 0, 0, 0.6),
      0px 0px 6.229px 0px rgba(77, 77, 77, 0.12);

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

    /* Labels/L/Regular */
    font-family: Sora;
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: 20px; /* 125% */
  }

  .action {
    /* Labels/M/Semibold */
    font-family: Sora;
    font-size: 14px;
    font-style: normal;
    font-weight: 600;
    line-height: 20px; /* 128.571% */

    span {
      display: inline-flex;
      align-items: center;

      &:not(.other) {
        margin: 0 8px;
      }
    }

    .buy {
      color: var(--BL-Green2, #00eba8);
    }

    .sold {
      color: var(--BL-red, #da4354);
    }

    .create {
      color: var(--GB-GB-Blue, #3fd9ff);
    }

    .other {
      margin-left: 8px;
      color: #888;
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
</style>
