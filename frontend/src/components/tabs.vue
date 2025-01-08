<script lang="ts" setup>
interface TabsItem {
  label: string
  name: string | number
}

interface Tabs {
  modelValue: number | string
  tabItems: TabsItem[]
}
withDefaults(defineProps<Tabs>(), {
  modelValue: 0,
  tabItems: () => []
})

const emit = defineEmits(['update:modelValue'])

const handleToggle = (index: number) => {
  emit('update:modelValue', index)
}
</script>

<template>
  <div class="tabs">
    <div
      class="tab"
      :class="{ active: modelValue === index }"
      v-for="(item, index) in tabItems"
      :name="item.name"
      :key="item.name"
      @click="handleToggle(index)"
    >
      {{ item.label }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
.tabs {
  display: flex;
  gap: 12px;

  .tab {
    display: flex;
    padding: 8px 16px;
    justify-content: center;
    align-items: center;
    border-radius: 40px;
    border: 1px solid transparent;
    cursor: pointer;

    /* Labels/M/Regular */
    font-family: Sora;
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: 18px; /* 128.571% */
    color: rgba(255, 255, 255, 0.3);

    &.active {
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: #fff;
    }
  }
}
</style>
