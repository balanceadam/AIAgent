<script lang="ts" setup>
import { useWallet } from '@/hooks/useWallet'

interface Props {
  modelValue: boolean
}
const props = defineProps<Props>()

const showModal = ref(false)
watch(
  () => props.modelValue,
  (newV) => {
    showModal.value = newV
  }
)

const wallet = useWallet()
const emit = defineEmits(['update:modelValue'])
const connectWallet = async (walletType: string) => {
  // connect wallet
  await wallet.connectWallet(walletType)
  emit('update:modelValue', false)
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
      <div class="header">
        <div class="title">Connect Wallet</div>
        <SvgIcon name="close" @click="$emit('update:modelValue', false)"></SvgIcon>
      </div>
      <div class="image-wallet">
        <img src="@/assets/images/wallet.svg" alt="" />
      </div>
      <div class="wallet-list">
        <div class="wallet-item" @click="connectWallet('MetaMask')">
          <div class="item__left">
            <div class="icon-wrapper metamask">
              <SvgIcon name="metamask"></SvgIcon>
            </div>
            <span>MetaMask</span>
          </div>
          <div class="item__right">
            <SvgIcon name="arrow-right"></SvgIcon>
          </div>
        </div>
        <div class="wallet-item">
          <div class="item__left">
            <div class="icon-wrapper ton">
              <SvgIcon name="ton"></SvgIcon>
            </div>

            <span>Ton Wallet</span>
          </div>
          <div class="item__right">
            <SvgIcon name="arrow-right"></SvgIcon>
          </div>
        </div>
        <div class="wallet-item">
          <div class="item__left">
            <div class="icon-wrapper binance">
              <SvgIcon name="binance"></SvgIcon>
            </div>

            <span>Binance Wallet</span>
          </div>
          <div class="item__right">
            <SvgIcon name="arrow-right"></SvgIcon>
          </div>
        </div>
      </div>
    </div>
  </n-modal>
</template>

<style lang="scss" scoped>
:global(.n-modal-mask) {
  background: linear-gradient(180deg, rgba(7, 5, 19, 0.05) 1.54%, rgba(255, 255, 255, 0.05) 100%);
  backdrop-filter: blur(25px);
}

.modal-content {
  display: flex;
  width: 640px;
  padding: 32px;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  gap: 64px;
  flex-shrink: 0;
  border-radius: 24px;
  background: #000;

  .header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    align-self: stretch;

    .title {
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

  .image-wallet {
    width: 100%;
    text-align: center;

    img {
      width: 160px;
      height: 160px;
    }
  }

  .wallet {
    &-list {
      width: 100%;
      display: flex;
      padding-bottom: 24px;
      flex-direction: column;
      align-items: flex-start;
      gap: 16px;
      align-self: stretch;
    }

    &-item {
      width: 100%;
      display: flex;
      height: 56px;
      padding: 0px 20px;
      align-items: center;
      gap: 12px;
      align-self: stretch;
      border-radius: 12px;
      border: 1px solid var(---Normal, rgba(255, 255, 255, 0.3));
      cursor: pointer;

      .item__left {
        display: flex;
        align-items: center;
        gap: 8px;
        flex: 1;

        .icon-wrapper {
          display: flex;
          width: 32px;
          height: 32px;
          justify-content: center;
          align-items: center;
          gap: 13.333px;
          border-radius: 5.333px;

          .svg-icon {
            width: 21px;
            height: 21px;
          }

          &.metamask {
            background: #fff;
          }

          &.ton {
            background: #08c;
          }

          &.binance {
            background: #f0b90b;
          }
        }

        span {
          color: #fff;

          /* Labels/L/Regular */
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 400;
          line-height: 20px; /* 125% */
        }
      }

      .item__right {
        width: 24px;
        height: 24px;
        color: #ededed;

        .svg-icon {
          width: 24px;
          height: 24px;
        }
      }

      &:hover {
        opacity: 0.85;
      }

      &:active {
        opacity: 0.75;
      }
    }
  }
}
</style>
