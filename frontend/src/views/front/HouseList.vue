<template>
  <div class="house-list">
    <h1>房源列表</h1>

    <!-- 搜索框 -->
    <div class="search-bar">
      <el-input v-model="searchText" placeholder="搜索房源（小区名、地址、标题）" size="large" clearable @keyup.enter="onSearch" @clear="onSearch">
        <template #append>
          <el-button @click="onSearch"><el-icon><Search /></el-icon></el-button>
        </template>
      </el-input>
    </div>

    <!-- 筛选区 -->
    <el-card class="filter-card">
      <!-- 城市已在头部选择，这里显示当前城市 -->
      <div class="filter-row">
        <span class="filter-label">城市：</span>
        <div class="filter-options">
          <el-tag type="">{{ locationStore.cityName || '未选择' }}</el-tag>
        </div>
      </div>
      <!-- 区域筛选 -->
      <div class="filter-row">
        <span class="filter-label">区域：</span>
        <div class="filter-options">
          <el-tag :type="!filters.district ? '' : 'info'" @click="filters.district=undefined;filters.area=undefined">不限</el-tag>
          <el-tag v-for="d in filteredDistricts" :key="d.id" :type="filters.district===d.id ? '' : 'info'" @click="selectDistrict(d)">{{ d.name }}</el-tag>
        </div>
      </div>
      <!-- 商圈筛选 -->
      <div class="filter-row" v-if="currentAreas.length">
        <span class="filter-label">商圈：</span>
        <div class="filter-options">
          <el-tag :type="!filters.area ? '' : 'info'" @click="filters.area=undefined;filters.community=undefined;communityOptions=[]">不限</el-tag>
          <el-tag v-for="a in currentAreas" :key="a.id" :type="filters.area===a.id ? '' : 'info'" @click="selectArea(a)">{{ a.name }}</el-tag>
        </div>
      </div>
      <!-- 小区筛选（选商圈后显示） -->
      <div class="filter-row">
        <span class="filter-label">小区：</span>
        <div class="filter-options">
          <template v-if="filters.area && communityOptions.length">
            <el-tag :type="!filters.community ? '' : 'info'" @click="filters.community=undefined">不限</el-tag>
            <el-tag v-for="c in communityOptions" :key="c.id" :type="filters.community===c.value ? '' : 'info'" @click="filters.community=c.value">{{ c.label }}</el-tag>
          </template>
          <span v-else class="no-data">-</span>
        </div>
      </div>
      <!-- 方式 -->
      <div class="filter-row">
        <span class="filter-label">方式：</span>
        <div class="filter-options">
          <el-tag :type="!filters.category ? '' : 'info'" @click="filters.category=undefined">不限</el-tag>
          <el-tag v-for="c in categories" :key="c.id" :type="filters.category===c.id ? '' : 'info'" @click="filters.category=c.id">{{ c.name }}</el-tag>
        </div>
      </div>
      <!-- 租金 -->
      <div class="filter-row">
        <span class="filter-label">租金：</span>
        <div class="filter-options">
          <el-tag :type="!priceRange ? '' : 'info'" @click="clearPrice">不限</el-tag>
          <el-tag v-for="p in priceRanges" :key="p.label" :type="priceRange===p.label ? '' : 'info'" @click="setPrice(p)">{{ p.label }}</el-tag>
        </div>
      </div>
      <!-- 户型 -->
      <div class="filter-row">
        <span class="filter-label">户型：</span>
        <div class="filter-options">
          <el-tag :type="!filters.room_count ? '' : 'info'" @click="filters.room_count=undefined">不限</el-tag>
          <el-tag v-for="r in [1,2,3,4]" :key="r" :type="filters.room_count===r ? '' : 'info'" @click="filters.room_count=r">{{ r===4 ? '四居+' : r+'居' }}</el-tag>
        </div>
      </div>
      <!-- 更多筛选 -->
      <div class="filter-row">
        <span class="filter-label">更多：</span>
        <div class="filter-options">
          <el-checkbox v-model="filters.has_subway">近地铁</el-checkbox>
          <el-checkbox v-model="filters.has_elevator">有电梯</el-checkbox>
          <el-select v-model="filters.orientation" clearable placeholder="朝向" size="small" style="width:100px;margin-left:8px">
            <el-option v-for="o in orientationOptions" :key="o" :label="o" :value="o" />
          </el-select>
          <el-select v-model="filters.decoration" clearable placeholder="装修" size="small" style="width:100px;margin-left:8px">
            <el-option v-for="d in decorationOptions" :key="d" :label="d" :value="d" />
          </el-select>
        </div>
      </div>
    </el-card>

    <!-- 排序 -->
    <div class="sort-bar">
      <el-radio-group v-model="ordering" size="small">
        <el-radio-button value="">默认</el-radio-button>
        <el-radio-button value="-created_at">最新</el-radio-button>
        <el-radio-button value="price">价格↑</el-radio-button>
        <el-radio-button value="-price">价格↓</el-radio-button>
        <el-radio-button value="-area_size">面积↓</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 未选城市时的引导提示 -->
    <el-empty v-if="!selectedCity" description="请先选择城市以查看房源" />

    <!-- 房源列表 -->
    <el-row :gutter="20" v-loading="loading" v-else>
      <el-col :span="8" v-for="house in houses" :key="house.id">
        <el-card shadow="hover" class="house-card" @click="$router.push(`/houses/${house.id}`)">
          <div class="card-img">
            <img :src="house.cover_image || '/placeholder.png'" alt="" />
            <div class="tags">
              <el-tag v-if="house.is_new" type="danger" size="small">新上</el-tag>
              <el-tag v-if="house.has_subway" type="warning" size="small">近地铁</el-tag>
            </div>
          </div>
          <div class="card-body">
            <h3>{{ house.title }}</h3>
            <p class="location">{{ house.district_name }} · {{ house.area_name }} · {{ house.community }}</p>
            <p class="info">{{ house.layout_desc }} | {{ house.area_size }}㎡ | {{ house.orientation }} | {{ house.floor_level }}</p>
            <p class="price">¥{{ house.price }}<span>/月</span></p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 空状态 -->
    <el-empty v-if="selectedCity && !loading && houses.length===0" description="暂无符合条件的房源" />

    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <el-pagination
        v-model:current-page="page"
        :page-size="9"
        :total="total"
        layout="prev, pager, next"
        @current-change="fetchHouses"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'
import { useLocationStore } from '@/stores/location'

const route = useRoute()
const locationStore = useLocationStore()
const loading = ref(false)
const houses = ref<any[]>([])
const districts = ref<any[]>([])
const categories = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const ordering = ref('')
const priceRange = ref('')
const searchText = ref(route.query.search as string || '')
const communityOptions = ref<any[]>([])

// 从 location store 读取选中的城市
const selectedProvince = computed(() => locationStore.selectedProvince)
const selectedCity = computed(() => locationStore.selectedCity)

const filters = reactive<any>({
  district: undefined, area: undefined, community: undefined, category: undefined,
  room_count: undefined, orientation: undefined, decoration: undefined,
  has_subway: false, has_elevator: false,
  min_price: undefined, max_price: undefined,
})

const orientationOptions = ref<string[]>([])
const decorationOptions = ref<string[]>([])

const priceRanges = [
  { label: '≤800', min: 0, max: 800 },
  { label: '800-1200', min: 800, max: 1200 },
  { label: '1200-1600', min: 1200, max: 1600 },
  { label: '1600-2000', min: 1600, max: 2000 },
  { label: '2000-2500', min: 2000, max: 2500 },
  { label: '2500-3000', min: 2500, max: 3000 },
  { label: '3000-6000', min: 3000, max: 6000 },
  { label: '≥6000', min: 6000, max: 999999 },
]

// 选了城市则过滤区域
const filteredDistricts = computed(() => {
  if (!selectedCity.value) return districts.value
  return districts.value.filter((d: any) => d.city === selectedCity.value)
})

const currentAreas = computed(() => {
  const d = districts.value.find((x: any) => x.id === filters.district)
  return d ? d.areas : []
})

function onSearch() {
  page.value = 1
  if (selectedCity.value) fetchHouses()
}

function selectDistrict(d: any) {
  filters.district = d.id
  filters.area = undefined
  filters.community = undefined
  communityOptions.value = []
}

async function selectArea(a: any) {
  filters.area = a.id
  filters.community = undefined
  // 从字典加载该商圈的小区名
  const res = await api.get('/houses/dicts/', { params: { group: 'community', area: a.id } })
  communityOptions.value = res.data
}

function setPrice(p: any) { priceRange.value = p.label; filters.min_price = p.min; filters.max_price = p.max }
function clearPrice() { priceRange.value = ''; filters.min_price = undefined; filters.max_price = undefined }

async function fetchHouses() {
  loading.value = true
  const params: any = { page: page.value }
  if (searchText.value) params.search = searchText.value
  if (ordering.value) params.ordering = ordering.value
  if (filters.district) {
    params.district = filters.district
  } else if (selectedCity.value) {
    // 选了城市但未选区域，传该城市所有区域ID
    const districtIds = filteredDistricts.value.map((d: any) => d.id)
    if (districtIds.length) params.district__in = districtIds.join(',')
  }
  if (filters.area) params.area = filters.area
  if (filters.community) params.community = filters.community
  if (filters.category) params.category = filters.category
  if (filters.room_count) params.room_count = filters.room_count
  if (filters.orientation) params.orientation = filters.orientation
  if (filters.decoration) params.decoration = filters.decoration
  if (filters.has_subway) params.has_subway = true
  if (filters.has_elevator) params.has_elevator = true
  if (filters.min_price) params.min_price = filters.min_price
  if (filters.max_price && filters.max_price < 999999) params.max_price = filters.max_price

  try {
    const res = await api.get('/houses/', { params })
    houses.value = res.data.results || res.data
    total.value = res.data.count || houses.value.length
  } finally { loading.value = false }
}

onMounted(async () => {
  await locationStore.loadProvinces()
  const [distRes, catRes, oriRes, decRes] = await Promise.all([
    api.get('/houses/districts/'),
    api.get('/houses/categories/'),
    api.get('/houses/dicts/', { params: { group: 'orientation' } }),
    api.get('/houses/dicts/', { params: { group: 'decoration' } }),
  ])
  districts.value = distRes.data
  categories.value = catRes.data
  orientationOptions.value = oriRes.data.map((d: any) => d.value)
  decorationOptions.value = decRes.data.map((d: any) => d.value)
  // 如果已有选中城市，自动加载数据
  if (selectedCity.value) fetchHouses()
})

watch(filters, () => {
  if (!selectedCity.value) return
  page.value = 1; fetchHouses()
}, { deep: true })
watch(ordering, () => {
  if (!selectedCity.value) return
  page.value = 1; fetchHouses()
})
// 监听头部城市切换
watch(() => locationStore.selectedCity, (newCity) => {
  if (newCity) {
    filters.district = undefined
    filters.area = undefined
    page.value = 1
    fetchHouses()
  } else {
    houses.value = []
    total.value = 0
  }
})
</script>

<style scoped>
.house-list h1 { margin-bottom: 16px; }
.search-bar { margin-bottom: 16px; }
.filter-card { margin-bottom: 16px; }
.filter-row { display: flex; align-items: flex-start; margin-bottom: 10px; }
.filter-label { width: 50px; font-size: 14px; color: #666; line-height: 32px; flex-shrink: 0; }
.filter-options { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.filter-options .el-tag { cursor: pointer; }
.no-data { color: #ccc; font-size: 14px; line-height: 32px; }
.sort-bar { margin-bottom: 16px; }
.house-card { cursor: pointer; margin-bottom: 20px; }
.house-card:hover { transform: translateY(-2px); transition: 0.3s; }
.card-img { position: relative; height: 180px; overflow: hidden; border-radius: 4px; }
.card-img img { width: 100%; height: 100%; object-fit: cover; }
.tags { position: absolute; top: 8px; left: 8px; display: flex; gap: 4px; }
.card-body { padding: 10px 0 0; }
.card-body h3 { font-size: 14px; margin-bottom: 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.location { color: #999; font-size: 12px; margin-bottom: 4px; }
.info { color: #666; font-size: 12px; margin-bottom: 6px; }
.price { color: #ff5500; font-size: 20px; font-weight: bold; }
.price span { font-size: 12px; color: #999; font-weight: normal; }
.pagination { display: flex; justify-content: center; margin-top: 20px; }
</style>
