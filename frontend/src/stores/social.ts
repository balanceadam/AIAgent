import { defineStore } from 'pinia'
import type { Comment, CommentParams, TradeHistory } from '@/types/index'
import {
  getFollow,
  getFollowed,
  follow,
  unfollow,
  getComments,
  postComment,
  deleteComment,
  getFans,
  getFollowings
} from '@/apis'

export const useSocialStore = defineStore('social', () => {
  const comments = ref<Comment[]>([])
  const tradeHistoryList = ref<TradeHistory[]>([])

  const getFollowInfo = async (accountId: number) => {
    try {
      const results = await getFollow(accountId)

      return Promise.resolve(results)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  const getFollowedInfo = async (accountId: number) => {
    try {
      const result = await getFollowed(accountId)

      return Promise.resolve(result.followed)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  const followAccount = async (accountId: number) => {
    try {
      const result = await follow(accountId)
      return Promise.resolve(result)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  const unfollowAccount = async (accountId: number) => {
    try {
      const result = await unfollow(accountId)
      return Promise.resolve(result)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  const getFansList = async (accountId: number, page: number = 1, size: number = 20) => {
    try {
      const result = await getFans(accountId, page, size)
      return Promise.resolve(result)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  const getFollowingList = async (accountId: number, page: number = 1, size: number = 20) => {
    try {
      const result = await getFollowings(accountId, page, size)
      return Promise.resolve(result)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  /**
   * 获取指定epal token的评论列表
   * @param tokenId
   * @param page
   * @param size
   * @returns
   */
  const getCommentList = async (tokenId: number, page: number = 1, size: number = 100) => {
    try {
      const { results } = await getComments(tokenId, page, size)
      console.log(results)

      comments.value = results
      return Promise.resolve(results)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  /**
   * 发表评论
   * @param params
   * @returns
   */
  const postCommentInfo = async (params: any) => {
    try {
      const result = await postComment(params)
      return Promise.resolve(result)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  /**
   * 删除评论
   * @param id
   * @returns
   */
  const deleteCommentInfo = async (id: number) => {
    try {
      const result = await deleteComment(id)
      return Promise.resolve(result)
    } catch (error) {
      console.error(error)
      return Promise.reject(error)
    }
  }

  const getTradeHistoryList = () => {
    tradeHistoryList.value = [
      {
        id: 1,
        account: {
          id: 1,
          name: 'test1',
          username: 'test1',
          avatar: `https://picsum.photos/40/40?time=${Math.random()}`,
          bio: 'test1',
          createdAt: '2023-05-01T00:00:00.000Z',
          updatedAt: '2023-05-01T00:00:00.000Z'
        },
        transaction: '0x1234567890abcdef1',
        symbol: 'buy',
        eth: 0.0004,
        date: '2023-05-01 09:25:45',
        cics: '3.60m'
      },
      {
        id: 2,
        account: {
          id: 2,
          name: 'test2',
          username: 'test2',
          avatar: `https://picsum.photos/40/40?time=${Math.random()}`,
          bio: 'test2',
          createdAt: '2023-05-02T00:00:00.000Z',
          updatedAt: '2023-05-02T00:00:00.000Z'
        },
        transaction: '0x1234567890abcdef2',
        symbol: 'sell',
        eth: 0.0005,
        date: '2023-05-02 10:30:50',
        cics: '4.50m'
      },
      {
        id: 3,
        account: {
          id: 3,
          name: 'test3',
          username: 'test3',
          avatar: `https://picsum.photos/40/40?time=${Math.random()}`,
          bio: 'test3',
          createdAt: '2023-05-03T00:00:00.000Z',
          updatedAt: '2023-05-03T00:00:00.000Z'
        },
        transaction: '0x1234567890abcdef3',
        symbol: 'buy',
        eth: 0.0006,
        date: '2023-05-03 11:45:55',
        cics: '5.40m'
      },
      {
        id: 4,
        account: {
          id: 4,
          name: 'test4',
          username: 'test4',
          avatar: `https://picsum.photos/40/40?time=${Math.random()}`,
          bio: 'test4',
          createdAt: '2023-05-04T00:00:00.000Z',
          updatedAt: '2023-05-04T00:00:00.000Z'
        },
        transaction: '0x1234567890abcdef4',
        symbol: 'sell',
        eth: 0.0007,
        date: '2023-05-04 12:00:00',
        cics: '6.30m'
      },
      {
        id: 5,
        account: {
          id: 5,
          name: 'test5',
          username: 'test5',
          avatar: `https://picsum.photos/40/40?time=${Math.random()}`,
          bio: 'test5',
          createdAt: '2023-05-05T00:00:00.000Z',
          updatedAt: '2023-05-05T00:00:00.000Z'
        },
        transaction: '0x1234567890abcdef5',
        symbol: 'buy',
        eth: 0.0008,
        date: '2023-05-05 13:15:10',
        cics: '7.20m'
      },
      {
        id: 6,
        account: {
          id: 6,
          name: 'test6',
          username: 'test6',
          avatar: `https://picsum.photos/40/40?time=${Math.random()}`,
          bio: 'test6',
          createdAt: '2023-05-06T00:00:00.000Z',
          updatedAt: '2023-05-06T00:00:00.000Z'
        },
        transaction: '0x1234567890abcdef6',
        symbol: 'sell',
        eth: 0.0009,
        date: '2023-05-06 14:30:20',
        cics: '8.10m'
      },
      {
        id: 7,
        account: {
          id: 7,
          name: 'test7',
          username: 'test7',
          avatar: `https://picsum.photos/40/40?time=${Math.random()}`,
          bio: 'test7',
          createdAt: '2023-05-07T00:00:00.000Z',
          updatedAt: '2023-05-07T00:00:00.000Z'
        },
        transaction: '0x1234567890abcdef7',
        symbol: 'buy',
        eth: 0.001,
        date: '2023-05-07 15:45:30',
        cics: '9.00m'
      },
      {
        id: 8,
        account: {
          id: 8,
          name: 'test8',
          username: 'test8',
          avatar: `https://picsum.photos/40/40?time=${Math.random()}`,
          bio: 'test8',
          createdAt: '2023-05-08T00:00:00.000Z',
          updatedAt: '2023-05-08T00:00:00.000Z'
        },
        transaction: '0x1234567890abcdef8',
        symbol: 'sell',
        eth: 0.0011,
        date: '2023-05-08 16:00:40',
        cics: '9.90m'
      },
      {
        id: 9,
        account: {
          id: 9,
          name: 'test9',
          username: 'test9',
          avatar: `https://picsum.photos/40/40?time=${Math.random()}`,
          bio: 'test9',
          createdAt: '2023-05-09T00:00:00.000Z',
          updatedAt: '2023-05-09T00:00:00.000Z'
        },
        transaction: '0x1234567890abcdef9',
        symbol: 'buy',
        eth: 0.0012,
        date: '2023-05-09 17:15:50',
        cics: '10.80m'
      },
      {
        id: 10,
        account: {
          id: 10,
          name: 'test10',
          username: 'test10',
          avatar: `https://picsum.photos/40/40?time=${Math.random()}`,
          bio: 'test10',
          createdAt: '2023-05-10T00:00:00.000Z',
          updatedAt: '2023-05-10T00:00:00.000Z'
        },
        transaction: '0x1234567890abcdefa',
        symbol: 'sell',
        eth: 0.0013,
        date: '2023-05-10 18:30:00',
        cics: '11.70m'
      }
    ]
    return Promise.resolve(tradeHistoryList.value)
  }

  return {
    comments,
    tradeHistoryList,
    getFollowInfo,
    getFollowedInfo,
    followAccount,
    unfollowAccount,
    getFansList,
    getFollowingList,
    getCommentList,
    postCommentInfo,
    deleteCommentInfo,
    getTradeHistoryList
  }
})
