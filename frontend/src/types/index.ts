import type { UserInfo } from 'node:os'

export interface Account {
  id: number
  username: string
  name: string
  avatar?: File | null | undefined | string
  inviteCode?: string
  createdAt?: string
  updatedAt?: string
  bio?: string
}

export interface AssetsChain {
  id: number
  name: string
  logo?: string
  fee: number
  symbol: string
}

export interface FillingService {
  id: number
  name: string
  logo?: string
  description: string
}

export interface Game {
  id: number
  name: string
  img?: string
}

export interface ProtocolParams {
  protocolId: number
  address: string
  symbol: string
  price: number
  bondingCurve: number
  marketValue: number
  dayIncrease: number
  dayTradingVolume: number
}

export interface Protocol {
  id: number
  protocolId: number
  address: string
  symbol: string
  price: number
  bondingCurve: number
  marketValue: number
  dayIncrease: number
  dayTradingVolume: number
  createdAt: string
  updatedAt: string
}

export interface AssetsToken {
  id: number
  account: number
  chain: AssetsChain
  fillingServices: FillingService[]
  games: Game[]
  protocol: Protocol
  isEnabled?: boolean
  createdAt?: string
  updatedAt?: string
  name: string
  epalName?: string
  ticker: string
  telegram?: string
  website?: string
  twitter?: string
  description?: string
  logo?: string
  epal?: string
  initialBuyType?: number | null | undefined
  initialBuyNumber?: number | null | undefined
  labels?: string
  sort?: number
}

export interface AssetsTokenCreate {
  chain: number | null | undefined
  fillingServices: number[]
  games: number[]
  name: string
  epalName: string
  protocol: ProtocolParams
  ticker: string
  telegram?: string
  website?: string
  twitter?: string
  description?: string
  initialBuyType?: number | null | undefined
  initialBuyNumber?: number | null | undefined
  labels?: string
  logo?: string | File | null | undefined
  epal?: string | File | null | undefined
  account: number
}

export interface AssetsTokenEdit {
  games: number[]
  telegram?: string
  website?: string
  twitter?: string
  labels?: string
}

export interface PositionParams {
  account: number
  token: number
  position: number
}

export interface Position {
  id: number
  account: number
  token: AssetsToken
  createdAt: string
  updatedAt: string
  position: number
}

export interface Transaction {
  id: number
  account: Account
  token: AssetsToken
  type: string
  quantity: number
  amount: number
  time: string
  hash: string
}

export interface BasicInfo {
  id: number
  type: number
  name: string
  value?: string
  createdAt?: string
  updatedAt?: string
}

export interface Wallet {
  address: string
  chainId: string | number | bigint
  balance?: number | string
  [key: string]: any
}

export interface Results<T> {
  count: number
  next: string
  previous: string
  results: T[]
}

export interface TokenParams {
  page?: number
  size?: number
  bondingCurve?: number | null | undefined
  chain: number | null | undefined
  ordering?: string | null | undefined
}

declare global {
  interface WindowEventMap {
    'eip6963:announceProvider': EIP6963AnnounceProviderEvent
  }
}

// Define a class for the "eip6963:requestProvider" event
export class EIP6963RequestProviderEvent extends Event {
  constructor() {
    super('eip6963:requestProvider')
  }
}

// Define an interface for the "eip6963:announceProvider" event
export interface EIP6963AnnounceProviderEvent extends Event {
  type: 'eip6963:announceProvider'
  detail: EIP6963ProviderDetail
}

// Define an interface for the provider details
export interface EIP6963ProviderDetail {
  info: EIP6963ProviderInfo
  provider: EIP1193Provider
}

// Define an interface for the provider information
export interface EIP6963ProviderInfo {
  uuid: string // Unique identifier of the wallet extension announcement, keep in mind it changes on every request-announcement cycle
  name: string // Name of the wallet extension
  icon: string // Icon for the wallet extension
  rdns: string // Reverse DNS name of the wallet extension
}

// Define an interface for the EIP1193 provider.
// It's the same interface we are used to access with 'window.ethereum'
export interface EIP1193Provider {
  request(request: { method: string; params?: Array<any> | Record<string, any> }): Promise<any>
}

export interface Follow {
  fansCount: number
  followingCount: number
}

export interface Followed {
  followed: boolean
}

export interface Friend {
  id: number
  account: Account
  marketValue: number
  hasToken: boolean
  followed: boolean
  tokenId: number
}

export interface Comment {
  id: number
  account: Account
  content: string
  imgs: string[]
  createdAt?: string
}

export interface CommentParams {
  tokenId: number
  content: string
  imgs: File[]
}

export interface TradeHistory {
  id: number
  account: Account
  symbol: string
  eth: number
  cics: string
  date: string
  transaction: string
}
