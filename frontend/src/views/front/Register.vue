<template>
  <div class="register-page">
    <el-card class="register-card">
      <h2>注册 Bit House</h2>
      <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleRegister">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="phone">
          <el-input v-model="form.phone" placeholder="手机号（大陆 / 香港 / 澳门）" prefix-icon="Phone" size="large" />
        </el-form-item>
        <el-form-item>
          <el-select v-model="form.role" placeholder="选择角色" size="large" style="width:100%">
            <el-option label="租客" value="tenant" />
            <el-option label="房东" value="owner" />
          </el-select>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码(至少6位)" prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item prop="password2">
          <el-input v-model="form.password2" type="password" placeholder="确认密码" prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-button type="primary" size="large" :loading="loading" @click="handleRegister" style="width:100%">注册</el-button>
      </el-form>
      <p class="login-link">已有账号？<router-link to="/login">去登录</router-link></p>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const formRef = ref<FormInstance>()
const form = reactive({ username: '', phone: '', role: 'tenant', password: '', password2: '' })

// 手机号格式校验：大陆 / 香港 / 澳门
const validatePhone = (_rule: any, value: string, callback: any) => {
  if (!value) return callback() // 手机号非必填
  // 大陆：1[3-9]开头，共11位
  const mainland = /^1[3-9]\d{9}$/
  // 香港：+852或无前缀，[569]开头，共8位
  const hongkong = /^(\+852)?[569]\d{7}$/
  // 澳门：+853或无前缀，6开头，共8位
  const macau = /^(\+853)?6\d{7}$/
  if (mainland.test(value) || hongkong.test(value) || macau.test(value)) {
    callback()
  } else {
    callback(new Error('请输入大陆、香港或澳门手机号'))
  }
}

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  phone: [{ validator: validatePhone, trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' },
  ],
  password2: [{ required: true, message: '请确认密码', trigger: 'blur' }],
}

async function handleRegister() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await userStore.register(form)
    await userStore.login(form.username, form.password)
    ElMessage.success('注册成功，已自动登录')
    router.push('/')
  } catch (e: any) {
    // 错误已由 Axios 拦截器显示
  } finally { loading.value = false }
}
</script>

<style scoped>
.register-page { display: flex; justify-content: center; align-items: center; min-height: 80vh; }
.register-card { width: 400px; }
h2 { text-align: center; margin-bottom: 24px; }
.login-link { text-align: center; margin-top: 16px; font-size: 14px; }
</style>
