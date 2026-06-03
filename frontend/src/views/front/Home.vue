<template>
  <div class="home">
    <!-- 搜索栏 -->
    <section class="hero">
      <h1>找到你的理想之家</h1>
      <div class="search-bar">
        <el-input v-model="searchText" placeholder="搜索房源..." size="large" @keyup.enter="goSearch">
          <template #append>
            <el-button @click="goSearch"><el-icon><Search /></el-icon></el-button>
          </template>
        </el-input>
      </div>
    </section>

    <!-- 推荐房源 -->
    <section class="section">
      <h2>推荐房源</h2>
      <el-row :gutter="20">
        <el-col :span="8" v-for="house in recommended" :key="house.id">
          <el-card shadow="hover" class="house-card" @click="$router.push(`/houses/${house.id}`)">
            <div class="card-img">
              <img :src="house.cover_image || '/placeholder.png'" alt="" />
              <el-tag v-if="house.is_new" type="danger" class="tag">新上</el-tag>
            </div>
            <div class="card-body">
              <h3>{{ house.title }}</h3>
              <p class="location">{{ house.district_name }} {{ house.community }}</p>
              <p class="info">{{ house.layout_desc }} | {{ house.area_size }}㎡ | {{ house.orientation }}</p>
              <p class="price">¥{{ house.price }}<span>/月</span></p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </section>

    <!-- 最新房源 -->
    <section class="section">
      <h2>最新房源</h2>
      <el-row :gutter="20">
        <el-col :span="8" v-for="house in latest" :key="house.id">
          <el-card shadow="hover" class="house-card" @click="$router.push(`/houses/${house.id}`)">
            <div class="card-img">
              <img :src="house.cover_image || '/placeholder.png'" alt="" />
            </div>
            <div class="card-body">
              <h3>{{ house.title }}</h3>
              <p class="location">{{ house.district_name }} {{ house.community }}</p>
              <p class="info">{{ house.layout_desc }} | {{ house.area_size }}㎡</p>
              <p class="price">¥{{ house.price }}<span>/月</span></p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const searchText = ref('')
const recommended = ref<any[]>([])
const latest = ref<any[]>([])

onMounted(async () => {
  const [rec, lat] = await Promise.all([
    api.get('/houses/recommended/'),
    api.get('/houses/latest/'),
  ])
  recommended.value = rec.data
  latest.value = lat.data
})

function goSearch() {
  router.push({ path: '/houses', query: { search: searchText.value } })
}
</script>

<style scoped>
.hero { text-align: center; padding: 60px 0 40px; background: linear-gradient(135deg, #409eff 0%, #53a8ff 100%); border-radius: 8px; color: #fff; margin-bottom: 30px; }
.hero h1 { font-size: 32px; margin-bottom: 20px; }
.search-bar { max-width: 600px; margin: 0 auto; }
.section { margin-bottom: 30px; }
.section h2 { font-size: 20px; margin-bottom: 16px; }
.house-card { cursor: pointer; margin-bottom: 20px; }
.house-card:hover { transform: translateY(-2px); transition: 0.3s; }
.card-img { position: relative; height: 180px; overflow: hidden; border-radius: 4px; }
.card-img img { width: 100%; height: 100%; object-fit: cover; }
.tag { position: absolute; top: 8px; left: 8px; }
.card-body { padding: 10px 0 0; }
.card-body h3 { font-size: 14px; margin-bottom: 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.location { color: #999; font-size: 12px; margin-bottom: 4px; }
.info { color: #666; font-size: 12px; margin-bottom: 6px; }
.price { color: #ff5500; font-size: 20px; font-weight: bold; }
.price span { font-size: 12px; color: #999; font-weight: normal; }
</style>
