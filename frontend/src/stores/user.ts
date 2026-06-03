import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')
  const userInfo = ref<any>(null)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => localStorage.getItem('role') === 'admin')
  const isOwner = computed(() => localStorage.getItem('role') === 'owner')
  const isTenant = computed(() => localStorage.getItem('role') === 'tenant')
  const username = computed(() => localStorage.getItem('display_name') || '')

  async function login(username: string, password: string) {
    const res = await api.post('/auth/login/', { username, password })
    token.value = res.data.access
    refreshToken.value = res.data.refresh
    localStorage.setItem('access_token', res.data.access)
    localStorage.setItem('refresh_token', res.data.refresh)
    // 解析 JWT payload
    const payload = JSON.parse(atob(res.data.access.split('.')[1]))
    localStorage.setItem('role', payload.role)
    localStorage.setItem('display_name', payload.display_name)
    localStorage.setItem('username', payload.username)
    return payload
  }

  async function register(data: any) {
    return await api.post('/auth/register/', data)
  }

  async function fetchProfile() {
    const res = await api.get('/auth/profile/')
    userInfo.value = res.data
    return res.data
  }

  async function updateProfile(data: any) {
    const res = await api.put('/auth/profile/', data)
    userInfo.value = res.data
    // 同步更新 localStorage，右上角立即生效
    localStorage.setItem('display_name', res.data.display_name || res.data.username || '')
    return res.data
  }

  function logout() {
    token.value = ''
    refreshToken.value = ''
    userInfo.value = null
    localStorage.clear()
  }

  return {
    token, refreshToken, userInfo,
    isLoggedIn, isAdmin, isOwner, isTenant, username,
    login, register, fetchProfile, updateProfile, logout,
  }
})
