import { request } from '@/utils/request'
import type {
  Account,
  Wallet,
  BasicInfo,
  AssetsChain,
  FillingService,
  Game,
  AssetsToken,
  Position,
  PositionParams,
  Results,
  TokenParams,
  Follow,
  Followed,
  Friend,
  Comment,
  AssetsTokenEdit,
  Transaction
} from '@/types'

/**
 * 获取用户信息
 * @returns
 */
export const getAccountInfo = () => request<Account>('/account/info/', 'GET')

/**
 * 更新用户信息
 * @param data
 * @returns
 */
export const updateAccount = (data: Partial<Account>) =>
  request<Account>('/account/info/', 'PUT', data, {
    'Content-Type': 'multipart/form-data'
  })

/**
 * 检查是否在白名单内
 * @returns
 */
export const fetchInWhitelist = () =>
  request<{ inWhitelist: boolean }>('/account/in_whitelist/', 'GET')

/**
 * 验证表单
 * @param data
 * @returns
 */
export const postValidateForm = (data: { name: string; epalName: string; ticker: string }) =>
  request<{ detail: string }>('/assets/tokens/validate/', 'POST', data)
/***************wallet start****************/
/**
 * 钱包登录或注册
 * @param data
 * @returns
 */
export const registerOrLoginWallet = (data: Wallet) =>
  request('/wallet/login_or_register/', 'POST', data)
/***************wallet end****************/

/***************assets start****************/
/**
 * 获取链列表
 * @returns
 */
export const getChains = () => request<AssetsChain[]>('/assets/chains/', 'GET')

/**
 * 获取补单服务列表
 * @returns
 */
export const getFillingService = () => request<FillingService[]>('/assets/filling_services/', 'GET')

/**
 * 获取游戏列表
 * @returns
 */
export const getGames = () => request<Game[]>('/assets/games/', 'GET')

/**
 * 获取我的token列表
 * @param page
 * @param size
 * @returns
 */
export const getAssetsTokens = (page: number = 1, size: number = 10) =>
  request<Results<AssetsToken>>('/assets/tokens/', 'GET', { page, size })

/**
 * 铸造token
 * @param data
 * @returns
 */
export const postAssetsToken = (data: any) =>
  request<AssetsToken>('/assets/tokens/', 'POST', data, {
    'Content-Type': 'multipart/form-data'
  })

/**
 * 编辑token
 * @param id
 * @param data
 * @returns
 */
export const editAssetsToken = (id: number, data: AssetsTokenEdit) =>
  request(`/assets/tokens/${id}/`, 'PUT', data)

/**
 * 获取单个token信息
 * @param id
 * @returns
 */
export const getAssetsTokenById = (id: number) =>
  request<AssetsToken>(`/assets/all_tokens/${id}/`, 'GET')

/**
 * 获取分钟级别数据
 * @param id
 * @returns
 */
export const getMinuteMarketDataById = (id: number) =>
  request(`/assets/minute_market_data/?id=${id}`, 'GET')

/**
 * 获取我的持仓列表
 * @returns
 */
export const getMyPositions = (page = 1, size = 20) =>
  request<Results<Position>>('/assets/positions/', 'GET', { page, size })

/**
 * 提交持仓信息
 * @param data
 * @returns
 */
export const postPosition = (data: PositionParams) => request('/assets/positions/', 'POST', data)

/**
 * 获取交易记录
 * @param id
 * @param page
 * @param size
 * @returns
 */
export const getTransactionsById = (id: number, page = 1, size = 20) =>
  request<Results<Transaction>>(`/assets/transactions/?tokenId=${id}`, 'GET', { page, size })
/***************assets end****************/

/***************generic start****************/
/**
 * 获取基础信息
 * @param type
 * @param name
 * @returns
 */
export const getBasicInfo = (type?: string, name?: string) =>
  request<BasicInfo[]>('/generic/basic_info/', 'GET', { type, name })
/***************generic end****************/

/***************social start****************/
/**
 * 获取关注/粉丝数量
 * @returns
 */
export const getFollow = (accountId: number) =>
  request<Follow>('/social/follow/', 'GET', { accountId })

/**
 * 是否关注某个用户
 * @returns
 */
export const getFollowed = (accountId: number) =>
  request<Followed>('/social/followed/', 'GET', { accountId })

/**
 *
 * @param accountId
 * @returns
 */
export const follow = (accountId: number) => request('/social/follow/', 'POST', { accountId })

/**
 *
 * @param accountId
 * @returns
 */
export const unfollow = (accountId: number) => request('/social/follow/', 'DELETE', { accountId })

/**
 * 粉丝列表
 * @returns
 */
export const getFans = (accountId: number, page: number = 1, size: number = 20) =>
  request<Results<Friend>>('/social/fans/', 'GET', { accountId, page, size })

/**
 * 关注列表
 * @returns
 */
export const getFollowings = (accountId: number, page: number = 1, size: number = 20) =>
  request<Results<Friend>>('/social/followings/', 'GET', { accountId, page, size })

/**
 * 获取评论列表
 * @param tokenId
 * @param page
 * @param size
 * @returns
 */
export const getComments = (tokenId: number, page: number = 1, size: number = 10) =>
  request<Results<Comment>>('/social/comments/', 'GET', { tokenId, page, size })

/**
 * 发布评论
 * @param data
 * @returns
 */
export const postComment = (data: any) =>
  request<{ detail: string }>('/social/comments/', 'POST', data, {
    'Content-Type': 'multipart/form-data'
  })

/**
 * 删除评论
 * @param id
 * @returns
 */
export const deleteComment = (id: number) => request('/social/comments/', 'DELETE', { id })
/***************social end****************/

/***************Epal tokens start****************/
/**
 * 获取Epal Space list
 * @param params {
 *  page?: number
    pageSize?: number
    bondingCurve?: string
    chain?: string
    ordering?: string
 * }
 * @returns
 */
export const getEpalTokens = (params: TokenParams) =>
  request<Results<AssetsToken>>('/assets/all_tokens/', 'GET', params)

/***************Epal tokens End****************/
