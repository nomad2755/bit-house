<template>
  <div class="profile">
    <el-card>
      <h2>个人中心</h2>
      <el-form :model="form" label-width="80px" v-if="form">
        <el-form-item label="用户名"><el-input v-model="form.username" disabled /></el-form-item>
        <el-form-item label="昵称"><el-input v-model="form.display_name" /></el-form-item>
        <el-form-item label="手机号"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
        <el-form-item label="身份证"><el-input v-model="form.id_card" /></el-form-item>
        <el-form-item label="角色"><el-tag>{{ form.role }}</el-tag></el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const form = ref<any>(null)

onMounted(async () => { form.value = await userStore.fetchProfile() })

async function handleSave() {
  await userStore.updateProfile(form.value)
  ElMessage.success('保存成功')
}
</script>
