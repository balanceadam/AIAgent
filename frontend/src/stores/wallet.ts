import { defineStore } from 'pinia'
import type { Wallet, Account } from '@/types/index'
import { registerOrLoginWallet, getAccountInfo } from '@/apis'

export const useWalletStore = defineStore(
  'wallet',
  () => {
    const wallet = ref<Wallet>({
      providerName: null,
      address: '',
      chainId: '',
      balance: 0
    })
    const accessToken = ref<string>('')
    const userInfo = ref<Account>({
      id: 0,
      name: '',
      username: '',
      avatar: '',
      updatedAt: '',
      createdAt: '',
      inviteCode: ''
    })

    const setWallet = async (data: Wallet) => {
      try {
        const { address, chainId } = data
        // 登录
        if (!accessToken.value) {
          const { token }: any = await registerOrLoginWallet({ address, chainId })
          accessToken.value = token

          // 更新用户信息
          getUserInfo()
        }
        wallet.value = data
        window.$message?.success('Connected successfully')
      } catch (error) {
        console.error('Failed to connect wallet:', error)
      }
    }

    const emptyWallet = () => {
      wallet.value = { address: '', chainId: '', balance: 0 }
    }

    const getUserInfo = async () => {
      try {
        const res: Account = await getAccountInfo()
        userInfo.value = res
      } catch (error) {
        console.error(error)
      }
    }

    const logout = () => {
      emptyWallet()
      accessToken.value = ''
      userInfo.value = {
        id: 0,
        name: '',
        username: '',
        avatar: '',
        updatedAt: '',
        createdAt: '',
        inviteCode: ''
      }
    }

    return {
      wallet,
      setWallet,
      emptyWallet,
      accessToken,
      userInfo,
      logout
    }
  },
  {
    persist: true
    // persist: {
    //   storage: localStorage,
    //   debug: true
    // }
  }
)
