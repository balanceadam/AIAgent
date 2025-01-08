<script lang="ts" setup>
import dayjs from 'dayjs'
import { useSocialStore } from '@/stores/social'
import { useAssetsStore } from '@/stores/assets'

const socialStore = useSocialStore()
const assetsStore = useAssetsStore()
const isLoading = ref(false)

const init = async () => {
  try {
    isLoading.value = true
    await socialStore.getCommentList(assetsStore.token.id)
    isLoading.value = false
  } catch (error) {
    isLoading.value = false
    console.error(error)
  }
}

init()
</script>

<template>
  <div class="comment-list">
    <empty v-if="!isLoading && !socialStore.comments.length" description="No comment yet"> </empty>
    <div class="comment-item" v-for="item in socialStore.comments" :key="item.id">
      <div class="comment-top">
        <div class="name-wrapper">
          <div class="avatar-wrapper">
            <img v-if="item.account.avatar" :src="item.account.avatar as string" alt="" />
            <SvgIcon v-else name="default-avatar"></SvgIcon>
          </div>

          <div class="name">{{ item.account.name }}</div>
        </div>
        <div class="time">{{ dayjs(item.createdAt).format('HH:mm:ss DD/MM/YYYY') }}</div>
      </div>
      <div class="comment-bottom">
        <div class="comment">
          {{ item.content }}
        </div>
        <div class="images-wrapper">
          <n-image-group>
            <div class="file-item" v-for="img in item.imgs" :key="img">
              <n-image :src="img" object-fit="cover" />
            </div>
          </n-image-group>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.comment-list {
  margin-top: 16px;
  padding-bottom: 120px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 20px;
  align-self: stretch;

  .empty-view {
    width: 100%;
  }

  .comment-item {
    display: flex;
    padding: 20px 0px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    align-self: stretch;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);

    .comment-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      align-self: stretch;

      .name-wrapper {
        display: flex;
        height: 24px;
        align-items: center;
        gap: 8px;

        .avatar-wrapper {
          display: flex;
          justify-content: center;
          align-items: center;
          width: 24px;
          height: 24px;
          border-radius: 40px;
          background: #ffffff26;
          overflow: hidden;

          img,
          .svg-icon {
            object-fit: cover;
            object-position: center;
            width: 100%;
            height: 100%;
            flex-shrink: 0;
          }
        }

        .name {
          color: rgba(255, 255, 255, 0.85);

          /* H6/Semibold */
          font-family: Sora;
          font-size: 20px;
          font-style: normal;
          font-weight: 600;
          line-height: 28px; /* 140% */
        }
      }

      .time {
        color: rgba(255, 255, 255, 0.3);

        /* Labels/M/Regular */
        font-family: Sora;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 18px; /* 128.571% */
      }
    }

    .comment-bottom {
      display: flex;
      padding-left: 32px;
      flex-direction: column;
      gap: 16px;
      align-self: stretch;

      .comment {
        color: rgba(255, 255, 255, 0.85);

        /* Paragraphs/M/Light */
        font-family: Sora;
        font-size: 16px;
        font-style: normal;
        font-weight: 300;
        line-height: 24px; /* 150% */
      }

      .images-wrapper {
        display: flex;
        align-items: center;
        gap: 24px;
        opacity: 0.8;

        :deep(.n-image) {
          width: 120px;
          height: 120px;
          overflow: hidden;

          img {
            object-fit: cover;
            object-position: center;
            width: 100%;
            height: 100%;
            flex-shrink: 0;
          }
        }
      }
    }
  }
}
</style>
