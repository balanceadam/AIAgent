<script lang="ts" setup>
interface Props {
  icon?: string
  description?: string
}
defineProps<Props>()
</script>

<template>
  <div class="empty-view">
    <div class="no-data">
      <img v-if="!!icon" :src="icon" alt="" />
      <img v-else src="@/assets/images/no-data.svg" />
      <div class="text">
        <slot>{{ description ?? 'No token has been created yet' }}</slot>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.empty-view {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  .no-data {
    margin-top: 180px;
    margin-bottom: 180px;
    display: flex;
    // width: 214px;
    flex-direction: column;
    align-items: center;
    gap: 24px;

    img {
      width: 128px;
      height: 128px;
    }

    .text {
      color: rgba(255, 255, 255, 0.3);

      /* Labels/M/Light */
      font-family: Sora;
      font-size: 14px;
      font-style: normal;
      font-weight: 300;
      line-height: 18px; /* 128.571% */
    }
  }
}
</style>
