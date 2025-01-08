<script lang="ts" setup>
import type { SelectRenderLabel, SelectRenderTag } from 'naive-ui'
import type { SelectProps } from 'naive-ui'
import { NAvatar, NText } from 'naive-ui'
import { useLaunchStore } from '@/stores/launch'

interface Props {
  label?: string
  modelValue: number | null | undefined
  showFee?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  showFee: true
})

const launchStore = useLaunchStore()

const selectedValue = ref<typeof props.modelValue>(props.modelValue ?? launchStore.chainList[0]?.id)

watch(
  () => props.modelValue,
  (val) => {
    selectedValue.value = val ?? launchStore.chainList[0]?.id
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
      h(NAvatar, {
        src: option.logo as string,
        round: true,
        size: 32
      }),
      h(
        'div',
        {
          style: {
            marginLeft: '8px',
            padding: '4px 0',
            fontSize: '16px'
          }
        },
        [
          h('div', null, [option.name as string]),
          props.showFee
            ? h(
                NText,
                {
                  depth: 3,
                  tag: 'div',
                  style: {
                    fontSize: '14px',
                    fontWeight: 300,
                    color: '#888',
                    lineHeight: '18px'
                  }
                },
                {
                  default: () => `Estimated Fee: ${option.fee} ${option.symbol}`
                }
              )
            : ''
        ]
      )
    ]
  )
}

const renderSingleSelectTag: SelectRenderTag = ({ option }) => {
  return h(
    'div',
    {
      style: {
        display: 'flex',
        alignItems: 'center'
      }
    },
    [
      h(NAvatar, {
        src: option.logo as string,
        round: true,
        size: 32
      }),
      h(
        'div',
        {
          style: {
            marginLeft: '8px',
            padding: '4px 0',
            fontSize: '16px'
          }
        },
        [
          h('div', null, [option.name as string]),
          props.showFee
            ? h(
                NText,
                {
                  depth: 3,
                  tag: 'div',
                  style: {
                    fontSize: '14px',
                    fontWeight: 300,
                    color: '#888',
                    lineHeight: '18px'
                  }
                },
                {
                  default: () => `Estimated Fee: ${option.fee} ${option.symbol}`
                }
              )
            : ''
        ]
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
      border: '1px solid rgba(255, 255, 255, 0.25)',
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

const emit = defineEmits(['update:modelValue'])

watch(
  () => launchStore.chainList,
  (newV) => {
    if (newV?.length) {
      selectedValue.value = newV[0].id
    } else {
      selectedValue.value = null
    }
    emit('update:modelValue', selectedValue.value)
  }
)
</script>

<template>
  <div class="select-wrapper">
    <div class="label" v-if="props.label">
      {{ props.label }}
    </div>
    <div class="value">
      <n-select
        v-model:value="selectedValue"
        label-field="name"
        value-field="id"
        :options="launchStore.chainList"
        :render-label="renderLabel"
        :render-tag="renderSingleSelectTag"
        :theme-overrides="selectThemeOverrides"
        @update:value="$emit('update:modelValue', selectedValue)"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.select-wrapper {
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
    :deep(.n-base-selection .n-base-suffix) {
      font-weight: 300;
      right: 16px;
    }
  }
}
</style>
