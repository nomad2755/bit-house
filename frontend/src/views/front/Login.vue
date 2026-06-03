<template>
  <div class="login-page">
    <router-link to="/" class="back-home">
      <el-icon><HomeFilled /></el-icon> 返回首页
    </router-link>
    <el-card class="login-card">
      <h2>登录 Bit House</h2>
      <el-form :model="form" @submit.prevent="handleLogin">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名 / 手机号 / 身份证号" prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-button type="primary" size="large" :loading="loading" @click="handleLogin" style="width:100%">登录</el-button>
      </el-form>
      <p class="register-link">还没有账号？<router-link to="/register">立即注册</router-link></p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const form = reactive({ username: '', password: '' })

async function handleLogin() {
  if (!form.username || !form.password) {
    return ElMessage.warning('请填写完整')
  }
  loading.value = true
  try {
    await userStore.login(form.username, form.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (e: any) {
    // 错误已由 api 拦截器统一处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page { display: flex; justify-content: center; align-items: center; min-height: 80vh; position: relative; }
.back-home { position: absolute; top: 20px; left: 20px; font-size: 14px; color: #409eff; text-decoration: none; display: flex; align-items: center; gap: 4px; }
.back-home:hover { text-decoration: underline; }
.login-card { width: 400px; }
h2 { text-align: center; margin-bottom: 24px; }
.register-link { text-align: center; margin-top: 16px; font-size: 14px; }
</style>
