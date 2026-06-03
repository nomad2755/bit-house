import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// 不需要自动刷新 token 的 URL
const AUTH_URLS = ['/auth/login/', '/auth/register/', '/auth/refresh/']

// 请求拦截器：自动添加 JWT token（跳过登录/注册/刷新接口，避免失效token干扰认证）
api.interceptors.request.use((config) => {
  const url = config.url || ''
  const isAuthRequest = ['/auth/login/', '/auth/register/', '/auth/refresh/'].some(u => url.includes(u))
  const token = localStorage.getItem('access_token')
  if (token && !isAuthRequest) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：统一错误处理
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      const url = error.config?.url || ''

      if (status === 401) {
        // 登录/注册/刷新接口的 401 直接抛出，不做 token 刷新
        if (AUTH_URLS.some(u => url.includes(u))) {
          ElMessage.error('用户名或密码错误')
          return Promise.reject(error)
        }

        // 其他接口的 401 尝试刷新 token
        const refresh = localStorage.getItem('refresh_token')
        if (refresh && !error.config._retry) {
          error.config._retry = true
          return axios.post('/api/auth/refresh/', { refresh })
            .then((res) => {
              localStorage.setItem('access_token', res.data.access)
              error.config.headers.Authorization = `Bearer ${res.data.access}`
              return api(error.config)
            })
            .catch(() => {
              localStorage.clear()
              router.push('/login')
              ElMessage.error('登录已过期，请重新登录')
            })
        }
        localStorage.clear()
        router.push('/login')
        ElMessage.error('请先登录')
      } else if (status === 403) {
        ElMessage.error('没有权限执行此操作')
      } else if (status === 400) {
        // 提取错误信息
        let msg = ''
        if (typeof data === 'object' && data !== null) {
          const firstKey = Object.keys(data)[0]
          const val = data[firstKey]
          msg = Array.isArray(val) ? val[0] : (data.detail || data.error || String(val))
        } else {
          msg = String(data)
        }
        ElMessage.error(msg || '请求参数错误')
      } else {
        ElMessage.error(data?.detail || data?.error || '请求失败')
      }
    } else {
      ElMessage.error('网络错误，请检查后端服务是否启动')
    }
    return Promise.reject(error)
  }
)

export default api
