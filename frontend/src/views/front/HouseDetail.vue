<template>
  <div class="house-detail" v-loading="loading">
    <template v-if="house">
      <!-- 图片区 -->
      <el-carousel height="400px" v-if="house.images?.length">
        <el-carousel-item v-for="img in house.images" :key="img.id">
          <img :src="img.image" class="carousel-img" />
        </el-carousel-item>
      </el-carousel>

      <el-row :gutter="20" style="margin-top:20px">
        <el-col :span="16">
          <!-- 基本信息 -->
          <el-card>
            <h1>{{ house.title }}</h1>
            <div class="meta">
              <el-tag v-for="tag in houseTags" :key="tag" size="small" style="margin-right:4px">{{ tag }}</el-tag>
            </div>
            <el-descriptions :column="3" border style="margin-top:16px">
              <el-descriptions-item label="月租金"><span class="price">¥{{ house.price }}</span></el-descriptions-item>
              <el-descriptions-item label="押金">¥{{ house.deposit }}</el-descriptions-item>
              <el-descriptions-item label="付款方式">{{ house.pay_type }}</el-descriptions-item>
              <el-descriptions-item label="户型">{{ house.layout_desc }}</el-descriptions-item>
              <el-descriptions-item label="面积">{{ house.area_size }}㎡</el-descriptions-item>
              <el-descriptions-item label="朝向">{{ house.orientation }}</el-descriptions-item>
              <el-descriptions-item label="楼层">{{ house.floor_level }}（{{ house.floor }}/{{ house.total_floors }}层）</el-descriptions-item>
              <el-descriptions-item label="装修">{{ house.decoration }}</el-descriptions-item>
              <el-descriptions-item label="电梯">{{ house.has_elevator ? '有' : '无' }}</el-descriptions-item>
              <el-descriptions-item label="区域">{{ house.district_name }}</el-descriptions-item>
              <el-descriptions-item label="商圈">{{ house.area_name }}</el-descriptions-item>
              <el-descriptions-item label="小区">{{ house.community }}</el-descriptions-item>
            </el-descriptions>
            <div class="facilities" v-if="house.facilities?.length" style="margin-top:16px">
              <h3>配套设施</h3>
              <el-tag v-for="f in house.facilities" :key="f" type="info" style="margin:2px">{{ f }}</el-tag>
            </div>
            <div style="margin-top:16px">
              <h3>房源描述</h3>
              <p>{{ house.description }}</p>
            </div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <!-- 操作区 -->
          <el-card>
            <div class="actions">
              <el-button type="primary" size="large" style="width:100%" @click="handleBook" :disabled="house.status!==0">预约看房</el-button>
              <el-button size="large" style="width:100%;margin-top:10px" @click="handleContract" :disabled="house.status!==0">申请签约</el-button>
              <el-button :type="house.is_favorited ? 'danger' : 'default'" style="width:100%;margin-top:10px" @click="toggleFav">
                {{ house.is_favorited ? '已收藏' : '收藏' }}
              </el-button>
            </div>
          </el-card>
          <!-- 房东信息 -->
          <el-card style="margin-top:16px">
            <h3>房东信息</h3>
            <p>{{ house.owner_name }}</p>
            <p class="sub">浏览 {{ house.view_count }} 次</p>
          </el-card>
        </el-col>
      </el-row>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const house = ref<any>(null)

const houseTags = computed(() => {
  if (!house.value) return []
  const tags = []
  if (house.value.is_new) tags.push('新上')
  if (house.value.has_subway) tags.push('近地铁')
  if (house.value.has_elevator) tags.push('有电梯')
  tags.push(house.value.category_name)
  return tags
})

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get(`/houses/${route.params.id}/`)
    house.value = res.data
  } finally { loading.value = false }
})

async function toggleFav() {
  if (!userStore.isLoggedIn) return router.push('/login')
  await api.post('/houses/favorites/', { house: house.value.id })
  house.value.is_favorited = !house.value.is_favorited
  ElMessage.success(house.value.is_favorited ? '已收藏' : '已取消收藏')
}

function handleBook() {
  if (!userStore.isLoggedIn) return router.push('/login')
  ElMessage.info('看房预约功能开发中')
}

function handleContract() {
  if (!userStore.isLoggedIn) return router.push('/login')
  router.push({ path: '/contracts', query: { house_id: house.value.id } })
}
</script>

<style scoped>
.carousel-img { width: 100%; height: 400px; object-fit: cover; }
.price { color: #ff5500; font-size: 24px; font-weight: bold; }
.sub { color: #999; font-size: 12px; margin-top: 8px; }
</style>
