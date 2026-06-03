<template>
  <div class="dashboard">
    <h2>仪表盘</h2>
    <el-row :gutter="20">
      <el-col :span="6" v-for="card in cards" :key="card.title">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" :style="{ background: card.color }">
            <el-icon :size="24"><component :is="card.icon" /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-value">{{ card.value }}</p>
            <p class="stat-title">{{ card.title }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

const cards = ref([
  { title: '总用户', value: 0, icon: 'User', color: '#409eff' },
  { title: '总房源', value: 0, icon: 'House', color: '#67c23a' },
  { title: '总合同', value: 0, icon: 'Document', color: '#e6a23c' },
  { title: '总收入', value: '¥0', icon: 'Money', color: '#f56c6c' },
])

onMounted(async () => {
  // Fetch dashboard stats (placeholder - would need a dedicated endpoint)
  try {
    const [users, houses] = await Promise.all([
      api.get('/auth/list/'),
      api.get('/houses/'),
    ])
    cards.value[0].value = users.data.count || users.data.length || 0
    cards.value[1].value = houses.data.count || houses.data.length || 0
  } catch (e) {}
})
</script>

<style scoped>
.stat-card { display: flex; align-items: center; padding: 20px; }
.stat-card :deep(.el-card__body) { display: flex; align-items: center; gap: 16px; width: 100%; }
.stat-icon { width: 48px; height: 48px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #fff; }
.stat-value { font-size: 24px; font-weight: bold; }
.stat-title { color: #999; font-size: 14px; }
</style>
