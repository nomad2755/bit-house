<template>
  <div class="contracts">
    <h2>我的合同</h2>
    <el-table :data="contracts" stripe v-loading="loading">
      <el-table-column prop="contract_no" label="合同编号" width="180" />
      <el-table-column prop="house_title" label="房源" />
      <el-table-column prop="landlord_name" label="房东" width="100" />
      <el-table-column prop="tenant_name" label="租客" width="100" />
      <el-table-column label="租期">
        <template #default="{ row }">{{ row.start_date }} ~ {{ row.end_date }}</template>
      </el-table-column>
      <el-table-column prop="rent_amount" label="月租金" width="100">
        <template #default="{ row }"><span style="color:#ff5500">¥{{ row.rent_amount }}</span></template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)">{{ row.status_display }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button type="primary" link @click="$router.push(`/contracts/${row.id}`)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!loading && contracts.length===0" description="暂无合同" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

const loading = ref(false)
const contracts = ref<any[]>([])

function statusType(s: string) {
  const map: any = { draft: 'info', pending_sign: 'warning', active: 'success', expired: '', terminated: 'danger', renewed: 'info' }
  return map[s] || ''
}

onMounted(async () => {
  loading.value = true
  try { const res = await api.get('/orders/contracts/'); contracts.value = res.data.results || res.data }
  finally { loading.value = false }
})
</script>
