<template>
  <div>
    <h2>房源管理</h2>
    <el-table :data="houses" stripe v-loading="loading">
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="district_name" label="区域" width="100" />
      <el-table-column prop="community" label="小区" width="120" />
      <el-table-column prop="price" label="月租" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status===0?'success':row.status===1?'warning':'info'">
            {{ row.status===0?'出租中':row.status===1?'已租出':'已下架' }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

const loading = ref(false)
const houses = ref<any[]>([])
onMounted(async () => {
  loading.value = true
  try { const res = await api.get('/houses/', { params: { status: '' } }); houses.value = res.data.results || res.data }
  finally { loading.value = false }
})
</script>
