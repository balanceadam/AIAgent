<script setup lang="ts">
import type { UploadFileInfo, FormInst, FormRules, FormItemRule } from 'naive-ui'
import { useLaunchStore } from '@/stores/launch'
import { useWalletStore } from '@/stores/wallet'

const showLogoPreviewModal = ref(false)
const previewLogoImageUrl = ref('')
const previewLogoFileList = ref<UploadFileInfo[]>([
  // {
  //   id: 'c',
  //   name: '我是自带url的图片.png',
  //   status: 'finished',
  //   url: 'https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg'
  // }
])

const showFacePreviewModal = ref(false)
const previewFaceImageUrl = ref('')
const previewFaceFileList = ref<UploadFileInfo[]>([
  // {
  //   id: 'c',
  //   name: '我是自带url的图片.png',
  //   status: 'finished',
  //   url: 'https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg'
  // }
])

const formRef = ref<FormInst | null>(null)

const rules: FormRules = {
  name: [
    {
      required: true,
      trigger: ['input', 'blur'],
      message: 'Please enter the name of Tokens'
    }
  ],
  ticker: [
    {
      required: true,
      trigger: ['input', 'blur'],
      validator(rule: FormItemRule, value: string) {
        if (!value) {
          return new Error('Please enter the ticker of Tokens')
        } else if (!/^(?!.*__)[A-Za-z0-9_]{3,20}$/.test(value)) {
          return new Error('The ticker must be 3-20 characters and cannot contain __')
        }
        return true
      }
    }
  ],
  epalName: [
    {
      required: true,
      trigger: ['input', 'blur'],
      message: 'Please enter the Epal Name'
    }
  ],
  labels: [
    {
      required: true,
      trigger: ['input', 'blur'],
      message: 'Please enter the Game tags'
    }
  ],
  games: [
    {
      type: 'array',
      required: true,
      trigger: ['blur', 'change'],
      message: 'Please select the Game'
    }
  ],
  fillingServices: [
    {
      type: 'array',
      required: true,
      trigger: ['blur', 'change'],
      message: 'Please select the Filling Service'
    }
  ]
}

const logoValidationStatus = ref()

const logoFeedback = ref('')

const faceValidationStatus = ref()

const faceFeedback = ref('')

const launchStore = useLaunchStore()
const walletStore = useWalletStore()

watch(
  () => launchStore.launchForm.logo,
  () => {
    if (!launchStore.launchForm.logo) {
      logoValidationStatus.value = 'error'
      logoFeedback.value = 'Please upload the logo'
    } else {
      logoValidationStatus.value = ''
      logoFeedback.value = ''
    }
  }
)

watch(
  () => launchStore.launchForm.epal,
  () => {
    if (!launchStore.launchForm.epal) {
      faceValidationStatus.value = 'error'
      faceFeedback.value = 'Please upload the Face'
    } else {
      faceValidationStatus.value = ''
      faceFeedback.value = ''
    }
  }
)

const toggleCheck = (value: number) => {
  if (launchStore.launchForm.fillingServices.includes(value)) {
    launchStore.launchForm.fillingServices = launchStore.launchForm.fillingServices.filter(
      (item) => item !== value
    )
  } else {
    launchStore.launchForm.fillingServices.push(value)
  }
}

const handleBeforeUploadLogo = (options: { file: UploadFileInfo; fileList: UploadFileInfo[] }) => {
  const { id, name, file } = options.file
  const URL = window.URL || window.webkitURL
  previewLogoFileList.value = [
    {
      id,
      name,
      status: 'finished',
      url: URL.createObjectURL(file as File)
    }
  ]
  launchStore.launchForm.logo = file as File

  return true
}

const handlePreviewLogo = (file: UploadFileInfo) => {
  const { url } = file
  previewLogoImageUrl.value = url as string
  showLogoPreviewModal.value = true
}
const handleBeforeUploadFace = (options: { file: UploadFileInfo; fileList: UploadFileInfo[] }) => {
  const { id, name, file } = options.file
  const URL = window.URL || window.webkitURL
  previewFaceFileList.value = [
    {
      id,
      name,
      status: 'finished',
      url: URL.createObjectURL(file as File)
    }
  ]
  launchStore.launchForm.epal = file as File

  return true
}

const handlePreviewFace = (file: UploadFileInfo) => {
  const { url } = file
  previewFaceImageUrl.value = url as string
  showFacePreviewModal.value = true
}

const showInitialBuyModal = ref(false)
const showWalletDialog = ref(false)

const handleCreate = async () => {
  // 判断是否登录
  if (!walletStore.accessToken) {
    showWalletDialog.value = true
    return
  }

  // 校验图片
  if (!launchStore.launchForm.logo) {
    logoValidationStatus.value = 'error'
    logoFeedback.value = 'Please upload the logo'
  } else {
    logoValidationStatus.value = ''
    logoFeedback.value = ''
  }
  if (!launchStore.launchForm.epal) {
    faceValidationStatus.value = 'error'
    faceFeedback.value = 'Please upload the Face'
  } else {
    faceValidationStatus.value = ''
    faceFeedback.value = ''
  }

  // 校验表单
  formRef.value?.validate(async (errors) => {
    if (errors || !launchStore.launchForm.logo || !launchStore.launchForm.epal) return

    const isInWhitelist = await launchStore.getInWhitelist()

    // 判断是否在白名单中
    if (!isInWhitelist) {
      window.$message?.error('You are not in the whitelist')
      return
    }

    // 验证表单
    const valid = await launchStore.validateForm()
    console.log(valid)

    if (!valid) {
      window.$message?.error('The form is not valid')
      return
    }

    showInitialBuyModal.value = true
  })
}

const logoUploadRef = ref()
const faceUploadRef = ref()

// 创建token成功后，重置upload
const handleChange = () => {
  launchStore.launchForm.logo = null
  launchStore.launchForm.epal = null

  logoUploadRef.value?.clear()
  faceUploadRef.value?.clear()
  previewLogoFileList.value = []
  previewFaceFileList.value = []
  previewLogoImageUrl.value = ''
  previewFaceImageUrl.value = ''

  setTimeout(() => {
    logoValidationStatus.value = ''
    logoFeedback.value = ''
    faceValidationStatus.value = ''
    faceFeedback.value = ''
  }, 100)
}

watch(
  () => walletStore.accessToken,
  (newV) => {
    if (newV) {
      launchStore.getFillingServiceList()
      launchStore.getGamesList()
      launchStore.getChainList()
    }
  },
  { immediate: true }
)
</script>
<template>
  <div class="page-view launch">
    <div class="header">
      <div class="left">
        Launch your <br />
        Token on Balanpump
      </div>
      <div class="right">
        <div class="item">
          <SvgIcon name="presale"></SvgIcon>
          <div class="desc">No Presale</div>
        </div>
        <div class="item">
          <SvgIcon name="allocation"></SvgIcon>
          <div class="desc">No Team Allocation</div>
        </div>
        <div class="item">
          <SvgIcon name="gas"></SvgIcon>
          <div class="desc">Lower Gas</div>
        </div>
      </div>
    </div>

    <n-form ref="formRef" :model="launchStore.launchForm" :rules="rules" class="content">
      <div class="left">
        <n-form-item
          :validation-status="faceValidationStatus"
          :feedback="faceFeedback"
          style="--n-label-height: 0"
        >
          <div class="upload">
            <div class="label">Face*</div>
            <div class="value image face">
              <n-upload
                ref="faceUploadRef"
                style="--n-border-radius: 12px"
                :max="1"
                :default-upload="false"
                :default-file-list="previewFaceFileList"
                accept="image/*"
                list-type="image-card"
                @before-upload="handleBeforeUploadFace"
                @preview="handlePreviewFace"
              >
                <SvgIcon name="add"></SvgIcon>
              </n-upload>
              <n-modal
                v-model:show="showFacePreviewModal"
                preset="card"
                style="width: 600px"
                title="预览"
              >
                <img :src="previewFaceImageUrl" style="width: 100%" />
              </n-modal>
            </div>
            <div class="tip">*Please upload images in PNG, JPG, GIF formats Less than 4MB</div>
            <div class="required">*Unchangeable</div>
          </div>
        </n-form-item>

        <n-form-item :validation-status="logoValidationStatus" :feedback="logoFeedback">
          <div class="upload">
            <div class="label">Token Logo*</div>
            <div class="value image token">
              <n-upload
                ref="logoUploadRef"
                style="--n-border-radius: 12px"
                :max="1"
                :default-upload="false"
                :default-file-list="previewLogoFileList"
                accept="image/*"
                list-type="image-card"
                @before-upload="handleBeforeUploadLogo"
                @preview="handlePreviewLogo"
              >
                <SvgIcon name="add"></SvgIcon>
              </n-upload>
              <n-modal
                v-model:show="showLogoPreviewModal"
                preset="card"
                style="width: 600px"
                title="预览"
              >
                <img :src="previewLogoImageUrl" style="width: 100%" />
              </n-modal>
            </div>
            <div class="tip">*Please upload images in PNG, JPG, GIF formats Less than 4MB</div>
            <div class="required">*Unchangeable</div>
          </div>
        </n-form-item>
      </div>
      <div class="right">
        <div class="top">
          <div class="user">
            <n-form-item :span="12" path="name" style="--n-label-height: 0">
              <Input
                label="Name*"
                v-model="launchStore.launchForm.name"
                placeholder="Enter the name of Tokens *Unchangeable"
                :length="20"
                type="text"
                :clearable="true"
              />
            </n-form-item>

            <n-form-item :span="12" path="ticker" style="--n-label-height: 0">
              <Input
                label="Ticker*"
                v-model="launchStore.launchForm.ticker"
                placeholder="Enter the ticker of Tokens *Unchangeable"
                :length="10"
                type="text"
                :clearable="true"
              />
            </n-form-item>
          </div>
          <Input
            class="desc"
            label="Description"
            v-model="launchStore.launchForm.description"
            placeholder="Enter the descriptionof Tokens"
            :length="500"
            type="textarea"
            :clearable="true"
            :autosize="{ minRows: 8, maxRows: 10 }"
          />
          <div class="chain">
            <ChainSelect
              label="Selection Chain*"
              v-model="launchStore.launchForm.chain"
            ></ChainSelect>
            <n-form-item :span="12" path="epalName" style="--n-label-height: 0">
              <Input
                label="Epal Name*"
                v-model="launchStore.launchForm.epalName"
                placeholder="Enter the Epal Name *Unchangeable"
                :length="20"
                type="text"
                :clearable="true"
              />
            </n-form-item>
          </div>
        </div>
        <div class="center">
          <div class="row">
            <Input
              label="Telegram"
              v-model="launchStore.launchForm.telegram"
              placeholder="Optional"
              type="text"
              :clearable="true"
            />
            <Input
              label="Website"
              v-model="launchStore.launchForm.website"
              placeholder="Optional"
              type="text"
              :clearable="true"
            />
            <Input
              label="Twitter"
              v-model="launchStore.launchForm.twitter"
              placeholder="Optional"
              type="text"
              :clearable="true"
            />
          </div>
          <div class="row">
            <div class="col">
              <n-form-item :span="12" path="labels" style="--n-label-height: 0">
                <Input
                  label="Gamer tag*"
                  v-model="launchStore.launchForm.labels"
                  placeholder="Use # to distinguish input tags *Unchangeable"
                  :length="50"
                  type="text"
                  :clearable="true"
                />
              </n-form-item>
            </div>
            <div class="col">
              <n-form-item :span="12" path="games" style="--n-label-height: 0">
                <GameSelect
                  label="Selection Game*"
                  v-model="launchStore.launchForm.games"
                ></GameSelect>
              </n-form-item>
            </div>
            <div class="col"></div>
          </div>
        </div>
        <div class="bottom">
          <div class="label">Filling Service</div>
          <n-form-item path="fillingServices" style="--n-label-height: 0">
            <n-checkbox-group
              class="checkbox-group"
              v-model:value="launchStore.launchForm.fillingServices"
            >
              <div
                class="item"
                v-for="item in launchStore.fillingServiceList"
                :key="item.id"
                :class="{ active: launchStore.launchForm.fillingServices.includes(item.id) }"
                @click="toggleCheck(item.id)"
              >
                <div class="item__top">
                  <img :src="item.logo" alt="" />
                  <n-checkbox
                    style="
                      --n-color: transparent;
                      --n-border: 2px solid rgba(255, 255, 255, 0.3);
                      --n-border-radius: 4px;
                      --n-border-checked: 2px solid rgba(255, 255, 255, 0.5);
                      --n-check-mark-color: #1e1e22;
                      --n-border-focus: rgba(255, 255, 255, 0.85);
                      --n-color-checked: #fff;
                      --n-box-shadow-focus: 0 0 0 2px transparent;
                    "
                    :value="item.id"
                    @click="toggleCheck(item.id)"
                  />
                </div>
                <div class="item__bottom">
                  <div class="title">{{ item.name }}</div>
                  <div class="desc">
                    {{ item.description }}
                  </div>
                </div>
              </div>
            </n-checkbox-group>
          </n-form-item>
        </div>
        <div class="footer">
          <div class="button button-create" @click="handleCreate">
            <span>Let's Create Token</span>
            <SvgIcon name="arrow-right"></SvgIcon>
          </div>
          <div class="notice">
            <SvgIcon name="coin"></SvgIcon>
            <span>Cost to deploy 50 EPT</span>
          </div>
        </div>
      </div>
    </n-form>
    <InitialBuyDialog
      v-model="showInitialBuyModal"
      @createSuccess="handleChange"
    ></InitialBuyDialog>
    <WalletDialog v-model="showWalletDialog"></WalletDialog>
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

    .left {
      color: #fff;

      /* Display1/Regular */
      font-family: Sora;
      font-size: 52px;
      font-style: normal;
      font-weight: 400;
      line-height: 64px; /* 123.077% */
    }

    .right {
      display: flex;
      align-items: center;
      gap: 32px;
      align-self: stretch;

      .item {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 8px;
        flex: 1 0 0;
        align-self: stretch;
        width: 238px;

        .svg-icon {
          width: 100px;
          height: 100px;
        }

        .desc {
          color: #888;
          text-align: center;

          /* Paragraphs/XS/Light */
          font-family: Sora;
          font-size: 12px;
          font-style: normal;
          font-weight: 300;
          height: 40px;
        }
      }
    }
  }

  .content {
    display: flex;
    width: 100%;
    padding: 40px;
    justify-content: space-between;
    align-items: flex-start;
    gap: 40px;

    .upload {
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      align-items: flex-start;
      gap: 16px;

      & + .upload {
        margin-top: 64px;
      }

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
        display: flex;
        width: 180px;
        height: 180px;
        justify-content: space-between;
        align-items: center;

        border-radius: 12px;
        overflow: hidden;

        :deep(.n-upload) {
          .n-upload-file--image-card-type {
            width: 180px;
            height: 180px;
            border: none;
          }

          .n-upload-trigger.n-upload-trigger--image-card {
            width: 180px;
            height: 180px;
          }

          .n-upload-dragger {
            background: transparent;
            border: none;

            .svg-icon {
              display: none;
              width: 36px;
              height: 36px;
            }
          }

          img {
            object-fit: cover !important;
          }
        }

        &.face {
          background-image: url('@/assets/images/bg-face.png');
          background-size: cover;
          background-position: center;
        }

        &.token {
          width: 120px;
          height: 120px;
          border-radius: 100%;
          background-image: url('@/assets/images/bg-token.png');
          background-size: cover;
          background-position: center;

          :deep(.n-upload) {
            .n-upload-file--image-card-type {
              width: 120px;
              height: 120px;
              border: none;
            }

            .n-upload-trigger.n-upload-trigger--image-card {
              width: 120px;
              height: 120px;
            }

            .n-upload-dragger {
              .svg-icon {
                width: 24px;
                height: 24px;
              }
            }
          }
        }
      }

      .tip,
      .required {
        margin-top: -4px;
        width: 160px;
        color: var(--, rgba(255, 255, 255, 0.3));
        text-shadow: 0px 0px 36.4px #000;

        /* Paragraphs/XS/Light */
        font-family: Sora;
        font-size: 12px;
        font-style: normal;
        font-weight: 300;
        line-height: 20px; /* 166.667% */
        opacity: 0.7;
      }

      .required {
        margin-top: -16px;
      }
    }

    :deep(.n-form-item-blank--error .image) {
      border: 1px solid #d03050;
    }

    .right {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 64px;
      flex-shrink: 0;
      flex: 1;

      .top {
        display: flex;
        align-items: flex-start;
        gap: 40px;
        align-self: stretch;

        .user {
          display: flex;
          flex-direction: column;
          flex: 1;
          gap: 8px;
        }

        .desc {
          display: flex;
          flex-direction: column;
          gap: 16px;
          flex: 1;

          .select-wrapper {
            width: 100%;
          }
        }

        .chain {
          display: flex;
          flex-direction: column;
          gap: 32px;
          flex: 1;

          .select-wrapper {
            width: 100%;
          }
        }
      }

      .center {
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

      .bottom {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
        align-self: stretch;

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

        .checkbox-group {
          display: flex;
          align-items: stretch; /* 使子项等高 */
          align-content: center;
          gap: 40px;
          align-self: stretch;
          flex-wrap: wrap;
        }

        .item {
          display: flex;
          padding: 16px;
          flex-direction: column;
          align-items: flex-start;
          gap: 20px;
          flex: 1 0 0;
          border-radius: 12px;
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid transparent;
          cursor: pointer;

          .item__top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            align-self: stretch;
            width: 100%;

            .svg-icon {
              width: 30px;
              height: 30px;
              color: #fff;
            }
          }

          .item__bottom {
            .title {
              color: rgba(255, 255, 255, 0.5);
              text-shadow: 0px 0px 36.4px #000;

              /* Labels/M/Light */
              font-family: Sora;
              font-size: 14px;
              font-style: normal;
              font-weight: 300;
              line-height: 18px; /* 128.571% */
            }

            .desc {
              margin-top: 8px;
              color: rgba(255, 255, 255, 0.3);
              text-shadow: 0px 0px 36.4px #000;

              /* Paragraphs/XS/Light */
              font-family: Sora;
              font-size: 12px;
              font-style: normal;
              font-weight: 300;
              line-height: 20px; /* 166.667% */
              opacity: 0.7;
            }
          }

          &:hover {
            border: 1px solid var(---Normal, rgba(255, 255, 255, 0.3));
          }

          &:active,
          &.active {
            border: 1px solid var(---Normal, rgba(255, 255, 255, 0.75));
          }
        }
      }

      .footer {
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;

        .notice {
          padding: 4px 8px;
          display: flex;
          align-items: center;
          gap: 4px;
          justify-content: center;
          align-items: center;
          border-radius: 8px;
          background: var(--GB-GB-Yellow-BG, rgba(255, 212, 105, 0.1));

          /* Paragraphs/XS/Light */
          color: var(--GB-GB-Yellow, #ffd469);

          /* Paragraphs/XS/Light */
          font-family: Sora;
          font-size: 12px;
          font-style: normal;
          font-weight: 300;
          line-height: 20px; /* 166.667% */

          .svg-icon {
            width: 16px;
            height: 16px;
          }
        }

        .button-create {
          width: 560px;
        }
      }
    }
  }
}
</style>
