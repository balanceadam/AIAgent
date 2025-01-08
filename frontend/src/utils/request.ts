import axios, { AxiosError, type Method } from 'axios'
import { useWalletStore } from '@/stores/wallet'

interface ApiResponseError {
  detail?: string
}

const baseURL = import.meta.env.VITE_APP_API_PREFIX

const instance = axios.create({
  baseURL,
  timeout: 5000
})

instance.interceptors.request.use(
  (config) => {
    const walletStore = useWalletStore()
    if (walletStore.accessToken) {
      config.headers.Authorization = `Token ${walletStore.accessToken}`
    }

    return config
  },
  (error) => Promise.reject(error)
)

instance.interceptors.response.use(
  (response) => {
    // TODO: 业务错误处理

    return response.data
  },
  (error: AxiosError<ApiResponseError>) => {
    // 处理401错误
    if (error.response?.status === 401) {
      window.$message?.error('登录已过期，请重新登录')
      const walletStore = useWalletStore()
      walletStore.logout()
      return Promise.reject(error)
    }

    if (error.response && error.response.data && error.response.data.detail)
      window.$message.error(error.response?.data?.detail || '请求失败')

    return Promise.reject(error)
  }
)

export const request = <T>(
  url: string,
  method: Method = 'GET',
  submitData?: object,
  headers?: object
) => {
  // 参数：地址，请求方式，提交的数据
  // 返回：promise
  return instance.request<any, T>({
    url,
    method,
    [method.toUpperCase() === 'GET' ? 'params' : 'data']: submitData,
    headers
  })
}
