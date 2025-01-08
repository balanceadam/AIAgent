<script lang="ts" setup>
import { useWallet } from '@/hooks/useWallet'
import { useWalletStore } from '@/stores/wallet'
import { formatAddress, formatAmount } from '@/utils/index'
// 定义双向绑定的modelValue
interface Props {
  modelValue: boolean
}
const props = defineProps<Props>()

// 通过watch监听modelValue，实现数据的修改
const showModal = ref(false)
const showEditModal = ref(false)
watch(
  () => props.modelValue,
  (newV) => {
    showModal.value = newV
  }
)

const emit = defineEmits(['update:modelValue'])

const wallet = useWallet()
const walletStore = useWalletStore()
const disconnectWallet = () => {
  // 断开钱包连接
  wallet.disconnectWallet()
  emit('update:modelValue', false)
}

const handleCopy = () => {
  // 复制到剪切板
  navigator.clipboard.writeText(walletStore.wallet.address)
  window.$message.success('Copied address to clipboard')
}
</script>

<template>
  <n-modal
    class="custom-modal"
    v-model:show="showModal"
    transform-origin="center"
    @update:show="$emit('update:modelValue', $event)"
  >
    <div class="modal-content">
      <div class="info">
        <div class="info__top">
          <div class="avatar-wrapper">
            <img
              v-if="walletStore.userInfo.avatar"
              :src="walletStore.userInfo.avatar as string"
              alt=""
            />
            <img v-else src="https://picsum.photos/200/200" alt="" />
          </div>
          <div class="info__wrapper">
            <div class="info__name">
              <span>{{ walletStore.userInfo.name }}</span>
              <SvgIcon name="close" @click="$emit('update:modelValue', false)"></SvgIcon>
            </div>
            <div class="info__button" @click="showEditModal = true">
              <SvgIcon name="edit"></SvgIcon>
              <span>Edit Profile</span>
            </div>
          </div>
        </div>
        <div class="info__wallet">
          <div class="address">
            <span>{{ formatAddress(walletStore.wallet.address) }}</span>
            <span class="copy-text" @click="handleCopy">
              <SvgIcon name="copy"></SvgIcon>
            </span>
          </div>
          <div class="unit">
            <span>{{ formatAmount(Number(walletStore.wallet.balance ?? 0).toFixed(4)) }}</span>
            <SvgIcon name="ept"></SvgIcon>
            <span>EPT</span>
          </div>
        </div>
      </div>
      <div class="button button-create" @click="disconnectWallet">Disconnect Wallet</div>
    </div>
  </n-modal>
  <ProfileEditDialog v-model="showEditModal"></ProfileEditDialog>
</template>

<style lang="scss" scoped>
:global(.n-modal-mask) {
  background: linear-gradient(180deg, rgba(7, 5, 19, 0.05) 1.54%, rgba(255, 255, 255, 0.05) 100%);
  backdrop-filter: blur(25px);
}

.modal-content {
  display: flex;
  width: 640px;
  height: 400px;
  padding: 32px;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  border-radius: 24px;
  background: #000;

  .info {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 40px;
    align-self: stretch;

    &__top {
      display: flex;
      align-items: flex-start;
      gap: 20px;
      align-self: stretch;

      .avatar-wrapper {
        width: 98px;
        height: 98px;
        overflow: hidden;
        border-radius: 100%;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          object-position: center;
        }
      }
    }

    &__wrapper {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 20px;
      flex: 1 0 0;
    }

    &__name {
      display: flex;
      justify-content: space-between;
      align-items: center;
      align-self: stretch;

      span {
        color: #fff;
        /* H4/Regular */
        font-family: Sora;
        font-size: 28px;
        font-style: normal;
        font-weight: 400;
        line-height: 36px; /* 128.571% */
      }

      .svg-icon {
        width: 20px;
        height: 20px;
        flex-shrink: 0;
        cursor: pointer;
      }
    }

    &__button {
      display: flex;
      width: 153px;
      height: 42px;
      justify-content: center;
      align-items: center;
      gap: 8px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      cursor: pointer;

      .svg-icon {
        color: #fff;
        width: 20px;
        height: 20px;
        flex-shrink: 0;
      }

      span {
        color: #ededed;

        /* Labels/L/Regular */
        font-family: Sora;
        font-size: 16px;
        font-style: normal;
        font-weight: 400;
        line-height: 20px; /* 125% */
      }

      &:hover {
        border-color: rgba(255, 255, 255, 0.85);

        .svg-icon,
        span {
          color: rgba(#ededed, 0.85);
        }
      }

      &:active {
        border-color: rgba(255, 255, 255, 0.75);

        .svg-icon,
        span {
          color: rgba(#ededed, 0.75);
        }
      }
    }

    &__wallet {
      display: flex;
      height: 80px;
      padding: 0px 16px;
      justify-content: space-between;
      align-items: center;
      width: 100%;

      border-radius: 12px;
      border: 1px solid var(---Disable, rgba(255, 255, 255, 0.1));

      .address {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #888;

        /* Labels/L/Regular */
        font-family: Sora;
        font-size: 16px;
        font-style: normal;
        font-weight: 400;
        line-height: 20px; /* 125% */

        .copy-text {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 24px;
          height: 24px;
          background-color: #27272a;
          border-radius: 6px;
          cursor: pointer;

          &:hover {
            color: #e4e4e7;
          }
        }
      }

      .unit {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;

        .svg-icon {
          width: 24px;
          height: 24px;
          flex-shrink: 0;
        }

        span {
          color: #fff;

          /* Labels/L/Light */
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 300;
          line-height: 20px; /* 125% */
        }
      }
    }
  }

  .button {
    width: 100%;
    background-color: #1a1a1a;
    color: #fff;
    border: 1px solid rgba(255, 255, 255, 0.3);

    &:hover {
      color: rgba(#fff, 0.85);
      background-color: rgba(#1a1a1a, 0.85);
      border-color: rgba(255, 255, 255, 0.85);
    }

    &:active {
      color: rgba(#fff, 0.75);
      background-color: rgba(#1a1a1a, 0.75);
      border-color: rgba(255, 255, 255, 0.75);
    }
  }
}
</style>
