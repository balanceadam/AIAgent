<script lang="ts" setup>
import type { SelectRenderLabel } from 'naive-ui'
import type { SelectProps } from 'naive-ui'

interface Props {
  modelValue: string | null | undefined
}

const props = defineProps<Props>()

const selectedValue = ref<typeof props.modelValue>(props.modelValue ?? 'createdAt')

const filterList = ref([
  {
    label: 'Launched Time',
    value: 'createdAt'
  },
  {
    label: 'Trading Volume',
    value: 'dayTradingVolume'
  },
  {
    label: 'Market Cap',
    value: 'marketValue'
  },
  {
    label: '24H Price Increase',
    value: 'dayIncrease'
  }
])

watch(
  () => props.modelValue,
  (val) => {
    selectedValue.value = val
  }
)

const renderLabel: SelectRenderLabel = (option) => {
  return h(
    'div',
    {
      style: {
        display: 'flex',
        alignItems: 'center'
      }
    },
    [
      h(
        'div',
        {
          style: {
            marginLeft: '8px',
            padding: '4px 0',
            fontSize: '16px'
          }
        },
        [h('div', null, [option.label as string])]
      )
    ]
  )
}

type SelectThemeOverrides = NonNullable<SelectProps['themeOverrides']>
const selectThemeOverrides: SelectThemeOverrides = {
  peers: {
    InternalSelection: {
      textColor: '#fff',
      borderRadius: '40px',
      color: '#111',
      colorActive: '#111',
      colorActiveError: '#111',
      border: '1px solid rgba(255, 255, 255, 0.25)',
      borderActive: '1px solid rgba(255, 255, 255, 0.3)',
      borderFocus: '1px solid rgba(255, 255, 255, 0.3)',
      borderHover: '1px solid rgba(255, 255, 255, 0.3)',
      placeholderColor: 'rgba(255, 255, 255, 0.30)',
      heightMedium: '48px',
      paddingSingle: '0 36px 0 16px'
    },
    InternalSelectMenu: {
      color: '#202020',
      optionTextColor: '#fff',
      optionTextColorActive: '#fff',
      optionCheckColor: '#EDEDED',
      optionColorActive: '#111',
      optionColorPending: '#111',
      optionColorActivePending: '#111',
      optionPaddingMedium: '8px 20px'
    }
  }
}
</script>

<template>
  <div class="filter-select-wrapper">
    <n-select
      v-model:value="selectedValue"
      label-field="label"
      value-field="value"
      :options="filterList"
      :render-label="renderLabel"
      :theme-overrides="selectThemeOverrides"
      @update:value="$emit('update:modelValue', selectedValue)"
    />
  </div>
</template>

<style lang="scss" scoped>
.filter-select-wrapper {
  width: 218px;

  :deep(.n-base-selection .n-base-suffix) {
    font-weight: 300;
    right: 16px;
  }
}
</style>
