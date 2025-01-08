<script lang="ts" setup>
import type { UploadFileInfo } from 'naive-ui'
import { updateAccount } from '@/apis'
import { useWalletStore } from '@/stores/wallet'
import { simpleNotify } from '@/utils'

interface Props {
  modelValue: boolean
}
const props = defineProps<Props>()

const walletStore = useWalletStore()

const form = reactive<{ avatar: File | undefined; name: string }>({
  avatar: undefined,
  name: walletStore.userInfo.name || ''
})

// 通过watch监听modelValue，实现数据的修改
const showModal = ref(false)
watch(
  () => props.modelValue,
  (newV) => {
    showModal.value = newV
  }
)

const showPreviewModal = ref(false)
const previewImageUrl = ref('')
const previewFileList = ref<UploadFileInfo[]>([])

if (walletStore.userInfo.avatar) {
  previewFileList.value = [
    {
      id: 'c',
      name: '我是自带url的图片.png',
      status: 'finished',
      url: walletStore.userInfo.avatar as string
    }
  ]
}

watch(
  () => walletStore.userInfo.avatar,
  (newV) => {
    if (newV) {
      previewFileList.value = [
        {
          id: 'c',
          name: '我是自带url的图片.png',
          status: 'finished',
          url: newV as string
        }
      ]
    }
  }
)

const emit = defineEmits(['update:modelValue'])

const handleBeforeUpload = (options: { file: UploadFileInfo; fileList: UploadFileInfo[] }) => {
  const { id, name, file } = options.file
  if ((file as File).size > 4 * 1024 * 1024) {
    simpleNotify('Image size must be less than 4MB', 'fail')
    return false
  }
  const URL = window.URL || window.webkitURL
  previewFileList.value = [
    {
      id,
      name,
      status: 'finished',
      url: URL.createObjectURL(file as File)
    }
  ]
  form.avatar = file as File

  return true
}

const handlePreview = (file: UploadFileInfo) => {
  const { url } = file
  previewImageUrl.value = url as string
  showPreviewModal.value = true
}

const handleSubmit = async () => {
  if (!form.avatar && !form.name) return

  try {
    const account = await updateAccount(form)
    walletStore.userInfo = account
    emit('update:modelValue', false)
    simpleNotify('Successfully updated')
  } catch (error) {
    console.error(error)
    emit('update:modelValue', false)
    simpleNotify('Failed to update profile', 'fail')
  }
}
</script>

<template>
  <n-modal
    class="custom-modal"
    v-model:show="showModal"
    transform-origin="center"
    @update:show="$emit('update:modelValue', false)"
  >
    <div class="modal-content">
      <div class="info">
        <div class="header">
          <div class="title">Edit Profile</div>
          <SvgIcon name="close" @click="$emit('update:modelValue', false)"></SvgIcon>
        </div>
        <div class="desc">You can change your username once every day</div>
        <div class="form">
          <div class="upload">
            <div class="label">Logo</div>
            <div class="value">
              <n-upload
                style="--n-border-radius: 12px"
                :max="1"
                :default-upload="false"
                :default-file-list="previewFileList"
                accept="image/*"
                list-type="image-card"
                @before-upload="handleBeforeUpload"
                @preview="handlePreview"
              >
                <SvgIcon name="add"></SvgIcon>
              </n-upload>
              <n-modal
                v-model:show="showPreviewModal"
                preset="card"
                style="width: 600px"
                title="预览"
              >
                <img :src="previewImageUrl" style="width: 100%" />
              </n-modal>
            </div>
            <div class="tip">*Please upload images in PNG, JPG, GIF formats Less than 4MB</div>
          </div>

          <Input
            label="User name"
            v-model="form.name"
            placeholder="Enter the User name"
            :length="10"
            type="text"
            :clearable="true"
          />

          <!-- <Input
            label="Bio"
            v-model="form.bio"
            placeholder="Option"
            :length="20"
            type="text"
            :clearable="true"
          /> -->
        </div>
      </div>
      <div class="action">
        <div
          class="button button-create"
          :class="{ disabled: !form.avatar && !form.name }"
          @click="handleSubmit"
        >
          Save
        </div>
        <!-- <div class="level">Previous level</div> -->
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
  align-items: center;
  gap: 64px;
  flex-shrink: 0;
  border-radius: 24px;
  background: #000;

  .info {
    width: 100%;
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
      margin-top: 32px;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 24px;
      align-self: stretch;

      .upload {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: flex-start;
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
          display: flex;
          width: 98px;
          height: 98px;
          justify-content: space-between;
          align-items: center;

          border-radius: 12px;
          border: 1.5px dashed var(--icon-Normal, #ededed);
          overflow: hidden;

          :deep(.n-upload) {
            .n-upload-file--image-card-type {
              width: 98px;
              height: 98px;
              border: none;
            }

            .n-upload-trigger.n-upload-trigger--image-card {
              width: 98px;
              height: 98px;
            }

            .n-upload-dragger {
              background: transparent;
              border: none;

              .svg-icon {
                width: 20px;
                height: 20px;
              }
            }
          }

          :deep(.n-image) {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 98px;
            height: 98px;

            img {
              width: 100%;
              height: 100%;
              object-fit: cover !important;
              object-position: center;
            }
          }
        }

        .tip {
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

      &.disabled {
        opacity: 0.3;
        cursor: not-allowed;
        pointer-events: none;
      }
    }

    .level {
      margin-top: 38px;
      color: #888;

      /* H6/Regular */
      font-family: Sora;
      font-size: 20px;
      font-style: normal;
      font-weight: 400;
      line-height: 28px; /* 140% */
    }
  }
}
</style>
