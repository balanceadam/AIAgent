<script lang="ts" setup>
import type { UploadFileInfo } from 'naive-ui'
import type { CommentParams } from '@/types'
import { useSocialStore } from '@/stores/social'
import { useAssetsStore } from '@/stores/assets'
import { simpleNotify } from '@/utils'
import data from 'emoji-mart-vue-fast/data/apple.json'
import 'emoji-mart-vue-fast/css/emoji-mart.css'
import { Picker, EmojiIndex } from 'emoji-mart-vue-fast/src'

const emojiIndex = new EmojiIndex(data)

const fileList = ref<string[]>([])
const params = reactive<CommentParams>({
  content: '',
  imgs: [],
  tokenId: 0
})

const socialStore = useSocialStore()
const assetsStore = useAssetsStore()

/**
 * 上传图片，并将图片路径添加到 fileList和imgs中
 * @param options
 */
const handleUpload = (options: { file: UploadFileInfo; fileList: UploadFileInfo[] }) => {
  const { file } = options.file
  const URL = window.URL || window.webkitURL
  fileList.value.push(URL.createObjectURL(file as File))
  params.imgs.push(file as File)

  return true
}

/**
 * 添加表情到评论内容中
 * @param emoji
 */
const addEmoji = (emoji: any) => {
  params.content += emoji.native
}

/**
 * 删除图片
 * @param index
 */
const handleDelete = (index: number) => {
  fileList.value.splice(index, 1)
  params.imgs.splice(index, 1)
}

/**
 * 提交评论
 */
const isSubmitting = ref(false)
const handleSubmit = async () => {
  // 防止重复提交
  if (isSubmitting.value) return

  params.tokenId = assetsStore.token.id
  if (!params.content) {
    return simpleNotify('Comment cannot be empty', 'fail')
  }

  // 组装formData
  const formData = new FormData()
  formData.append('content', params.content)
  params.imgs.forEach((item) => {
    formData.append('imgs', item)
  })
  formData.append('token_id', params.tokenId + '')

  try {
    isSubmitting.value = true
    // 提交评论
    await socialStore.postCommentInfo(formData)
    // 更新评论列表
    await socialStore.getCommentList(assetsStore.token.id)

    // 清空评论内容和图片列表
    params.content = ''
    fileList.value = []
    params.imgs = []
    isSubmitting.value = false
  } catch (error) {
    console.error(error)
    simpleNotify('Post comment failed', 'fail')
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="comment-post">
    <n-input
      v-model:value="params.content"
      type="textarea"
      placeholder="Say something? Dude!"
      :autosize="{ minRows: 1, maxRows: 10 }"
      :maxlength="200"
      clearable
      style="
        --n-color: rgba(255, 255, 255, 0.03);
        --n-color-focus: rgba(255, 255, 255, 0.03);
        --n-border: 1px solid rgba(255, 255, 255, 0.25);
        --n-border-hover: 1px solid rgba(255, 255, 255, 0.5);
        --n-border-focus: 1px solid rgba(255, 255, 255, 0.5);
        --n-placeholder-color: rgba(255, 255, 255, 0.3);
        --n-caret-color: rgba(255, 255, 255, 0.85);
        --n-text-color: rgba(255, 255, 255, 0.85);
        --n-height: 56px;
        --n-border-radius: 12px;
      "
    />
    <div class="actions">
      <div class="action-left">
        <n-popover trigger="hover" raw :show-arrow="false">
          <template #trigger>
            <div class="icon-wrapper">
              <svg-icon name="emoji" />
            </div>
          </template>

          <picker :data="emojiIndex" @select="addEmoji" />
        </n-popover>
        <n-upload
          multiple
          :max="5"
          accept="image/*"
          :default-upload="false"
          :show-file-list="false"
          @before-upload="handleUpload"
        >
          <div class="icon-wrapper">
            <svg-icon name="pic" />
          </div>
        </n-upload>
      </div>
      <div class="button button-send" @click="handleSubmit">Send</div>
    </div>
    <div class="file-list">
      <n-image-group>
        <div class="file-item" v-for="(item, index) in fileList" :key="index">
          <n-image :src="item" object-fit="cover" />
          <div class=""></div>
          <svg-icon name="close" class="close-icon" @click="handleDelete(index)" />
        </div>
      </n-image-group>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.comment-post {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 24px 0;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  .actions {
    width: 100%;
    display: flex;
    justify-content: space-between;

    .action-left {
      display: flex;
      align-items: center;
      gap: 16px;

      .icon-wrapper {
        position: relative;
        display: flex;
        width: 24px;
        height: 24px;
        padding: 12px;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;

        .svg-icon {
          width: 20px;
          height: 20px;
          flex-shrink: 0;
        }
      }

      .n-upload {
        display: flex;
      }
    }

    .button-send {
      display: flex;
      width: 120px;
      height: 44px;
      padding: 0px 16px;
      justify-content: center;
      align-items: center;
      gap: 10px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.05);

      color: #fff;

      /* Labels/L/Regular */
      font-family: Sora;
      font-size: 16px;
      font-style: normal;
      font-weight: 400;
      line-height: 20px; /* 125% */
      cursor: pointer;

      &:hover,
      &:active {
        background: rgba(255, 255, 255, 0.1);
      }
    }
  }

  .file-list {
    display: flex;
    align-items: center;
    gap: 24px;
    opacity: 0.8;

    .file-item {
      position: relative;

      :deep(.n-image) {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 120px;
        height: 120px;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          object-position: center;
        }
      }

      .svg-icon {
        position: absolute;
        top: -12px;
        right: -12px;
        width: 24px;
        height: 24px;
        cursor: pointer;
        border-radius: 100%;
        background: #fff;
      }
    }
  }
}
</style>
