<script lang="ts" setup>
import type { SelectRenderLabel, SelectRenderTag } from 'naive-ui'
import type { SelectProps } from 'naive-ui'
import { NTag } from 'naive-ui'
import { useLaunchStore } from '@/stores/launch'

interface Props {
  label: string
  modelValue: number[]
}

const props = defineProps<Props>()

const launchStore = useLaunchStore()

const selectedValue = ref<typeof props.modelValue>(props.modelValue)

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
        [h('div', null, [option.name as string])]
      )
    ]
  )
}

const renderMultipleSelectTag: SelectRenderTag = ({ option }) => {
  return h(
    NTag,
    {
      bordered: false,
      style: {
        display: 'flex',
        alignItems: 'center',
        flexWrap: 'nowrap',
        whiteSpace: 'nowrap',
        '--n-color': 'transparent',
        '--n-text-color': '#888'
      }
    },
    {
      default: () => `${option.name as string};`
    }
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
      border: '1px solid rgba(255, 255, 255, 0.85)',
      borderActive: '1px solid rgba(255, 255, 255, 0.3)',
      borderFocus: '1px solid rgba(255, 255, 255, 0.3)',
      borderHover: '1px solid rgba(255, 255, 255, 0.3)',
      placeholderColor: '#888',
      heightMedium: '64px',
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
// launchStore.getGamesList()
</script>

<template>
  <div class="game-select-wrapper">
    <div class="label">{{ props.label }}</div>
    <div class="value">
      <n-select
        class="game-select"
        multiple
        max-tag-count="responsive"
        v-model:value="selectedValue"
        label-field="name"
        value-field="id"
        :options="launchStore.gameList"
        :render-label="renderLabel"
        :render-tag="renderMultipleSelectTag"
        :theme-overrides="selectThemeOverrides"
        @update:value="$emit('update:modelValue', selectedValue)"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.game-select-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .label {
    color: #fff;
    text-shadow: 0px 0px 36.4px #000;

    /* H6/Regular */
    font-family: Sora;
    font-size: 20px;
    font-style: normal;
    font-weight: 400;
    line-height: 28px; /* 140% */
  }

  .value {
    :deep(.n-base-selection-tag-wrapper .n-tag) {
      background-color: transparent;
      color: #888;

      .n-tag__content {
        font-weight: 300;
      }

      .n-tag__border {
        border-color: #888;
        // border: none;
      }
    }
    :deep(.n-base-selection .n-base-suffix) {
      font-weight: 300;
      right: 16px;
    }
  }
}
</style>
