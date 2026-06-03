<template>
  <div class="favorites">
    <h2>我的收藏</h2>
    <el-row :gutter="20">
      <el-col :span="8" v-for="fav in favorites" :key="fav.id">
        <el-card shadow="hover" class="house-card" @click="$router.push(`/houses/${fav.house.id}`)">
          <h3>{{ fav.house.title }}</h3>
          <p>{{ fav.house.district_name }} · {{ fav.house.community }}</p>
          <p class="price">¥{{ fav.house.price }}/月</p>
        </el-card>
      </el-col>
    </el-row>
    <el-empty v-if="favorites.length===0" description="暂无收藏" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'

const favorites = ref<any[]>([])
onMounted(async () => { const res = await api.get('/houses/favorites/'); favorites.value = res.data.results || res.data })
</script>

<style scoped>
.house-card { cursor: pointer; margin-bottom: 16px; }
.price { color: #ff5500; font-weight: bold; }
</style>
