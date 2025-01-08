<script lang="ts" setup>
import type { NotificationReactive } from 'naive-ui'
import { useLaunchStore } from '@/stores/launch'
import { useWalletStore } from '@/stores/wallet'
import { useAssetsStore } from '@/stores/assets'
import { useWallet } from '@/hooks/useWallet'
import { formatAmount, progressNotify, successNotify, simpleNotify } from '@/utils'

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
const { postMyPosition } = useAssetsStore()
const launchStore = useLaunchStore()
const walletStore = useWalletStore()

const selectedChain = computed(
  () =>
    launchStore.chainList.find((item) => item.id === launchStore.launchForm.chain) ?? {
      id: 0,
      name: '',
      logo: '',
      symbol: '',
      fee: 0
    }
)

const errorMessage = computed(() => {
  if (!launchStore.launchForm.initialBuyNumber) {
    return ''
  } else if (
    !/^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$/.test(launchStore.launchForm.initialBuyNumber + '')
  ) {
    return 'Please enter the number of tokens'
  } else if (launchStore.launchForm.initialBuyNumber < 0) {
    return 'Please enter a positive number'
  } else if (launchStore.launchForm.initialBuyNumber > Number(walletStore.wallet.balance ?? 0)) {
    return 'Please enter a number less than your balance'
  }
})

const inputRef = ref<HTMLInputElement>()
const handleFocus = () => {
  inputRef.value?.focus()
}

const handleSwitch = () => {
  // TODO: 切换代币和钱包币
  launchStore.launchForm.initialBuyType = launchStore.launchForm.initialBuyType === 1 ? 2 : 1
  // 切换币种以及计算Balance
}

const isLoading = ref(false)
const router = useRouter()
const { createToken, purchaseTokenWithCurrency, getTokenBalance } = useWallet()

// 购买代币操作
const handleBuy = async (tokenId: number, protocolId: number, amount: number, address: string) => {
  try {
    const receipt = await purchaseTokenWithCurrency(protocolId, amount ?? 0)
    // 处理成功，例如更新余额或显示通知
    console.log('Purchase successful:', receipt)
    const position = await getTokenBalance(address)
    await postMyPosition({
      position: Number(position ?? 0),
      token: tokenId,
      account: walletStore.userInfo.id
    })
    return Promise.resolve(true)
  } catch (error) {
    console.error(error)
    return Promise.reject(false)
  }
}

const emit = defineEmits(['createSuccess', 'update:modelValue'])

const handleSubmit = async () => {
  let notify: any, notify2: NotificationReactive

  // 校验输入的购买数量是否合法
  if (launchStore.launchForm.initialBuyNumber && errorMessage.value) return false

  try {
    isLoading.value = true
    // 右侧进行中通知
    notify = progressNotify()

    const protocol = await createToken(launchStore.launchForm.name, selectedChain.value.symbol)
    if (protocol) {
      console.log('Token creation succeeded:', protocol)
      // 生成的合约信息
      launchStore.launchForm.protocol = protocol
    } else {
      isLoading.value = false
      // 关闭弹窗
      showModal.value = false
      // 关闭弹窗
      emit('update:modelValue', false)

      console.error('Token creation failed')
      // 关闭弹窗
      notify.destroy()

      // 创建失败提示
      simpleNotify('Creation failed', 'fail')
      return Promise.reject(false)
    }

    const token = await launchStore.sumbitAssetsToken()
    if (token?.id && (launchStore.launchForm.initialBuyNumber ?? 0) > 0) {
      // 自购代币
      await handleBuy(
        token.id,
        token.protocol.protocolId,
        launchStore.launchForm.initialBuyNumber as number,
        token.protocol.address
      )

      isLoading.value = false
      notify.destroy()
      // 关闭弹窗
      showModal.value = false
      // 创建成功提示
      notify2 = successNotify(() => {
        notify2.destroy()
        setTimeout(() => {
          router.push('/me')
        }, 500)
      })

      // 重置表单
      launchStore.resetLaunchForm()
      emit('createSuccess', true)

      // 关闭弹窗
      emit('update:modelValue', false)
    } else {
      isLoading.value = false
      // 关闭弹窗
      showModal.value = false
      notify?.destroy()
      // 关闭弹窗
      emit('update:modelValue', false)
    }
  } catch (error) {
    isLoading.value = false
    // 关闭弹窗
    showModal.value = false
    notify?.destroy()
    simpleNotify('Creation failed', 'fail')
    console.error(error)
    // 关闭弹窗
    emit('update:modelValue', false)
  }
}

const goEpal = () => {
  emit('update:modelValue', false)

  // 跳转到Epal页面
  router.push('/epal')
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
      <template v-if="!isLoading">
        <div class="top">
          <div class="header">
            <div class="title">Initial Buy</div>
            <SvgIcon name="close" @click="$emit('update:modelValue', false)"></SvgIcon>
          </div>
          <div class="desc">
            when the market cap reaches $0 all the liquidity from the bonding curve will be
            deposited into Fans Protocol and burned. progression increases as the price goes up.
          </div>
        </div>
        <div class="form">
          <div class="chain">
            <div class="label">Confirmation chain</div>
            <div class="value">
              <div class="chain-wrapper">
                <img :src="selectedChain.logo" alt="" />
                <div class="chain-info">
                  <div class="name">{{ selectedChain.name }}</div>
                  <div class="symbol">
                    {{ `Estimated Fee: ${selectedChain.fee} ${selectedChain.symbol}` }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="tokens-wrapper">
            <!-- <div class="switch" @click="handleSwitch">
              <SvgIcon name="switch"></SvgIcon>
              <span>{{ `Switch to ${launchStore.launchForm.ticker}` }}</span>
            </div> -->
            <div class="input-wrapper" @click="handleFocus">
              <div class="tokens__left">
                <input
                  ref="inputRef"
                  class="input"
                  type="text"
                  v-model="launchStore.launchForm.initialBuyNumber"
                  placeholder="Enter the number of Tokens"
                />

                <div class="balance">
                  <div class="text">Balance:</div>
                  <div class="amount">
                    {{
                      `${formatAmount(Number(walletStore.wallet.balance ?? 0).toFixed(4))} ${selectedChain.symbol}`
                    }}
                  </div>
                </div>
              </div>
              <div class="tokens__right">
                <SvgIcon name="ept"></SvgIcon>
                <div class="text">{{ selectedChain.symbol }}</div>
              </div>
            </div>
            <div v-if="!!errorMessage" class="error">{{ errorMessage }}</div>
          </div>
        </div>
        <div class="action">
          <div
            class="button button-create"
            :class="{ disabled: !Number(walletStore.wallet.balance ?? 0) }"
            @click="handleSubmit"
          >
            Create Coin Now!!!
          </div>
        </div>
      </template>
      <template v-else>
        <div class="waiting">
          <div class="title">Waiting...</div>
          <div class="desc">
            Interaction with the blockchain in progress. This may take a few minutes. <br />
            Note: Due to potential network congestion, the wait time could be longer. Please be
            patient.
          </div>
        </div>
        <div class="loading">
          <img src="@/assets/images/loading.gif" alt="" />
        </div>
        <div class="button button-create" @click="goEpal">Close and wait</div>
      </template>
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
  gap: 40px;
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

  .desc {
    margin-top: 10px;
    color: #888;
    text-shadow: 0px 0px 36.4px #000;

    /* Paragraphs/XS/Light */
    font-family: Sora;
    font-size: 12px;
    font-style: normal;
    font-weight: 300;
    line-height: 20px; /* 166.667% */
    opacity: 0.7;
  }

  .form {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 40px;
    align-self: stretch;

    .chain {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 16px;
      align-self: stretch;

      .label {
        color: #fff;
        text-shadow: 0px 0px 36.4px #000;
        font-family: Sora;
        font-size: 20px;
        font-style: normal;
        font-weight: 400;
        line-height: 28px; /* 140% */
      }

      .value {
        display: flex;
        height: 64px;
        padding: 0px 16px;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        align-self: stretch;
        border-radius: 40px;
        background: var(--icon, #1e1e22);

        .chain-wrapper {
          display: flex;
          align-items: center;
          gap: 8px;

          img {
            width: 32px;
            height: 32px;
            flex-shrink: 0;
          }

          .chain-info {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 4px;

            .name {
              color: #fff;
              font-family: Sora;
              font-size: 16px;
              font-style: normal;
              font-weight: 400;
              line-height: 20px; /* 125% */
            }

            .symbol {
              color: #888;
              font-family: Sora;
              font-size: 14px;
              font-style: normal;
              font-weight: 300;
              line-height: 18px; /* 128.571% */
            }
          }
        }
      }
    }

    .tokens-wrapper {
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
      align-self: stretch;
      width: 100%;

      .switch {
        width: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        cursor: pointer;

        .svg-icon {
          width: 16px;
          height: 16px;
          flex-shrink: 0;
        }

        span {
          margin-left: 4px;
          color: #ededed;
          font-family: Sora;
          font-size: 12px;
          font-style: normal;
          font-weight: 400;
          line-height: 16px; /* 133.333% */
        }
      }

      .input-wrapper {
        display: flex;
        height: 80px;
        padding: 0px 16px;
        justify-content: space-between;
        align-items: center;
        align-self: stretch;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        background: #111;

        .tokens {
          &__left {
            display: flex;
            height: 58px;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            gap: 8px;
            flex: 1;

            .input {
              width: 100%;
              border: none;
              background: transparent;
              color: #fff;

              /* Labels/L/Regular */
              font-family: Sora;
              font-size: 16px;
              font-style: normal;
              font-weight: 400;
              line-height: 20px; /* 125% */

              &:focus-visible {
                outline: none;
              }
            }

            .balance {
              display: flex;
              align-items: center;
              gap: 4px;

              .text {
                color: #888;
                font-family: Sora;
                font-size: 12px;
                font-style: normal;
                font-weight: 300;
                line-height: 16px; /* 133.333% */
              }

              .amount {
                color: #fff;
                font-family: Sora;
                font-size: 14px;
                font-style: normal;
                font-weight: 400;
                line-height: 18px; /* 128.571% */
              }
            }
          }

          &__right {
            display: flex;
            align-items: center;
            gap: 8px;

            .text {
              color: #fff;
              font-family: Sora;
              font-size: 16px;
              font-style: normal;
              font-weight: 300;
              line-height: 20px; /* 125% */
            }
          }
        }
      }

      .error {
        position: absolute;
        bottom: -24px;
        font-size: 14px;
        line-height: 1.5;
        color: #d03050;
      }
    }
  }

  .action {
    display: flex;
    flex-direction: column;
    align-items: center;
    align-self: stretch;

    .button {
      width: 100%;
      font-weight: 300;
    }
  }

  .waiting {
    margin-top: 80px;

    .title {
      color: #fff;

      /* H4/Regular */
      font-family: Sora;
      font-size: 28px;
      font-style: normal;
      font-weight: 400;
      line-height: 36px; /* 128.571% */
    }

    .desc {
      margin-top: 10px;
      color: #fff;
      text-shadow: 0px 0px 36.4px #000;

      /* Paragraphs/XS/Light */
      font-family: Sora;
      font-size: 12px;
      font-style: normal;
      font-weight: 300;
      line-height: 20px; /* 166.667% */
    }
  }

  .loading {
    margin-top: 70px;
    margin-bottom: 160px;
  }

  .button-create {
    width: 100%;
    font-weight: 300;

    &.disabled {
      opacity: 0.3;
      cursor: not-allowed;
    }
  }
}
</style>
