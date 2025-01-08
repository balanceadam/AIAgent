<!-- eslint-disable vue/no-mutating-props -->
<script lang="ts" setup>
import { formatAmount, simpleNotify, progressNotify } from '@/utils'
import { useWalletStore } from '@/stores/wallet'
import { useAssetsStore } from '@/stores/assets'
import { useWallet } from '@/hooks/useWallet'
import type { AssetsToken } from '@/types'

interface Props {
  token: AssetsToken
}

const { token } = defineProps<Props>()

const showWalletModal = ref(false)
const tradeType = ref('buy')
const isInputFocused = ref(false)

// 是否是切换到代币交易
const isTokenPurchase = ref(false)

const buyAmount = ref<number | null>(null)
// 最大可购买代币数量
const maxTokenBuyBalance = ref<number>(0)
// 计算输入金额可购买代币数量
const estimatedTokenPurchase = ref<number>(0)

// 可售卖代币余额
const tokenBalance = ref(0)

const walletStore = useWalletStore()
const { postMyPosition } = useAssetsStore()
const {
  purchaseTokenWithCurrency,
  sellTokenWithFanToken,
  getBondingCurveInfo,
  getTokenBalance,
  estimateTokenPurchase
} = useWallet()

const buyErrorMessage = computed(() => {
  if (!buyAmount.value) {
    return ''
  } else if (!/^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$/.test(buyAmount.value + '')) {
    return 'Please enter the number of tokens'
  } else if (buyAmount.value < 0) {
    return 'Please enter a positive number'
  }
  // 如果是非代币交易，并且输入的数量大于余额，提示余额不足
  else if (
    (!isTokenPurchase.value && buyAmount.value > Number(walletStore.wallet.balance ?? 0)) ||
    (isTokenPurchase.value && buyAmount.value > Number(maxTokenBuyBalance.value ?? 0))
  ) {
    return 'Please enter a number less than your balance'
  }
})

const sellErrorMessage = computed(() => {
  if (!sellAmount.value) {
    return ''
  } else if (!/^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$/.test(sellAmount.value + '')) {
    return 'Please enter the number of tokens'
  } else if (sellAmount.value < 0) {
    return 'Please enter a positive number'
  }
  // 如果是非代币交易，并且输入的数量大于余额，提示余额不足
  else if (sellAmount.value > Number(tokenBalance.value ?? 0)) {
    return 'Please enter a number less than your balance'
  }
})

const inputRef = ref<HTMLInputElement>()

const handleFocus = () => {
  inputRef.value?.focus()
}

const handleSwitch = async () => {
  // 切换代币和钱包币
  isTokenPurchase.value = !isTokenPurchase.value
  // 清空amount
  buyAmount.value = null
}

// 文本框只允许输入数字
const handleKeyDown = (e: KeyboardEvent) => {
  // 获取按下的键值
  const key = e.key

  // 定义允许的数字键值
  const allowedKeys = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'Backspace',
    'Delete',
    'ArrowLeft',
    'ArrowRight',
    '.'
  ]

  // 如果按下的键不在允许的键值中，则阻止默认行为
  if (!allowedKeys.includes(key)) {
    e.preventDefault()
  }
}

// 点击快捷输入
const handleShortcut = (count: any) => {
  // 快捷选择
  buyAmount.value = count
  console.log(buyAmount.value)

  // 快捷输入购买数量，计算可购买代币数量
  handleEstimate(buyAmount.value ?? 0)
}

// 根据输入的数量计算可购买代币数量
const handleEstimate = async (amount: number) => {
  // 如果当前是代币交易，则不计算可购买代币数量
  if (isTokenPurchase.value) return
  // 输入为空，或者输入的数量为0，清除计算的代币数量
  if (!amount) {
    return (estimatedTokenPurchase.value = 0)
  }
  // 如果输入的数量小于0 或 大于余额
  if (amount > Number(walletStore.wallet.balance ?? 0)) return
  console.log(token.protocol.protocolId, buyAmount.value ?? 0)

  try {
    estimatedTokenPurchase.value =
      (await estimateTokenPurchase(token.protocol.protocolId, amount ?? 0)) ?? 0

    console.log(estimatedTokenPurchase.value, buyErrorMessage.value)
  } catch (error) {
    console.error(error)
  }
}

const sellAmount = ref<number | null>(null)
// 快捷输入卖出代币数量
const handleSellAmount = (percentage: number) => {
  sellAmount.value = tokenBalance.value * percentage
}

// 重置快捷输入
const handleReset = () => {
  buyAmount.value = null
  sellAmount.value = null
}

// 计算使用余额可购买代币数量
const calcCanPurchaseAmount = async () => {
  try {
    return (
      (await estimateTokenPurchase(
        token.protocol.protocolId,
        Number(walletStore.wallet.balance ?? 0)
      )) ?? 0
    )
  } catch (error) {
    console.error(error)

    return 0
  }
}

// 购买代币操作
const handleBuy = async () => {
  let notify = null
  if (!Number(walletStore.wallet.balance ?? 0) || buyErrorMessage.value) return
  try {
    if (walletStore.accessToken) {
      // 展示交易Progress
      notify = progressNotify()
      // 购买代币
      const receipt = await purchaseTokenWithCurrency(
        token.protocol.protocolId,
        buyAmount.value ?? 0
      )
      // 处理成功，例如更新余额或显示通知
      console.log('Purchase successful:', receipt)

      // 更新仓位
      const position = await getTokenBalance(token.protocol.address)
      await postMyPosition({
        position: Number(position ?? 0),
        token: token.id,
        account: walletStore.userInfo.id
      })

      // 隐藏ProgressNotify
      notify.destroy()

      // 提示成功
      simpleNotify('Transaction successful')

      // 重置表单
      buyAmount.value = null
    } else {
      showWalletModal.value = true
    }
  } catch (error) {
    console.error(error)
    notify?.destroy()
    simpleNotify('Transaction failed', 'fail')
  }
}

// 售卖代币操作
const handleSell = async () => {
  let notify = null
  if (!Number(walletStore.wallet.balance ?? 0) || sellErrorMessage.value) return
  try {
    if (walletStore.accessToken) {
      // 展示交易Progress
      notify = progressNotify()

      // 售卖代币
      console.log('sell amount', sellAmount.value)
      console.log('token address', token.protocol.address)
      const receipt = await sellTokenWithFanToken(token.protocol.protocolId, sellAmount.value ?? 0)
      // 处理成功，例如更新余额或显示通知
      console.log('Sell successful:', receipt)
      const position = await getTokenBalance(token.protocol.address)
      // 更新仓位
      tokenBalance.value = +position
      await postMyPosition({
        position: Number(position ?? 0),
        token: token.id,
        account: walletStore.userInfo.id
      })

      // 隐藏ProgressNotify
      notify.destroy()

      // 提示成功
      simpleNotify('Transaction successful')

      // 重置表单
      sellAmount.value = null
    } else {
      showWalletModal.value = true
    }
  } catch (error) {
    console.error(error)
    notify?.destroy()
    simpleNotify('Transaction failed', 'fail')
  }
}

// 监听切换buy/sell，重置amount
watch(tradeType, async () => {
  if (tradeType.value === 'sell') {
    sellAmount.value = null
    const position = await getTokenBalance(token.protocol.address)
    tokenBalance.value = +position
  } else {
    buyAmount.value = null
  }
})

// 监听token变化，更新价格等
watch(
  () => token.protocol.id,
  async () => {
    const bondingCurveInfo = await getBondingCurveInfo(token.protocol.protocolId)

    token.protocol.price = +bondingCurveInfo.price
    token.protocol.marketValue = +bondingCurveInfo.marketValue
    token.protocol.bondingCurve = bondingCurveInfo.bondingCurveProgress
  },
  {
    immediate: true
  }
)

// 监听钱包余额变化，更新可购买代币数量
watch(
  () => walletStore.wallet.balance,
  async () => {
    maxTokenBuyBalance.value = await calcCanPurchaseAmount()
    console.log('calcCanPurchaseAmount', maxTokenBuyBalance.value)
  }
)

onMounted(() => {
  nextTick(async () => {
    // 计算可购买代币数量
    maxTokenBuyBalance.value = await calcCanPurchaseAmount()
  })
})
</script>

<template>
  <div class="trading-panel">
    <div class="trading-panel__top">
      <div class="trading-view">
        <chart :id="token.protocol.id"></chart>
      </div>
      <div class="trading-board">
        <div class="trading-board__top">
          <n-tabs
            v-model:value="tradeType"
            type="segment"
            :animated="false"
            style="
              --n-color-segment: rgba(255, 255, 255, 0.03);
              --n-tab-text-color: rgba(255, 255, 255, 0.3);
              --n-tab-text-color-active: #fff;
              --n-tab-text-color-hover: rgba(255, 255, 255, 0.8);
              --n-tab-border-radius: 12px;
              --n-tab-font-size: 16px;
              --n-tab-padding: 9px 0;
              --n-pane-padding-top: 32px;
            "
            :style="{ '--n-tab-color-segment': tradeType === 'buy' ? '#00a878' : '#DA4354' }"
          >
            <n-tab-pane name="buy" tab="Buy">
              <div class="trade-wrapper">
                <div class="tokens-wrapper">
                  <!-- <div class="switch">
                    <div>
                      <SvgIcon name="settings"></SvgIcon>
                      <span>Set max slippage</span>
                    </div>
                    <div @click="handleSwitch">
                      <SvgIcon name="switch"></SvgIcon>
                      <span v-if="!isTokenPurchase">{{ `Switch to ${token.ticker}` }}</span>
                      <span v-else>Switch to EPT</span>
                    </div>
                  </div> -->
                  <div
                    class="input-wrapper"
                    :class="{ active: isInputFocused }"
                    @click="handleFocus"
                  >
                    <div class="tokens__left">
                      <input
                        ref="inputRef"
                        class="input"
                        type="text"
                        v-model="buyAmount"
                        placeholder="Enter the number of Tokens"
                        @keydown="handleKeyDown"
                        @change="handleEstimate(buyAmount ?? 0)"
                        @focus="isInputFocused = true"
                        @blur="isInputFocused = false"
                      />

                      <div class="balance">
                        <div class="text">Balance:</div>
                        <div class="amount" v-if="!isTokenPurchase">
                          {{
                            `${formatAmount(Number(walletStore.wallet.balance ?? 0).toFixed(4))} ${token.protocol.symbol}`
                          }}
                        </div>
                        <div class="amount" v-else>
                          {{
                            `${formatAmount(Number(maxTokenBuyBalance ?? 0).toFixed(4))} ${token.ticker}`
                          }}
                        </div>
                      </div>
                    </div>
                    <div class="tokens__right">
                      <template v-if="isTokenPurchase">
                        <div class="img-wrapper">
                          <img :src="token.logo" alt="" />
                        </div>
                        <div class="text">{{ token.ticker }}</div>
                      </template>
                      <template v-else>
                        <SvgIcon name="ept"></SvgIcon>
                        <div class="text">EPT</div>
                      </template>
                    </div>
                  </div>
                  <div v-if="!!buyErrorMessage" class="error">{{ buyErrorMessage }}</div>
                  <!-- <div
                    class="estimate"
                    v-if="!isTokenPurchase && !buyErrorMessage && estimatedTokenPurchase"
                  >
                    {{
                      `You will receive ${formatAmount(Number(estimatedTokenPurchase ?? 0).toFixed(4))} ${token.ticker}`
                    }}
                  </div> -->
                </div>
                <div class="shortcut__wrapper" v-if="!isTokenPurchase">
                  <div class="shortcut">
                    <div class="item" @click="handleShortcut(30)">30 EPT</div>
                    <div class="item" @click="handleShortcut(90)">90 EPT</div>
                    <div class="item" @click="handleShortcut(270)">270 EPT</div>
                  </div>
                  <div class="reset" @click="handleReset">Reset</div>
                </div>
                <div class="action">
                  <div
                    :class="{ disabled: !Number(walletStore.wallet.balance ?? 0) }"
                    class="button button-create buy"
                    @click="handleBuy"
                  >
                    Buy
                  </div>
                </div>
              </div>
            </n-tab-pane>
            <n-tab-pane name="sell" tab="Sell">
              <div class="trade-wrapper">
                <div class="tokens-wrapper">
                  <!-- <div class="switch">
                    <div @click="handleSwitch">
                      <SvgIcon name="settings"></SvgIcon>
                      <span>Set max slippage</span>
                    </div>
                    <div @click="handleSwitch">
                      <SvgIcon name="switch"></SvgIcon>
                      <span>Switch to MouMou</span>
                    </div>
                  </div> -->
                  <div class="input-wrapper" @click="handleFocus">
                    <div class="tokens__left">
                      <input
                        ref="inputRef"
                        class="input"
                        type="text"
                        v-model="sellAmount"
                        placeholder="Enter the number of Tokens"
                      />
                      <div class="balance">
                        <div class="text">Balance:</div>
                        <div class="amount">
                          {{
                            `${formatAmount(Number(tokenBalance ?? 0).toFixed(4))} ${token.ticker}`
                          }}
                        </div>
                      </div>
                    </div>
                    <div class="tokens__right">
                      <div class="img-wrapper">
                        <img :src="token.logo" alt="" />
                      </div>
                      <div class="text">{{ token.ticker }}</div>
                    </div>
                  </div>
                  <div v-if="!!sellErrorMessage" class="error">{{ sellErrorMessage }}</div>
                </div>
                <div class="shortcut__wrapper">
                  <div class="shortcut">
                    <div class="item" @click="handleSellAmount(0.25)">25%</div>
                    <div class="item" @click="handleSellAmount(0.5)">50%</div>
                    <div class="item" @click="handleSellAmount(0.75)">75%</div>
                    <div class="item" @click="handleSellAmount(1)">100%</div>
                  </div>
                  <div class="reset" @click="handleReset">Reset</div>
                </div>
                <div class="action">
                  <div
                    :class="{ disabled: !Number(walletStore.wallet.balance ?? 0) }"
                    class="button button-create sell"
                    @click="handleSell"
                  >
                    Sell
                  </div>
                </div>
              </div>
            </n-tab-pane>
          </n-tabs>
        </div>
        <div class="trading-board__bottom">
          <div class="boarding-curve">
            Bonding curve progress:
            <span class="amount">{{ `${token.protocol.bondingCurve}%` }}</span>
          </div>
          <n-progress
            type="line"
            :percentage="+token.protocol.bondingCurve"
            :show-indicator="false"
            color="#fff"
            rail-color="rgba(255, 255, 255, 0.05)"
            :height="8"
          />
          <div class="boarding-desc">
            graduate this coin to Fans Protocol at $104,522 market cap(414 EPT remaining in bonding
            curve)
          </div>
        </div>
      </div>
    </div>
    <WalletDialog v-model="showWalletModal"></WalletDialog>
  </div>
</template>

<style lang="scss" scoped>
.trading-panel {
  &__top {
    display: flex;
    padding: 24px 40px;
    align-items: center;
    gap: 40px;

    .trading-view {
      flex: 1;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.03);
      box-shadow: 0px 0px 19.2px 0px rgba(77, 77, 77, 0.06);
      height: 570px;
      width: 1326px;
      overflow: hidden;
    }

    .trading-board {
      display: flex;
      width: 480.215px;
      flex-direction: column;
      align-items: flex-start;
      gap: 32px;
      flex-shrink: 0;
      align-self: stretch;

      &__top {
        display: flex;
        padding: 24px;
        flex-direction: column;
        align-items: center;
        gap: 32px;
        align-self: stretch;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.03);
        box-shadow: 0px 0px 19.2px 0px rgba(77, 77, 77, 0.06);

        :deep(.n-tabs) {
          .n-tabs-rail {
            padding: 8px;
          }

          .n-tabs-capsule {
            border-radius: 8px;
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
            justify-content: space-between;
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
            border: 1px solid rgba(255, 255, 255, 0.25);
            background: #111;
            will-change: border-color;

            &:hover {
              border-color: rgba(255, 255, 255, 0.28);

              .input::placeholder {
                transition: color 0.3s ease-in-out;
                color: rgba(255, 255, 255, 0.75);
              }
            }

            &.active {
              transition: border-color 0.3s ease-in-out;
              border-color: rgba(255, 255, 255, 0.5);

              .input::placeholder {
                color: rgba(255, 255, 255, 0.75);
              }
            }

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
                    color: rgba(255, 255, 255, 0.3);
                    font-family: Sora;
                    font-size: 12px;
                    font-style: normal;
                    font-weight: 300;
                    line-height: 16px; /* 133.333% */
                  }

                  .amount {
                    color: rgba(255, 255, 255, 0.65);
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

                .svg-icon {
                  width: 24px;
                  height: 24px;
                }

                .img-wrapper {
                  width: 24px;
                  height: 24px;
                  border-radius: 100%;
                  overflow: hidden;
                }

                img {
                  object-fit: cover;
                  object-position: center;
                  width: 100%;
                  height: 100%;
                }

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

          .estimate {
            position: absolute;
            bottom: -24px;
            font-size: 14px;
            line-height: 1.5;
            color: rgba(#ffffff, 0.3);
          }
        }

        .shortcut__wrapper {
          margin-top: 32px;
          display: flex;
          width: 100%;
          justify-content: space-between;
          align-items: center;

          .shortcut {
            display: flex;
            align-items: center;
            gap: 12px;
          }

          .item,
          .reset {
            display: flex;
            height: 28px;
            padding: 0px 12px;
            justify-content: center;
            align-items: center;
            border-radius: 40px;
            background: rgba(255, 255, 255, 0.03);

            color: rgba(255, 255, 255, 0.3);

            /* Labels/S/Regular */
            font-family: Sora;
            font-size: 12px;
            font-style: normal;
            font-weight: 400;
            line-height: 16px; /* 133.333% */
            cursor: pointer;

            &:hover {
              color: rgba(255, 255, 255, 0.5);
              background: rgba(255, 255, 255, 0.28);
            }

            &:active {
              color: rgba(255, 255, 255, 0.7);
              background: rgba(255, 255, 255, 0.5);
            }
          }
        }

        .action {
          margin-top: 32px;
        }

        .button {
          width: 100%;
          border-radius: 80px;
          box-shadow: 0px 0px 9.9px 0px #111;
          color: #fff;

          &.buy {
            background: #00a878;
          }

          &.buy:hover {
            background: rgba(#00a878, 0.8);
          }

          &.buy:active {
            background: rgba(#00a878, 0.75);
          }

          &.buy.disabled {
            background: rgba(#00a878, 0.5);
            cursor: not-allowed;
          }

          &.sell {
            background: #da4354;
          }

          &.sell:hover {
            background: rgba(#da4354, 0.8);
          }

          &.sell:active {
            background: rgba(#da4354, 0.75);
          }

          &.sell.disabled {
            background: rgba(#da4354, 0.5);
            cursor: not-allowed;
          }
        }
      }

      &__bottom {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
        align-self: stretch;

        .boarding-curve {
          color: rgba(255, 255, 255, 0.85);

          /* H6/Semibold */
          font-family: Sora;
          font-size: 20px;
          font-style: normal;
          font-weight: 600;
          line-height: 28px; /* 140% */

          span {
            font-size: 24px;
            line-height: 32px;
          }
        }

        .boarding-desc {
          color: rgba(255, 255, 255, 0.3);
          text-shadow: 0px 0px 36.4px #000;

          /* Paragraphs/XS/Regular */
          font-family: Sora;
          font-size: 12px;
          font-style: normal;
          font-weight: 400;
          line-height: 20px; /* 166.667% */
        }
      }
    }
  }

  ::deep(.n-input-number) {
    .n-input {
      background: transparent;
    }

    .n-input-wrapper {
      background-color: red;
    }
  }
}
</style>
