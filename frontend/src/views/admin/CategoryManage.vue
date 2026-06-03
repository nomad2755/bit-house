<template>
  <div>
    <h2>分类管理</h2>
    <el-table :data="categories" stripe v-loading="loading">
      <el-table-column prop="name" label="分类名称" />
      <el-table-column prop="sort" label="排序" width="80" />
      <el-table-column prop="description" label="描述" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

const loading = ref(false)
const categories = ref<any[]>([])
onMounted(async () => {
  loading.value = true
  try { const res = await api.get('/houses/categories/'); categories.value = res.data.results || res.data }
  finally { loading.value = false }
})
</script>
