<script lang="ts" setup>
type CommentType = 'thread' | 'trades'
const type = ref<CommentType>('thread')
</script>

<template>
  <div class="comment-panel">
    <n-tabs
      v-model:value="type"
      type="segment"
      :animated="false"
      style="
        --n-color-segment: rgba(255, 255, 255, 0.03);
        --n-tab-text-color: rgba(255, 255, 255, 0.3);
        --n-tab-text-color-active: #1e1e22;
        --n-tab-border-radius: 12px;
        --n-tab-font-size: 16px;
        --n-tab-padding: 9px 0;
        --n-pane-padding-top: 16px;
        --n-tab-border-radius: 8px;
      "
      :style="{
        '--n-tab-color-segment': '#FFFFFF'
      }"
    >
      <n-tab-pane name="thread">
        <template #tab>
          <svg-icon
            name="comment"
            style="width: 16px; height: 16px; flex-shrink: 0; margin-right: 6px"
          />
          <span class="text">Thread</span>
        </template>
        <template #default>
          <CommentPost />
          <CommentList />
        </template>
      </n-tab-pane>
      <n-tab-pane name="trades">
        <template #tab>
          <svg-icon
            name="trades"
            style="width: 16px; height: 16px; flex-shrink: 0; margin-right: 6px"
          />
          <span class="text">Trades</span>
        </template>
        <template #default>
          <TradeHistory />
        </template>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<style lang="scss" scoped>
.comment-panel {
  margin-top: 24px;
  padding: 0 40px;
}
</style>
