<script setup lang="ts">
import { useLaunchStore } from '@/stores/launch'
import { useAssetsStore } from '@/stores/assets'
import type { AssetsToken } from '@/types'
import type { FormRules } from 'naive-ui'
import { postAssetsToken } from '@/apis'

const assetsStore = useAssetsStore()
const launchStore = useLaunchStore()

const token = ref<AssetsToken>({
  id: 0,
  account: 0,
  chain: {
    id: 0,
    name: '',
    fee: 0,
    symbol: ''
  },
  fillingServices: [],
  games: [],
  protocol: {
    address: '',
    price: 0,
    protocolId: 0,
    symbol: '',
    id: 0,
    bondingCurve: 0,
    marketValue: 0,
    dayIncrease: 0,
    dayTradingVolume: 0,
    createdAt: '',
    updatedAt: ''
  },
  name: '',
  ticker: '',
  website: '',
  twitter: '',
  telegram: '',
  description: '',
  labels: '',
  logo: '',
  epal: '',
  isEnabled: false,
  createdAt: '',
  updatedAt: ''
})

const rules: FormRules = {
  games: [
    {
      type: 'array',
      required: true,
      trigger: ['blur', 'change'],
      message: 'Please select the Game'
    }
  ]
}

const router = useRouter()

const handleEdit = async () => {
  await launchStore.submitEdit(token.value.id).then(() => {
    router.push('/me')
  })
}

const init = async () => {
  try {
    const tokens = await assetsStore.getMineTokens()
    await launchStore.getGamesList()
    token.value = tokens[0]
    launchStore.editForm.games = []
    token.value.games.forEach((game) => {
      launchStore.editForm.games.push(game.id)
    })
    launchStore.editForm.labels = token.value.labels
    launchStore.editForm.telegram = token.value.telegram
    launchStore.editForm.website = token.value.website
    launchStore.editForm.twitter = token.value.twitter
    launchStore.editForm.labels = token.value.labels
  } catch (error) {
    window.$message.error('Something went wrong, please try again later')
  }
}

init()

</script>
<template>
  <div class="page-view launch">
    <div class="header">
      <div class="left">
        Edit your Epal Information
      </div>
    </div>
    <n-form ref="formRef" :model="launchStore.editForm" :rules="rules" class="content">
      <div class="top">
        <div class="row">
          <Input
            label="Telegram"
            v-model="launchStore.editForm.telegram"
            placeholder="Optional"
            type="text"
            :clearable="true"
          />
          <Input
            label="Website"
            v-model="launchStore.editForm.website"
            placeholder="Optional"
            type="text"
            :clearable="true"
          />
          <Input
            label="Twitter"
            v-model="launchStore.editForm.twitter"
            placeholder="Optional"
            type="text"
            :clearable="true"
          />
        </div>
        <div class="row">
          <div class="col">
            <Input
              label="Gamer tag"
              v-model="launchStore.editForm.labels"
              placeholder="Use # to distinguish input tags"
              :length="50"
              type="text"
              :clearable="true"
            />
          </div>
          <div class="col">
            <n-form-item :span="12" path="games" style="--n-label-height: 0">
              <GameSelect
                label="Selection Game*"
                v-model="launchStore.editForm.games"
              ></GameSelect>
            </n-form-item>
          </div>
        </div>
      </div>
      <div class="footer">
        <div class="button button-create" @click="handleEdit()">
          <span>Save</span>
        </div>
      </div>
    </n-form>
  </div>
</template>

<style scoped lang="scss">
.page-view {
  .header {
    display: flex;
    width: 100%;
    padding: 40px;
    justify-content: space-between;
    align-items: center;
    color: #fff;

    /* Display1/Regular */
    font-family: Sora;
    font-size: 52px;
    font-style: normal;
    font-weight: 400;
    line-height: 64px; /* 123.077% */
  }

  .content {
    width: 100%;
    padding: 40px;
    justify-content: space-between;
    align-items: flex-start;
    gap: 40px;

    :deep(.n-form-item-blank--error .image) {
      border: 1px solid #d03050;
    }

    .top {
      display: flex;
      flex-direction: column;
      gap: 32px;
      width: 100%;

      .row {
        display: flex;
        align-items: flex-start;
        gap: 40px;
        align-self: stretch;

        .col {
          flex: 1;
          overflow: hidden;

          .n-form-item {
            width: 100%;

            &-blank {
              width: 100%;
            }

            .game-select-wrapper {
              width: 100%;
            }
          }
        }
      }
    }

    .footer {
      margin-top: 60px;
      justify-content: end;
      align-items: end;
      display: flex;

      .button-create {
        display: flex;
        width: 560px;
        height: 56px;
        padding: 0px 16px;
        justify-content: center;
        align-items: center;
        gap: 8px;
      }
    }
  }
}
</style>
