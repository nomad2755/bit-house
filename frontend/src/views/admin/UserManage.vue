<template>
  <div>
    <h2>用户管理</h2>
    <el-table :data="users" stripe v-loading="loading">
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="display_name" label="昵称" />
      <el-table-column prop="role" label="角色" width="80">
        <template #default="{ row }">
          <el-tag :type="row.role==='admin'?'danger':row.role==='owner'?'warning':''">{{ row.role }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="phone" label="手机号" width="120" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }"><el-tag :type="row.is_active?'success':'danger'">{{ row.is_active?'正常':'禁用' }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="date_joined" label="注册时间" width="160" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

const loading = ref(false)
const users = ref<any[]>([])
onMounted(async () => {
  loading.value = true
  try { const res = await api.get('/auth/list/'); users.value = res.data.results || res.data }
  finally { loading.value = false }
})
</script>
