<script lang="ts" setup>
import { useSocialStore } from '@/stores/social'
import { useWalletStore } from '@/stores/wallet'
import type { Friend, Results } from '@/types'

interface Props {
  accountId: number,
  friendType: string,    // fans / following
  showFollow: boolean,
}
const { accountId, friendType, showFollow } = defineProps<Props>()

const socialStore = useSocialStore()
const { userInfo } = useWalletStore()
const route = useRoute();
const router = useRouter()
const count = ref(0)
const next = ref('')
const page = ref(1)
const size = ref(20)
const friendList = ref<Friend[]>([])

const emit = defineEmits<{
  (event: 'afterFollow'): void;
}>();

const getFriendList = async (init: boolean=false) => {
  if (next.value) {
    page.value += 1
  }
  if (!init && !next.value) {
    return
  }
  let res: Results<Friend>
  try {
    if (friendType === 'fans') {
      res = await socialStore.getFansList(accountId, page.value, size.value)
    } else {
      res = await socialStore.getFollowingList(accountId, page.value, size.value)
    }
    count.value = res.count
    next.value = res.next
    friendList.value = friendList.value.concat(res.results)
  } catch (error) {
    console.error(error)
  }
}

const formatNumber = (value: number) => {
  if (value < 1000) {
    return value.toString()
  }
  return (value / 1000).toLocaleString('en-US', {
    style: 'decimal',
    maximumFractionDigits: 2,
    minimumFractionDigits: 2,
  }) + 'k';
}

const handleClick = (id: number) => {
  if (route.name === 'epal-detail') {
    router.replace({ name: 'epal-detail', params: { id }}).then(() => {
      location.reload()
    })
  } else {
    router.push({ name: 'epal-detail', params: { id } })
  }
}

const follow = async (f: Friend) => {
  if (userInfo.id) {
    f.followed = true
    await socialStore.followAccount(f.account.id)
    emit('afterFollow');
  }
}

const unfollow = async (f: Friend) => {
  if (userInfo.id) {
    f.followed = false
    await socialStore.unfollowAccount(f.account.id)
    emit('afterFollow');
  }
}

onMounted(async () => {
  await getFriendList(true)
})
</script>

<template>
  <div class="friends">
    <n-infinite-scroll style="height: 240px" :distance="10" @load="getFriendList">
      <n-grid :x-gap="12" :y-gap="12" :cols="2">
        <n-grid-item
          v-for="f in friendList"
          :key="f.id"
          @click="f.hasToken && handleClick(f.tokenId)"
          :style="{cursor: f.hasToken ? 'pointer': ''}"
        >
          <n-space justify="space-between" align="center" class="item">
            <n-space justify="start" align="center" class="left-content">
              <n-avatar :src="f.account.avatar as string" class="avatar"></n-avatar>
              <div class="name">
                <div class="label">Name</div>
                <div class="content">{{ f.account.name }}</div>
              </div>
            </n-space>
            <div class="right-content" v-if="f.hasToken">
              <div class="label">Amount(Value)</div>
              <div class="content">$ {{ formatNumber(f.marketValue) }}</div>
            </div>
            <div class="follow" v-if="showFollow && userInfo.id != f.account.id && !f.followed" @click.stop="follow(f)">
              <SvgIcon name="follow"></SvgIcon>
              <span>Follow</span>
            </div>
            <div class="unfollow" v-if="showFollow && userInfo.id != f.account.id && f.followed" @click.stop="unfollow(f)">
              <SvgIcon name="unfollow"></SvgIcon>
              <span>UnFollow</span>
            </div>
          </n-space>
        </n-grid-item>
      </n-grid>
    </n-infinite-scroll>
  </div>
</template>

<style lang="scss" scoped>
.friends {
  padding: 24px 40px;

  .item {
    display: flex;
    padding: 12px 24px;
    justify-content: space-between;
    align-items: center;
    align-self: stretch;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.03);
    box-shadow: 0px 0px 19.2px 0px rgba(77, 77, 77, 0.06);

    .left-content {
      .avatar {
        width: 44px !important;
        height: 44px !important;
        border-radius: 8px;
        box-shadow: 0px 0px 4.693px 0px rgba(0, 0, 0, 0.60), 0px 0px 8.565px 0px rgba(77, 77, 77, 0.12);
        margin-right: 16px;
        margin-top: 5px;
      }
    }

    .label {
      color: rgba(255, 255, 255, 0.30);
      text-shadow: 0px 0px 36.4px #000;
      font-family: Sora;
      font-size: 12px;
      font-style: normal;
      font-weight: 400;
      line-height: 16px; /* 133.333% */
    }

    .content {
      margin-top: 12px;
      color: #FFF;
      text-shadow: 0px 0px 36.4px #000;
      font-family: Sora;
      font-size: 16px;
      font-style: normal;
      font-weight: 300;
      line-height: 20px; /* 125% */
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
}
</style>
