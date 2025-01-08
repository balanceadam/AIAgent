<script setup lang="ts">
import type { AssetsToken } from '@/types'
import type { Follow } from '@/types'
import { useSocialStore } from '@/stores/social'
import { useWalletStore } from '@/stores/wallet'
import { useRoute } from 'vue-router'

const { getFollowInfo, getFollowedInfo, followAccount, unfollowAccount } = useSocialStore()
const { userInfo } = useWalletStore()
const route = useRoute()

interface Props {
  token: AssetsToken
}

const props = defineProps<Props>()

const followedLoaded = ref(false)
const followed = ref(false)
const activeTab = ref(1)
const fansCount = ref(0)
const followingCount = ref(0)
const tabItems = ref([
  {
    name: 0,
    label: 'Epal'
  },
  {
    name: 1,
    label: 'Fan Tokens'
  },
  {
    name: 2,
    label: `Fans(${fansCount.value})`
  },
  {
    name: 3,
    label: `Followed(${followingCount.value})`
  }
])

// 跳转媒体网站
const goToUrl = (url: string | undefined) => {
  if (url) window.open(url, '_blank')
}

const updateFollowCount = async () => {
  if (!props.token.account) {
    return
  }
  let data: Follow = {
    fansCount: 0,
    followingCount: 0
  }
  try {
    data = await getFollowInfo(props.token.account)
  } catch (error) {
    console.error(error)
  }
  fansCount.value = data.fansCount
  followingCount.value = data.followingCount
  tabItems.value = [
    {
      name: 0,
      label: 'Epal'
    },
    {
      name: 1,
      label: 'Fan Tokens'
    },
    {
      name: 2,
      label: `Fans(${fansCount.value})`
    },
    {
      name: 3,
      label: `Followed(${followingCount.value})`
    }
  ]
}

const updateFollowed = async () => {
  if (route.name !== 'me' && userInfo.id) {
    try {
      followed.value = await getFollowedInfo(props.token.account)
      followedLoaded.value = true
    } catch (error) {
      console.error(error)
    }
  }
}

const follow = async () => {
  try {
    if (route.name !== 'me' && userInfo.id) {
      followed.value = !followed.value
      await followAccount(props.token.account)
      await updateFollowed()
      await updateFollowCount()
      // TODO: 如果当前在fans或者Following页面，更新数据
    }
  } catch (error) {
    console.error(error)
  }
}

const unfollow = async () => {
  try {
    if (route.name !== 'me' && userInfo.id) {
      followed.value = false
      await unfollowAccount(props.token.account)
      await updateFollowed()
      await updateFollowCount()
    }
  } catch (error) {
    console.error(error)
  }
}

const router = useRouter()
const handleClick = () => {
  router.push({ name: 'epal-edit' })
}

onMounted(async () => {
  await updateFollowCount()
  await updateFollowed()
})
</script>
<template>
  <div class="epal-detail">
    <div class="me__header">
      <n-breadcrumb
        separator=">"
        style="
          --n-item-text-color: rgba(255, 255, 255, 0.3);
          --n-item-text-color-active: rgba(255, 255, 255, 0.85);
          --n-item-text-color-hover: rgba(255, 255, 255, 0.3);
          --n-item-text-color-pressed: rgba(255, 255, 255, 0.3);
        "
      >
        <n-breadcrumb-item v-if="$route.name === 'me'" :clickable="false"> Me </n-breadcrumb-item>
        <n-breadcrumb-item v-else @click="$router.go(-1)"> Epal Space </n-breadcrumb-item>
        <n-breadcrumb-item> {{ token.epalName }} </n-breadcrumb-item>
      </n-breadcrumb>
      <div class="me__wrapper">
        <div class="me__epal">
          <div class="me__epal-avatar">
            <img v-if="token.epal" :src="token.epal" alt="avatar" />
            <img v-else src="https://picsum.photos/300/300" alt="" />
            <div class="me__epal-cover"></div>
          </div>
          <div class="me__epal-box">
            <div class="me__epal-name">
              <div class="name">{{ token.epalName }}</div>
              <SvgIcon
                name="edit"
                v-if="token.account === userInfo.id"
                @click="handleClick()"
              ></SvgIcon>
              <div v-if="!followedLoaded" class="follow-hide"></div>
              <div
                class="follow"
                v-if="
                  followedLoaded &&
                  $route.name !== 'me' &&
                  token.account !== userInfo.id &&
                  !followed
                "
                @click="follow()"
              >
                <SvgIcon name="follow"></SvgIcon>
                <span>Follow</span>
              </div>
              <div
                class="unfollow"
                v-if="
                  followedLoaded &&
                  $route.name !== 'me' &&
                  token.account !== userInfo.id &&
                  followed
                "
                @click="unfollow()"
              >
                <SvgIcon name="unfollow"></SvgIcon>
                <span>UnFollow</span>
              </div>
            </div>
            <div class="me__epal-tags">
              <span
                class="me__epal-tag"
                v-for="tag in token.labels
                  ?.split('#')
                  .filter((item) => !!item)
                  .map((item) => item.trim())"
                :key="tag"
              >
                {{ tag }}
              </span>
            </div>
            <div class="me__epal-medias">
              <SvgIcon name="x" @click="goToUrl(token.twitter)"></SvgIcon>
              <SvgIcon name="telegram" @click="goToUrl(token.telegram)"></SvgIcon>
              <SvgIcon name="website" @click="goToUrl(token.website)"></SvgIcon>
            </div>
          </div>
        </div>
        <div class="me__tokens">
          <div class="me__tokens-header">
            <div class="me__tokens-info">
              <div class="me__tokens-logo">
                <img v-if="token.logo" :src="token.logo" alt="" />
                <img v-else src="https://picsum.photos/200/200" />
                <SvgIcon :name="`${token.chain.symbol.toLowerCase()}-2`"></SvgIcon>
              </div>
              <div class="me__tokens-name">
                <span class="label">{{ `$ ${token.name}` }}</span>
                <span class="value">{{ token.ticker }}</span>
              </div>
            </div>
            <div class="me__tokens-price">
              <span class="label">Market Cap</span>
              <span class="value">{{ `$ ${token.protocol.bondingCurve}` }}</span>
            </div>
            <div class="me__tokens-change">
              {{
                ` ${token.protocol.dayIncrease > 0 ? '+' : token.protocol.dayIncrease < 0 ? '-' : ''} ${(+token.protocol.dayIncrease).toFixed(2)}%`
              }}
            </div>
          </div>
          <div class="me__tokens-desc">
            {{ token.description }}
          </div>
          <div class="me__tokens-tags">
            <div class="me__tokens-tag" v-for="item in token.fillingServices" :key="item.id">
              <img v-if="item.logo" :src="item.logo" />
              <img v-else src="https://picsum.photos/100/100" />
              <span>{{ item.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="me__tabs">
      <Tabs v-model:model-value="activeTab" :tab-items="tabItems"></Tabs>
    </div>
    <div class="me__content">
      <div class="me__content-epal" v-if="activeTab === 0">
        <div class="game-wrapper" v-for="item in token.games" :key="item.id">
          <img :src="item.img" alt="" />
        </div>
      </div>
      <div v-if="activeTab === 1" class="me__content-token">
        <TradingPanel :token="token"></TradingPanel>
        <CommentPanel></CommentPanel>
      </div>
      <div v-if="activeTab === 2" class="me__content-fans">
        <Friends :account-id="token.account" :friend-type="'fans'" :show-follow="false"></Friends>
      </div>
      <div v-if="activeTab === 3" class="me__content-following">
        <Friends
          :account-id="token.account"
          :friend-type="'following'"
          :show-follow="false"
        ></Friends>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.me-view {
  color: #fff;
}
.me {
  &__header {
    display: flex;
    padding: 40px;
    flex-direction: column;
    align-items: flex-start;
    gap: 24px;
    align-self: stretch;
  }

  &__wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    align-self: stretch;
  }

  &__epal {
    display: flex;
    align-items: center;
    gap: 32px;

    &-avatar {
      position: relative;
      width: 192px;
      height: 192px;
      flex-shrink: 0;
      border-radius: 12px;
      overflow: hidden;

      img {
        object-position: center;
        object-fit: cover;
        width: 100%;
        height: 100%;
      }
    }

    &-cover {
      position: absolute;
      bottom: 0;
      width: 100%;
      height: 100%;
      border-radius: 0px 0px 5.053px 5.053px;
      opacity: 0.3;
      background: linear-gradient(180deg, rgba(0, 0, 0, 0) 14.47%, #000 100%);
    }

    &-box {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      gap: 32px;
    }

    &-name {
      display: flex;
      align-items: center;
      gap: 24px;

      .svg-icon {
        width: 40px;
        height: 40px;
        flex-shrink: 0;
        color: white;
        cursor: pointer;
      }

      .name {
        color: #fff;
        font-size: 52px;
        font-style: normal;
        font-weight: 800;
        line-height: 64px; /* 123.077% */
      }

      .follow-hide {
        width: 134px;
        height: 42px;
      }

      .follow {
        display: flex;
        gap: 8px;
        width: 134px;
        height: 42px;
        justify-content: center;
        align-items: center;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        cursor: pointer;

        span {
          display: block;
          color: #fff;

          /* Labels/L/Regular */
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 400;
          line-height: 20px; /* 125% */
        }

        .svg-icon {
          width: 20px;
          height: 20px;
          flex-shrink: 0;
        }

        &:hover {
          border-color: rgba(255, 255, 255, 0.5);
        }
      }

      .unfollow {
        display: flex;
        gap: 8px;
        width: 134px;
        height: 42px;
        justify-content: center;
        align-items: center;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        cursor: pointer;

        span {
          display: block;
          color: rgba(255, 255, 255, 0.3);
          /* Labels/L/Regular */
          font-family: Sora;
          font-size: 16px;
          font-style: normal;
          font-weight: 400;
          line-height: 20px; /* 125% */
        }

        .svg-icon {
          width: 20px;
          height: 20px;
          flex-shrink: 0;
        }

        &:hover {
          border-color: rgba(255, 255, 255, 0.5);
        }
      }
    }

    &-tags {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      align-self: stretch;
    }

    &-tag {
      padding: 8px;
      color: #fff;
      text-shadow: 0px 0px 2.9px #000;
      font-size: 14px;
      font-style: normal;
      font-weight: 600;
      line-height: 16px; /* 114.286% */
      opacity: 0.65;
      border-radius: 4px;
      background: #1d1d1d;
      box-shadow: 0px 0px 3.8px 0px rgba(0, 0, 0, 0.2);
      text-transform: capitalize;
    }

    &-medias {
      display: flex;
      align-items: center;
      gap: 24px;
      opacity: 0.85;

      .svg-icon {
        width: 24px;
        height: 24px;
        cursor: pointer;
      }
    }
  }

  &__tokens {
    display: flex;
    width: 670px;
    padding: 16px 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    background: #101010;
    border-radius: 12px;

    &-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      align-self: stretch;
    }

    &-info {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    &-logo {
      position: relative;
      display: flex;
      align-items: center;
      padding: 6px 6px 0px 0px;
      width: 60px;
      height: 60px;
      flex-shrink: 0;
      overflow: hidden;

      img {
        object-fit: cover;
        object-position: center;
        width: 100%;
        height: 100%;
        border-radius: 100%;
      }

      .svg-icon {
        position: absolute;
        right: 0;
        top: 0;
        width: 24px;
        height: 24px;
      }
    }

    &-name,
    &-price {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      gap: 2px;

      .label {
        color: rgba(255, 255, 255, 0.3);
        text-shadow: 0px 0px 36.4px #000;

        /* Paragraphs/S/Regular */
        font-family: Sora;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 22px; /* 157.143% */
      }

      .value {
        color: var(--GB-GB-White, #fff);
        text-shadow: 0px 0px 36.4px #000;
        font-size: 20px;
        font-style: normal;
        font-weight: 400;
        line-height: 28px; /* 140% */
      }
    }

    &-change {
      display: flex;
      padding: 8px;
      min-width: 80px;
      justify-content: center;
      align-items: center;
      border-radius: 40px;
      background: var(--BL-green-BG, rgba(0, 168, 120, 0.05));
      box-shadow: 0px 0px 5.4px 0px rgba(14, 14, 14, 0.39);
      color: var(--BL-green, #00a878);
      text-shadow: 0px 0px 15.5px rgba(0, 0, 0, 0.5);
      font-family: Sora;
      font-size: 16px;
      font-style: normal;
      font-weight: 600;
      line-height: 20px; /* 125% */
    }

    &-desc {
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

    &-tags {
      display: flex;
      align-items: center;
      align-content: center;
      gap: 16px;
      align-self: stretch;
      flex-wrap: wrap;
    }

    &-tag {
      display: flex;
      padding: 6px;
      align-items: center;
      gap: 8px;
      border-radius: 4px;
      background: #1d1d1d;

      img {
        width: 18px;
        height: 18px;
        fill: #fff;
        filter: drop-shadow(1px 1px 4px #0c0c0c);
        opacity: 0.3;
      }

      span {
        color: rgba(255, 255, 255, 0.3);
        font-family: Sora;
        font-size: 16px;
        font-style: normal;
        font-weight: 300;
        line-height: 20px; /* 125% */
      }
    }
  }

  &__tabs {
    display: flex;
    padding: 0px 40px;
    justify-content: flex-start;
    align-items: center;
    gap: 12px;
  }

  &__content {
    width: 100%;
    &-epal {
      width: 100%;
      display: grid;
      grid-template-rows: auto;
      grid-template-columns: repeat(4, 1fr);
      gap: 40px;
      padding: 24px 40px;

      @media (max-width: 1440px) {
        grid-template-columns: repeat(3, 1fr);
      }

      @media (max-width: 1024px) {
        grid-template-columns: repeat(2, 1fr);
      }

      @media (max-width: 780px) {
        grid-template-columns: repeat(1, 1fr);
      }

      .game-wrapper {
        flex-shrink: 0;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.03);
        overflow: hidden;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          object-position: center;
        }
      }
    }
  }
}
</style>
