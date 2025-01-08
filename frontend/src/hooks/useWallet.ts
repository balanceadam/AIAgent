import { Web3 } from 'web3'
import { useWalletStore } from '@/stores/wallet'
import type {
  EIP6963ProviderDetail,
  EIP6963AnnounceProviderEvent,
  ProtocolParams
} from '@/types/index'
import { EIP6963RequestProviderEvent } from '@/types/index'
import FansProtocolABI from '@/abis/FansProtocolABI.json'
import IERC20ABI from '@/abis/IERC20ABI.json'

declare global {
  interface Window {
    ethereum?: any
    okxwallet?: any
    web3: any
  }
}
const EPT_TOKEN_ADDRESS = '0x780f73aF0349b12735bB67Aa91ed660e06D38623'

export const useWallet = () => {
  const FANS_PROTOCOL_ADDRESS = '0xA74E5f34FF6448969858aB4Df575a7D3D0F9F87E'
  const providerDetails = ref<EIP6963ProviderDetail[]>([])
  const currentProvider = ref<EIP6963ProviderDetail | null | undefined>(null)
  const walletStore = useWalletStore()
  let web3: any

  const findProvider = async (providerName: string) => {
    const providerDetail = providerDetails.value.find((item) => item.info.name === providerName)
    currentProvider.value = providerDetail as EIP6963ProviderDetail
    return providerDetail?.provider
  }
  // 获取所有可用的wallet providers
  const requestProviders = () => {
    return new Promise<EIP6963ProviderDetail[]>((resolve) => {
      // ...
      window.addEventListener('eip6963:announceProvider', (event: EIP6963AnnounceProviderEvent) => {
        providerDetails.value.push(event.detail)
        return resolve(providerDetails.value)
      })
      window.dispatchEvent(new EIP6963RequestProviderEvent())
    })
  }

  // 连接wallet
  const connectWallet = async (walletName: string) => {
    if (walletName === 'MetaMask') {
      if (window.ethereum && window.ethereum.isMetaMask) {
        const provider = await findProvider('MetaMask')
        const web3 = new Web3(provider)
        web3.setProvider(provider)
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' })
        const defaultAccount = accounts[0]
        // // Getting the chain ID
        const chainId = await window.ethereum.request({ method: 'eth_chainId' })
        const wallet = walletStore.wallet
        // Fetch EPT Balance
        let eptBalance = '0'
        try {
          const eptContract = new web3.eth.Contract(IERC20ABI, EPT_TOKEN_ADDRESS)
          // Fetch balance
          const rawBalance: string = await eptContract.methods.balanceOf(defaultAccount).call()

          // Convert balance based on decimals
          eptBalance = Web3.utils.fromWei(rawBalance, 'ether') // Adjust if decimals !== 18
          // If decimals are not 18, use:
          // eptBalance = Web3.utils.toBN(rawBalance).div(Web3.utils.toBN(10).pow(Web3.utils.toBN(decimals))).toString();
        } catch (error) {
          console.error('Error fetching EPT balance:', error)
        }

        // 判断是否需要更新
        if (
          wallet.address === defaultAccount &&
          wallet.chainId === chainId &&
          wallet.balance === eptBalance
        ) {
          console.log('Wallet address is the same. No need to update.')
          return
        }
        // 更新本地数据
        walletStore.setWallet({
          providerName: walletName,
          address: defaultAccount,
          chainId: chainId,
          balance: eptBalance
        })
      } else {
        window.open('https://metamask.io/download/') // 打开Metamask 安装页面
      }
    }

    return Promise.resolve(true)
  }

  const disconnectWallet = async () => {
    window.removeEventListener(
      'eip6963:announceProvider',
      (event: EIP6963AnnounceProviderEvent) => {
        providerDetails.value.push(event.detail)
      }
    )
    if (web3) {
      web3?.setProvider(null)
      web3.defaultAccount = null
      web3.defaultChain = null
      web3 = null
    }
    if (window.ethereum._handleDisconnect) {
      await window.ethereum._handleDisconnect()
    } else if (window.ethereum.disconnect) {
      await window.ethereum?.disconnect()
    }

    walletStore.logout()
  }

  const checkEPTBalance = async (account: string): Promise<number> => {
    const currencyTokenContract = new web3.eth.Contract(
      IERC20ABI as any,
      EPT_TOKEN_ADDRESS // 替换为 EPT 代币的合约地址
    )

    const balance = await currencyTokenContract.methods.balanceOf(account).call()
    const balanceInEpt = parseFloat(web3.utils.fromWei(balance, 'ether'))
    return balanceInEpt
  }

  const approveCurrencyToken = async (account: string, amount: string = '50'): Promise<boolean> => {
    if (!web3) {
      await initWallet()
    }

    const currencyTokenContract = new web3.eth.Contract(
      IERC20ABI as any,
      EPT_TOKEN_ADDRESS // 替换为 EPT 代币的合约地址
    )

    const amountInWei = web3.utils.toWei(amount, 'ether') // 假设 EPT 有 18 位小数

    try {
      const tx = currencyTokenContract.methods.approve(FANS_PROTOCOL_ADDRESS, amountInWei)
      const gas = await tx.estimateGas({ from: account })
      const gasPrice = await web3.eth.getGasPrice()

      await tx.send({
        from: account,
        gas: gas.toString(),
        gasPrice: gasPrice.toString()
      })

      console.log('授权成功。')
      return true
    } catch (error) {
      console.error('授权失败：', error)
      return false
    }
  }

  const checkAllowance = async (
    account: string,
    requiredAmount: string = '50'
  ): Promise<boolean> => {
    if (!web3) {
      await initWallet()
    }

    const currencyTokenContract = new web3.eth.Contract(
      IERC20ABI as any,
      EPT_TOKEN_ADDRESS // 替换为 EPT 代币的合约地址
    )

    const allowanceStr: string = await currencyTokenContract.methods
      .allowance(account, FANS_PROTOCOL_ADDRESS)
      .call()

    const allowance = BigInt(allowanceStr)
    const requiredAmountWei = BigInt(web3.utils.toWei(requiredAmount, 'ether'))

    if (allowance < requiredAmountWei) {
      console.log(
        `当前授权额度为 ${allowanceStr} wei，不足以创建代币。需要授权 ${requiredAmountWei} wei。`
      )
      return false
    }

    console.log(`授权额度足够：${allowanceStr} wei。`)
    return true
  }

  const createToken = async (name: string, symbol: string): Promise<ProtocolParams | null> => {
    try {
      if (!web3) {
        await initWallet()
      }
      const contract = new web3.eth.Contract(FansProtocolABI.abi as any, FANS_PROTOCOL_ADDRESS)
      let accounts = await web3.eth.getAccounts()
      if (accounts.length === 0) {
        console.error('No accounts found. Attempting to reconnect wallet...')

        // Try reconnecting wallet if no accounts are found
        const walletConnected = await connectWallet('MetaMask') // You can pass other wallet names if needed
        if (!walletConnected) {
          console.error('Failed to reconnect wallet.')
          return null
        }

        // Re-fetch accounts after reconnecting
        accounts = await web3.eth.getAccounts()
        if (accounts.length === 0) {
          console.error('No accounts found after reconnecting. Make sure your wallet is connected.')
          return null
        }
      }
      const account = accounts[0]
      // 检查 EPT 余额
      // const hasEnoughBalance = await checkEPTBalance(account);
      // if (!hasEnoughBalance) {
      //   return null;
      // }

      // 授权智能合约转账 EPT
      // 检查授权额度
      const isAllowanceSufficient = await checkAllowance(account, '50')
      if (!isAllowanceSufficient) {
        // 授权智能合约转账 EPT
        const isApproved = await approveCurrencyToken(account)
        if (!isApproved) {
          console.error('Approve failed.')
          return null
        }
      } else {
        console.log('无需再次授权。')
      }

      // 生成一个随机的salt
      const salt = web3.utils.randomHex(32)

      // 调用createToken函数
      const tx = contract.methods.createToken(name, symbol, salt)

      // 估算Gas
      const gas = await tx.estimateGas({ from: account })
      const gasPrice = await web3.eth.getGasPrice()

      // 发送交易
      const receipt = await tx.send({
        from: account,
        gas: gas.toString(),
        gasPrice: gasPrice.toString()
      })

      console.log('Transaction successful:', receipt)

      // 解析交易收据中的 TokenCreation 事件
      const events = receipt.events?.TokenCreation
      if (!events) {
        console.error('TokenCreation event not found in receipt.')
        return null
      }

      // 如果有多个 TokenCreation 事件，您可能需要处理所有事件或选择特定的事件
      const tokenCreationEvent = Array.isArray(events) ? events[0] : events

      const returnValue = tokenCreationEvent.returnValues
      const {
        tokenId,
        tokenAddress,
        tokenName,
        symbol: tokenSymbol,
        timestamp,
        creator
      } = returnValue

      console.log(returnValue, 'returnValue')

      // 设置wallet balance
      walletStore.wallet.balance = await checkEPTBalance(account)

      return {
        protocolId: Number(tokenId),
        symbol: tokenSymbol,
        address: tokenAddress,
        price: 0,
        bondingCurve: 0,
        marketValue: 0,
        dayIncrease: 0,
        dayTradingVolume: 0
      }
    } catch (error) {
      console.error('Error creating token:', error)
      return null
    }
  }

  /**
   * 调用 FansProtocol 合约的 purchaseTokenWithCurrency 方法
   * @param tokenId 要购买的代币ID
   * @param currencyAmount 购买的 epl 代币数量（假设已是最小单位）
   */
  const purchaseTokenWithCurrency = async (tokenId: number, currencyAmount: string | number) => {
    if (!web3) {
      await initWallet()
    }
    const currencyAmountWei = web3.utils.toWei(currencyAmount.toString(), 'ether')

    // const tokenReceive = await estimateTokenPurchase(tokenId, Number(currencyAmount))
    // console.log("estimate, ", tokenReceive)

    const accounts = await web3.eth.getAccounts()
    if (accounts.length === 0) {
      throw new Error('No accounts found. Please connect your wallet.')
    }
    const userAddress = accounts[0]

    const fansProtocolContract = new web3.eth.Contract(
      FansProtocolABI.abi as any,
      FANS_PROTOCOL_ADDRESS
    )

    // 不需要转换，直接使用 currencyAmount
    const currencyAmountRaw =
      typeof currencyAmount === 'string' ? currencyAmount : currencyAmount.toString()

    try {
      // 检查用户是否已批准足够的 currencyToken 给 FansProtocol 合约
      const currencyTokenContract = new web3.eth.Contract(IERC20ABI as any, EPT_TOKEN_ADDRESS)
      const allowanceStr = await currencyTokenContract.methods
        .allowance(userAddress, FANS_PROTOCOL_ADDRESS)
        .call()

      // const requiredAmountBN = web3.utils.toWei(currencyAmountRaw, 'ether')
      const allowanceBN = BigInt(allowanceStr)
      const currencyAmountBN = BigInt(currencyAmountWei)

      if (allowanceBN < currencyAmountBN) {
        // 需要批准
        console.log('Insufficient allowance. Approving now...')
        // 调用 approveCurrencyToken
        const approveAmount = currencyAmountRaw.toString()
        const approveReceipt = await approveCurrencyToken(userAddress, currencyAmountRaw)
        console.log('Approval successful:', approveReceipt)

        // 再次检查 allowance
        const newAllowance = await currencyTokenContract.methods
          .allowance(userAddress, FANS_PROTOCOL_ADDRESS)
          .call()
        const newAllowanceBN = BigInt(newAllowance)
        if (newAllowanceBN < BigInt(currencyAmountRaw)) {
          throw new Error('Approval failed. Insufficient allowance after approval.')
        }
      }

      // 调用 purchaseTokenWithCurrency 方法
      const receipt = await fansProtocolContract.methods
        .purchaseTokenWithCurrency(tokenId, currencyAmountWei)
        .send({ from: userAddress })

      console.log('Transaction successful:', receipt)

      // 设置wallet balance
      walletStore.wallet.balance = await checkEPTBalance(userAddress)

      return receipt
    } catch (error: any) {
      console.error('Transaction failed:', error)
      throw new Error(error.message || 'Transaction failed')
    }
  }

  const estimateTokenPurchase = async (tokenId: number, currencyAmount: number) => {
    try {
      const fansProtocol = new web3.eth.Contract(FansProtocolABI.abi as any, FANS_PROTOCOL_ADDRESS)
      // 获取 Bonding Curve 参数和平台费用
      const A = Number(await fansProtocol.methods.A().call())
      const B = Number(await fansProtocol.methods.B().call())
      const PLATFORM_FEE_BP = Number(await fansProtocol.methods.PLATFORM_FEE_BP().call())

      // 获取 Token 信息
      const tokenInfo = await fansProtocol.methods.tokens(tokenId).call()
      const currencyCollected = Number(tokenInfo.currencyCollected)
      const tokenSold = Number(tokenInfo.tokenSold)

      // 计算平台费用
      const fee = (currencyAmount * PLATFORM_FEE_BP) / 10000
      const netFunds = currencyAmount - fee

      // 计算分母
      const denominator = 30 * 1e18 + (currencyCollected + netFunds) / 3000

      // 计算 y2
      const y2 = A * 1e18 - (B * 1e36) / denominator

      // 计算可购买的 Token 数量
      const estimatedTokenAmount = Math.abs(y2 - tokenSold)

      return estimatedTokenAmount
    } catch (error) {
      console.error('计算估算 Token 购买数量时出错:', error)
      return null
    }
  }

  /**
   * 调用 FansProtocol 合约的 sellToken 方法
   * @param tokenId 要出售的代币ID
   * @param tokenAmount 出售的 Fan 代币数量（假设已是最小单位）
   */
  const sellTokenWithFanToken = async (tokenId: number, tokenAmount: string | number) => {
    try {
      // 初始化钱包和 Web3 实例
      if (!web3) {
        await initWallet()
      }

      // 将 tokenAmount 转换为字符串形式
      const tokenAmountRaw = typeof tokenAmount === 'string' ? tokenAmount : tokenAmount.toString()

      // 获取用户账户
      const accounts = await web3.eth.getAccounts()
      if (accounts.length === 0) {
        throw new Error('未找到任何账户。请连接您的钱包。')
      }
      const userAddress = accounts[0]

      // 实例化 FansProtocol 合约
      const fansProtocolContract = new web3.eth.Contract(
        FansProtocolABI.abi as any,
        FANS_PROTOCOL_ADDRESS
      )

      // 获取指定 tokenId 的代币地址
      const tokenInfo = await fansProtocolContract.methods.tokens(tokenId).call()
      const fanTokenAddress = tokenInfo.tokenAddress

      // 实例化 Fan 代币合约
      const fanTokenContract = new web3.eth.Contract(IERC20ABI as any, fanTokenAddress)

      // 检查用户是否已批准足够的 Fan 代币给 FansProtocol 合约
      const allowance = await fanTokenContract.methods
        .allowance(userAddress, FANS_PROTOCOL_ADDRESS)
        .call()

      const allowanceBN = BigInt(allowance)
      const tokenAmountBN = BigInt(web3.utils.toWei(tokenAmountRaw, 'ether'))

      if (allowanceBN < tokenAmountBN) {
        // 需要批准
        console.log('代币批准不足。正在进行批准...')

        // 调用 approve 方法
        const approveReceipt = await fanTokenContract.methods
          .approve(FANS_PROTOCOL_ADDRESS, tokenAmountBN)
          .send({ from: userAddress })

        console.log('批准成功:', approveReceipt)

        // 再次检查批准额度
        const newAllowance = await fanTokenContract.methods
          .allowance(userAddress, FANS_PROTOCOL_ADDRESS)
          .call()
        const newAllowanceBN = BigInt(newAllowance)
        if (newAllowanceBN < tokenAmountBN) {
          throw new Error('批准失败。批准额度不足。')
        }
      }

      const userBalance = await fanTokenContract.methods.balanceOf(userAddress).call()
      console.log(
        `用户实际持有的 Fan 代币余额: ${web3.utils.fromWei(userBalance, 'ether')} Fan Token`
      )

      // 准备调用 sellToken 方法的交易对象
      const tx = fansProtocolContract.methods.sellToken(tokenId, tokenAmountBN)

      // 预估 Gas 并添加缓冲（例如 20%）
      const gasEstimate = await tx.estimateGas({ from: userAddress })
      const gas = Math.floor(Number(gasEstimate) * 1.2) // 增加 20% 的缓冲
      const gasPrice = await web3.eth.getGasPrice()

      // 发送交易，并包含预估的 Gas 和 Gas 价格
      const sellReceipt = await tx.send({
        from: userAddress,
        gas: gas.toString(),
        gasPrice: gasPrice.toString()
      })

      // 设置wallet balance
      walletStore.wallet.balance = await checkEPTBalance(userAddress)

      console.log('交易成功:', sellReceipt)
      return sellReceipt
    } catch (error: any) {
      console.error('交易失败:', error)
      throw new Error(error.message || '交易失败')
    }
  }

  /**
   * 获取 Bonding Curve 信息
   * @param tokenId 要查询的代币ID
   * @returns 包含 price、bondingCurveProgress 和 marketValue 的对象
   */
  const getBondingCurveInfo = async (
    tokenId: number
  ): Promise<{
    price: number
    bondingCurveProgress: number
    marketValue: string
  }> => {
    try {
      if (!web3) {
        await initWallet()
      }

      const fansProtocolContract = new web3.eth.Contract(
        FansProtocolABI.abi as any,
        FANS_PROTOCOL_ADDRESS
      )

      const result = await fansProtocolContract.methods.getBondingCurveInfo(tokenId).call()

      const price = Number(result.price)
      const bondingCurveProgress = Number(result.bondingCurveProgress)
      const marketValue = web3.utils.fromWei(result.marketValue, 'ether')

      return {
        price,
        bondingCurveProgress,
        marketValue
      }
    } catch (error) {
      console.error('Error fetching Bonding Curve Info:', error)
      throw new Error('Failed to fetch Bonding Curve Info')
    }
  }

  const initWallet = async () => {
    // 请求providers
    if (!providerDetails.value.length) {
      await requestProviders()
    }

    // 如果钱包处于登录状态，web3对象不存在，初始化web3
    if (!web3 && walletStore.wallet.address) {
      const provider = await findProvider(walletStore.wallet.providerName)
      web3 = new Web3(provider)
    }

    // const contract = new web3.eth.Contract(
    //   IERC20ABI as any,
    //   EPT_TOKEN_ADDRESS // 替换为 EPT 代币的合约地址
    // )

    // // 监听事件
    // contract.on('Transfer', async (from: string, to: string, value: string, event: any) => {
    //   console.log('Transfer event detected!')
    //   console.log('From:', from)
    //   console.log('To:', to)
    //   console.log('Value:', value)
    //   console.log('Hash:', event.log.transactionHash)
    //   console.log('\n')

    //   // 进一步处理
    //   walletStore.wallet.balance = await checkEPTBalance(walletStore.wallet.address)
    //   console.log(`Balance in EPT: ${walletStore.wallet.balance}`)
    // })
  }

  /**
   * 获取特定代币的余额
   * @param tokenAddress ERC20 代币合约地址
   * @returns 余额字符串（单位：代币的最小单位）
   */
  const getTokenBalance = async (tokenAddress: string): Promise<string> => {
    if (!walletStore.wallet.address) {
      throw new Error('Wallet not connected')
    }

    try {
      // 使用现有的 web3 实例或创建一个新的
      if (!web3) {
        if (currentProvider.value) {
          web3 = new Web3(currentProvider.value.provider)
        } else if (window.ethereum) {
          web3 = new Web3(window.ethereum)
        } else {
          throw new Error('No web3 provider found')
        }
      }

      // 创建 ERC20 合约实例
      const tokenContract = new web3.eth.Contract(IERC20ABI, tokenAddress)

      // 获取余额
      const balance: string = await tokenContract.methods
        .balanceOf(walletStore.wallet.address)
        .call()

      // 转换为人类可读的格式（假设代币有 18 个小数位）
      const decimals = 18 // 如果代币有不同的小数位，请调整或动态获取
      const formattedBalance = Web3.utils.fromWei(balance, 'ether')

      return formattedBalance
    } catch (error) {
      console.error('Error fetching token balance:', error)
      throw error
    }
  }

  initWallet()

  return {
    connectWallet,
    disconnectWallet,
    createToken,
    purchaseTokenWithCurrency,
    sellTokenWithFanToken,
    getBondingCurveInfo,
    getTokenBalance,
    estimateTokenPurchase
  }
}
