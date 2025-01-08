import { defineStore } from 'pinia'
import type { TokenParams, AssetsToken, Position, PositionParams } from '@/types'
import {
  getAssetsTokens,
  getEpalTokens,
  getAssetsTokenById,
  getMinuteMarketDataById,
  getMyPositions,
  postPosition,
  getTransactionsById
} from '@/apis'

export const useAssetsStore = defineStore('assets', () => {
  const myPositions = ref<Position[]>([])
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
  // 获取我的token列表
  const getMineTokens = async () => {
    try {
      const { results } = await getAssetsTokens()

      return Promise.resolve(results)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  // 获取所有epal token列表
  const getEpalTokenList = async (params: TokenParams) => {
    try {
      const { results } = await getEpalTokens(params)
      return Promise.resolve(results)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  // 根据epal id获取单个token
  const getEpalToken = async (id: number) => {
    try {
      token.value = await getAssetsTokenById(id)
      return Promise.resolve(token.value)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  const getMinuteMarketData = async (id: number) => {
    try {
      const data = await getMinuteMarketDataById(id)
      return Promise.resolve(data)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  // 获取我的持仓列表
  const getMyPosition = async () => {
    try {
      const { results } = await getMyPositions()
      myPositions.value = results
      return Promise.resolve(myPositions.value)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  // 提交持仓信息
  const postMyPosition = async (data: PositionParams) => {
    try {
      await postPosition(data)
      return Promise.resolve(true)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  const getTransactions = async (id: number, page = 1, size = 20) => {
    try {
      const data = await getTransactionsById(id, page, size)
      return Promise.resolve(data)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  return {
    token,
    myPositions,
    getMineTokens,
    getEpalTokenList,
    getEpalToken,
    getMinuteMarketData,
    getMyPosition,
    postMyPosition,
    getTransactions
  }
})
