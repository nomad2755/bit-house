<template>
  <div class="owner-houses">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>我的房源</h2>
          <el-button type="primary" @click="$router.push('/owner/houses/create')">发布房源</el-button>
        </div>
      </template>

      <!-- 状态筛选 -->
      <el-radio-group v-model="statusFilter" @change="loadHouses" style="margin-bottom:16px">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="0">出租中</el-radio-button>
        <el-radio-button label="1">已租出</el-radio-button>
        <el-radio-button label="2">已下架</el-radio-button>
      </el-radio-group>

      <!-- 房源列表 -->
      <el-table :data="houses" v-loading="loading" stripe>
        <el-table-column prop="title" label="标题" min-width="150" />
        <el-table-column prop="district_name" label="区域" width="100" />
        <el-table-column prop="community" label="小区" width="120" />
        <el-table-column label="月租" width="100">
          <template #default="{ row }">¥{{ row.price }}</template>
        </el-table-column>
        <el-table-column prop="layout_desc" label="户型" width="100" />
        <el-table-column prop="area_size" label="面积" width="80">
          <template #default="{ row }">{{ row.area_size }}㎡</template>
        </el-table-column>
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag v-if="row.status===0" type="success">出租中</el-tag>
            <el-tag v-else-if="row.status===1" type="warning">已租出</el-tag>
            <el-tag v-else type="info">已下架</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/owner/houses/${row.id}/edit`)">编辑</el-button>
            <el-button v-if="row.status===2" size="small" type="success" @click="updateStatus(row,0)">上架</el-button>
            <el-button v-else size="small" type="warning" @click="updateStatus(row,2)">下架</el-button>
            <el-button size="small" type="danger" @click="deleteHouse(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const houses = ref<any[]>([])
const statusFilter = ref('')

async function loadHouses() {
  loading.value = true
  try {
    const params: any = {}
    if (statusFilter.value !== '') params.status = statusFilter.value
    const res = await api.get('/houses/my/', { params })
    houses.value = res.data.results || res.data
  } finally { loading.value = false }
}

async function updateStatus(row: any, status: number) {
  await api.patch(`/houses/${row.id}/update/`, { status })
  ElMessage.success(status === 0 ? '已上架' : '已下架')
  loadHouses()
}

async function deleteHouse(row: any) {
  await ElMessageBox.confirm(`确定删除「${row.title}」？`, '提示', { type: 'warning' })
  await api.delete(`/houses/${row.id}/delete/`)
  ElMessage.success('已删除')
  loadHouses()
}

onMounted(loadHouses)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.card-header h2 { margin: 0; font-size: 18px; }
</style>
