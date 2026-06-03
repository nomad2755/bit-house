<template>
  <div class="contract-detail" v-loading="loading">
    <template v-if="contract">
      <el-card>
        <h2>合同详情 - {{ contract.contract_no }}</h2>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="房源">{{ contract.house_title }}</el-descriptions-item>
          <el-descriptions-item label="状态"><el-tag>{{ contract.status_display }}</el-tag></el-descriptions-item>
          <el-descriptions-item label="甲方(房东)">{{ contract.landlord_name }} {{ contract.landlord_phone }}</el-descriptions-item>
          <el-descriptions-item label="乙方(租客)">{{ contract.tenant_name }} {{ contract.tenant_phone }}</el-descriptions-item>
          <el-descriptions-item label="租赁期限">{{ contract.start_date }} ~ {{ contract.end_date }} ({{ contract.lease_months }}个月)</el-descriptions-item>
          <el-descriptions-item label="月租金">¥{{ contract.rent_amount }}</el-descriptions-item>
          <el-descriptions-item label="押金">¥{{ contract.deposit_amount }}</el-descriptions-item>
          <el-descriptions-item label="付款周期">{{ contract.payment_cycle_display }}</el-descriptions-item>
          <el-descriptions-item label="租金总额">¥{{ contract.total_rent }}</el-descriptions-item>
          <el-descriptions-item label="签约方式">{{ contract.sign_method }}</el-descriptions-item>
          <el-descriptions-item label="特别约定" :span="2">{{ contract.special_terms || '无' }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 缴费记录 -->
      <el-card style="margin-top:16px" v-if="contract.payments?.length">
        <h3>租金缴纳计划</h3>
        <el-table :data="contract.payments" stripe>
          <el-table-column label="账期" width="220">
            <template #default="{ row }">{{ row.period_start }} ~ {{ row.period_end }}</template>
          </el-table-column>
          <el-table-column prop="amount" label="应付金额" width="100" />
          <el-table-column prop="due_date" label="应付日期" width="120" />
          <el-table-column label="状态" width="100">
            <template #default="{ row }"><el-tag :type="row.status==='confirmed'?'success':row.is_overdue?'danger':'warning'">{{ row.status_display }}</el-tag></template>
          </el-table-column>
        </el-table>
      </el-card>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'

const route = useRoute()
const loading = ref(false)
const contract = ref<any>(null)

onMounted(async () => {
  loading.value = true
  try { const res = await api.get(`/orders/contracts/${route.params.id}/`); contract.value = res.data }
  finally { loading.value = false }
})
</script>
