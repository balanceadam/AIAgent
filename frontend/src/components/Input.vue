<script lang="ts" setup>
interface Props {
  label: string
  length?: number
  type: 'text' | 'password' | 'textarea'
  modelValue: string | [string, string] | null | undefined
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text'
})

const attrs = useAttrs()

const len = ref(0)

const value = ref<string | [string, string] | null | undefined>(props.modelValue)

watch(
  () => props.modelValue,
  (newV) => {
    value.value = newV
  }
)

const emit = defineEmits<{ (e: 'update:modelValue', val: string): void }>()
const onInput = (val: string) => {
  len.value = val.length
  emit('update:modelValue', val)
}
</script>

<template>
  <div class="input-widget">
    <div class="label">
      <div class="label__left">{{ props.label }}</div>
      <div class="label__right" v-if="props.length">
        {{ `${len}/${props.length}` }}
      </div>
    </div>
    <div class="value">
      <n-input
        v-bind="attrs"
        v-model:value="value"
        :type="props.type"
        style="
          --n-border-radius: 12px;
          --n-border: 1px solid rgba(255, 255, 255, 0.3);
          --n-border-hover: 1px solid rgba(255, 255, 255, 0.85);
          --n-border-focus: 1px solid rgba(255, 255, 255, 0.85);
          --n-placeholder-color: rgba(194, 194, 194, 1);
        "
        :maxlength="props.length"
        :on-clear="() => (len = 0)"
        :on-input="onInput"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.input-widget {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
  align-self: stretch;
  width: 100%;

  .label {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 16px;
    align-self: stretch;

    &__left {
      color: #fff;
      text-shadow: 0px 0px 36.4px #000;

      /* H6/Regular */
      font-family: Sora;
      font-size: 20px;
      font-style: normal;
      font-weight: 400;
      line-height: 28px; /* 140% */
    }

    &__right {
      color: rgba(255, 255, 255, 0.3);
      text-align: right;
      text-shadow: 0px 0px 36.4px #000;
      opacity: 0.7;

      /* Paragraphs/XS/Light */
      font-family: Sora;
      font-size: 12px;
      font-style: normal;
      font-weight: 300;
      line-height: 20px; /* 166.667% */
    }
  }

  .value {
    width: 100%;

    :deep(.n-input) {
      .n-input {
        overflow: hidden;
        &__input {
          height: 56px;
          line-height: 56px;
        }

        &-wrapper {
          padding: 0px 16px;
          background: #111;
        }

        &__placeholder,
        &__placeholder span {
          color: rgba(255, 255, 255, 0.3);
          text-shadow: 0px 0px 36.4px #000;

          /* Labels/M/Light */
          font-family: Sora;
          font-size: 14px;
          font-style: normal;
          font-weight: 300;
          line-height: 18px; /* 128.571% */
        }

        &__input-el,
        &__textarea-el {
          color: #fff;
          font-weight: 300;
          caret-color: #fff;
        }
      }
    }
  }
}
</style>
