import { defineStore } from 'pinia'
import { useWalletStore } from '@/stores/wallet'

import type {
  AssetsChain,
  FillingService,
  AssetsToken,
  Game,
  AssetsTokenCreate,
  AssetsTokenEdit
} from '@/types/index'
import {
  getChains,
  getFillingService,
  getAssetsTokens,
  getGames,
  postAssetsToken,
  fetchInWhitelist,
  postValidateForm,
  editAssetsToken
} from '@/apis/index'

export const useLaunchStore = defineStore(
  'launch',
  () => {
    const walletStore = useWalletStore()

    const chainList = ref<AssetsChain[]>([])
    const fillingServiceList = ref<FillingService[]>([])
    const AssetsTokenList = ref<AssetsToken[]>([])
    const gameList = ref<Game[]>([])
    const launchForm = ref<AssetsTokenCreate>({
      chain: null,
      description: '',
      logo: '',
      epal: '',
      name: '',
      telegram: '',
      ticker: '',
      twitter: '',
      website: '',
      fillingServices: [],
      account: walletStore.userInfo.id,
      games: [],
      initialBuyNumber: null,
      initialBuyType: 1,
      labels: '',
      epalName: '',
      protocol: {
        protocolId: 1,
        address: '',
        symbol: '',
        price: 0,
        bondingCurve: 0,
        marketValue: 0,
        dayIncrease: 0,
        dayTradingVolume: 0
      }
    })
    const editForm = ref<AssetsTokenEdit>({
      telegram: '',
      twitter: '',
      website: '',
      games: [],
      labels: ''
    })

    const isInWhitelist = ref<boolean>(false)

    const getChainList = async () => {
      try {
        const res = await getChains()
        chainList.value = res
        console.log(res)
        return Promise.resolve(res)
      } catch (error) {
        console.error(error)
      }
    }

    const getFillingServiceList = async () => {
      try {
        const res = await getFillingService()
        fillingServiceList.value = res
        console.log(res)
      } catch (error) {
        console.error(error)
      }
    }

    const getAssetsTokenList = async () => {
      try {
        const res = await getAssetsTokens(1, 10)
        AssetsTokenList.value = res.results
        console.log(res)
      } catch (error) {
        console.error(error)
      }
    }

    const getGamesList = async () => {
      try {
        const res = await getGames()
        gameList.value = res
        console.log(res)
      } catch (error) {
        console.error(error)
      }
    }

    const getInWhitelist = async () => {
      try {
        const { inWhitelist } = await fetchInWhitelist()
        isInWhitelist.value = inWhitelist
        return Promise.resolve(inWhitelist)
      } catch (error) {
        console.error(error)
        return Promise.reject(false)
      }
    }

    const validateForm = async () => {
      try {
        const params = {
          name: launchForm.value.name,
          ticker: launchForm.value.ticker,
          epalName: launchForm.value.epalName
        }
        const res = await postValidateForm(params)
        console.log(res)

        return Promise.resolve(true)
      } catch (error) {
        console.error(error)
        return Promise.reject(false)
      }
    }

    const sumbitAssetsToken = async () => {
      try {
        const formData = new FormData()

        Object.keys(launchForm.value).forEach((key) => {
          if (key === 'fillingServices' || key === 'games') {
            launchForm.value[key].forEach((item) => {
              if (key === 'games') {
                formData.append('games', item.toString())
              } else {
                formData.append('filling_services', item.toString())
              }
            })
          } else if (key === 'logo' || key === 'epal') {
            formData.append(key, launchForm.value[key] as File)
          } else if (key === 'protocol') {
            formData.append('protocol.protocol_id', launchForm.value.protocol.protocolId.toString())
            formData.append('protocol.address', launchForm.value.protocol.address.toString())
            formData.append('protocol.symbol', launchForm.value.protocol.symbol.toString())
            formData.append('protocol.price', launchForm.value.protocol.price.toString())
            // formData.append('protocol.id', launchForm.value.protocol.id.toString())
            formData.append(
              'protocol.bonding_curve',
              launchForm.value.protocol.bondingCurve.toString()
            )
            formData.append(
              'protocol.market_value',
              launchForm.value.protocol.marketValue.toString()
            )
            formData.append(
              'protocol.day_increase',
              launchForm.value.protocol.dayIncrease.toString()
            )
            formData.append(
              'protocol.day_trading_volume',
              launchForm.value.protocol.dayTradingVolume.toString()
            )
          } else if (key === 'epalName') {
            formData.append('epal_name', launchForm.value[key] as string)
          } else {
            formData.append(
              key,
              (launchForm.value[key as keyof AssetsTokenCreate] ?? '').toString()
            )
          }
        })

        const res = await postAssetsToken(formData)
        return Promise.resolve(res)
      } catch (error) {
        console.error(error)
        return Promise.reject(false)
      }
    }

    const submitEdit = async (id: number) => {
      try {
        const res = await editAssetsToken(id, editForm.value)
        return Promise.resolve(res)
      } catch (error) {
        console.error(error)
        return Promise.reject(false)
      }
    }

    const resetLaunchForm = () => {
      launchForm.value = {
        account: walletStore.userInfo.id,
        chain: chainList.value[0].id,
        fillingServices: [],
        games: [],
        name: '',
        ticker: '',
        telegram: '',
        twitter: '',
        website: '',
        initialBuyNumber: null,
        initialBuyType: 1,
        description: '',
        labels: '',
        logo: '',
        epal: '',
        epalName: '',
        protocol: {
          protocolId: 1,
          address: '',
          symbol: '',
          price: 0,
          bondingCurve: 0,
          marketValue: 0,
          dayIncrease: 0,
          dayTradingVolume: 0
        }
      }
    }

    return {
      chainList,
      fillingServiceList,
      AssetsTokenList,
      gameList,
      launchForm,
      editForm,
      isInWhitelist,
      getChainList,
      getFillingServiceList,
      getAssetsTokenList,
      getGamesList,
      getInWhitelist,
      validateForm,
      sumbitAssetsToken,
      submitEdit,
      resetLaunchForm
    }
  },
  {
    persist: true
  }
)
