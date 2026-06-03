<template>
  <div>
    <h2>合同管理</h2>
    <el-table :data="contracts" stripe v-loading="loading">
      <el-table-column prop="contract_no" label="合同编号" width="180" />
      <el-table-column prop="house_title" label="房源" />
      <el-table-column prop="landlord_name" label="房东" width="80" />
      <el-table-column prop="tenant_name" label="租客" width="80" />
      <el-table-column prop="rent_amount" label="月租" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }"><el-tag>{{ row.status_display }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

const loading = ref(false)
const contracts = ref<any[]>([])
onMounted(async () => {
  loading.value = true
  try { const res = await api.get('/orders/contracts/'); contracts.value = res.data.results || res.data }
  finally { loading.value = false }
})
</script>
