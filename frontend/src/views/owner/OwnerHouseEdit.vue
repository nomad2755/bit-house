<template>
  <div class="house-edit" v-loading="pageLoading">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>{{ isEdit ? '编辑房源' : '发布房源' }}</h2>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <!-- 基本信息 -->
        <h3 class="section-title">基本信息</h3>
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="如：精装修两居室 近地铁" maxlength="100" show-word-limit />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="分类" prop="category">
              <el-select v-model="form.category" placeholder="选择分类" style="width:100%">
                <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="区域" prop="district">
              <el-select v-model="form.district" placeholder="选择区域" style="width:100%" @change="onDistrictChange">
                <el-option v-for="d in districts" :key="d.id" :label="d.name" :value="d.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="商圈">
              <el-select v-model="form.area_ref" placeholder="选择商圈" style="width:100%" clearable @change="onAreaChange">
                <el-option v-for="a in currentAreas" :key="a.id" :label="a.name" :value="a.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="小区名" prop="community">
              <el-select v-model="form.community" placeholder="选择小区名" style="width:100%" filterable allow-create>
                <el-option v-for="c in communityOptions" :key="c.id" :label="c.label" :value="c.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="详细地址">
              <el-input v-model="form.address" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 价格与面积 -->
        <h3 class="section-title">价格与面积</h3>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="月租(元)" prop="price">
              <el-input-number v-model="form.price" :min="0" :step="100" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="押金(元)">
              <el-input-number v-model="form.deposit" :min="0" :step="100" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="面积(㎡)" prop="area_size">
              <el-input-number v-model="form.area_size" :min="1" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 户型与楼层 -->
        <h3 class="section-title">户型与楼层</h3>
        <el-row :gutter="16">
          <el-col :span="6">
            <el-form-item label="卧室"><el-input-number v-model="form.room_count" :min="0" :max="10" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="客厅"><el-input-number v-model="form.hall_count" :min="0" :max="5" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="卫生间"><el-input-number v-model="form.toilet_count" :min="0" :max="5" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="当前楼层"><el-input-number v-model="form.floor" :min="1" style="width:100%" /></el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="6">
            <el-form-item label="总楼层"><el-input-number v-model="form.total_floors" :min="1" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="朝向">
              <el-select v-model="form.orientation" placeholder="选择" style="width:100%" clearable>
                <el-option v-for="o in orientations" :key="o" :label="o" :value="o" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="装修">
              <el-select v-model="form.decoration" placeholder="选择" style="width:100%" clearable>
                <el-option v-for="d in decorations" :key="d" :label="d" :value="d" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="付款方式">
              <el-select v-model="form.pay_type" placeholder="选择" style="width:100%" clearable>
                <el-option v-for="p in payTypes" :key="p" :label="p" :value="p" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="6">
            <el-form-item label="租期">
              <el-select v-model="form.lease_term" placeholder="选择" style="width:100%" clearable>
                <el-option v-for="l in leaseTerms" :key="l" :label="l" :value="l" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="有电梯"><el-switch v-model="form.has_elevator" /></el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="近地铁"><el-switch v-model="form.has_subway" /></el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="配套设施">
              <el-select v-model="form.facilities" multiple placeholder="选择" style="width:100%" clearable>
                <el-option v-for="f in facilityOptions" :key="f" :label="f" :value="f" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 描述 -->
        <h3 class="section-title">房源描述</h3>
        <el-form-item label="摘要">
          <el-input v-model="form.summary" maxlength="200" show-word-limit placeholder="一句话概括房源亮点" />
        </el-form-item>
        <el-form-item label="详细描述">
          <el-input v-model="form.description" type="textarea" :rows="6" placeholder="详细描述房源特点、周边配套、交通情况等" />
        </el-form-item>

        <!-- 图片管理 -->
        <h3 class="section-title">房源图片</h3>
        <el-form-item>
          <!-- 已有图片 -->
          <div class="image-list" v-if="existingImages.length">
            <div class="image-item" v-for="img in existingImages" :key="img.id">
              <el-image :src="img.image" fit="cover" :preview-src-list="[img.image]" style="width:140px;height:100px;border-radius:4px" />
              <el-button class="del-btn" type="danger" :icon="Delete" circle size="small" @click="removeExistingImage(img)" />
            </div>
          </div>
          <!-- 上传新图片 -->
          <el-upload
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :file-list="newImageFiles"
            :on-change="onFileChange"
            :on-remove="onFileRemove"
            multiple
            accept="image/*"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <!-- 提交 -->
        <el-form-item>
          <el-button type="primary" size="large" :loading="saving" @click="handleSave">
            {{ isEdit ? '保存修改' : '发布房源' }}
          </el-button>
          <el-button size="large" @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, Plus } from '@element-plus/icons-vue'
import type { FormInstance, FormRules, UploadFile } from 'element-plus'

const route = useRoute()
const router = useRouter()
const houseId = computed(() => route.params.id ? Number(route.params.id) : null)
const isEdit = computed(() => !!houseId.value)

const pageLoading = ref(false)
const saving = ref(false)
const formRef = ref<FormInstance>()
const categories = ref<any[]>([])
const districts = ref<any[]>([])
const existingImages = ref<any[]>([])
const newImageFiles = ref<UploadFile[]>([])

// 从字典 API 加载的选项
const orientations = ref<string[]>([])
const decorations = ref<string[]>([])
const payTypes = ref<string[]>([])
const leaseTerms = ref<string[]>([])
const facilityOptions = ref<string[]>([])
const communityOptions = ref<any[]>([])

const form = reactive({
  title: '', category: null as number | null, district: null as number | null,
  area_ref: null as number | null, community: '', address: '',
  price: 0, deposit: 0, area_size: 50, room_count: 1, hall_count: 1,
  toilet_count: 1, floor: 1, total_floors: 6, orientation: '',
  decoration: '', has_elevator: false, has_subway: false,
  facilities: [] as string[], pay_type: '', lease_term: '',
  summary: '', description: '',
})

const rules: FormRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  district: [{ required: true, message: '请选择区域', trigger: 'change' }],
  community: [{ required: true, message: '请选择小区名', trigger: 'change' }],
  price: [{ required: true, message: '请输入月租', trigger: 'blur' }],
  area_size: [{ required: true, message: '请输入面积', trigger: 'blur' }],
}

const currentAreas = computed(() => {
  const d = districts.value.find((d: any) => d.id === form.district)
  return d ? d.areas : []
})

function onDistrictChange() {
  form.area_ref = null
  form.community = ''
  communityOptions.value = []
}

function onAreaChange() {
  form.community = ''
  loadCommunities()
}

async function loadOptions() {
  const [catRes, distRes, oriRes, decRes, payRes, leaseRes, facRes] = await Promise.all([
    api.get('/houses/categories/'),
    api.get('/houses/districts/'),
    api.get('/houses/dicts/', { params: { group: 'orientation' } }),
    api.get('/houses/dicts/', { params: { group: 'decoration' } }),
    api.get('/houses/dicts/', { params: { group: 'pay_type' } }),
    api.get('/houses/dicts/', { params: { group: 'lease_term' } }),
    api.get('/houses/dicts/', { params: { group: 'facility' } }),
  ])
  categories.value = catRes.data
  districts.value = distRes.data
  orientations.value = oriRes.data.map((d: any) => d.value)
  decorations.value = decRes.data.map((d: any) => d.value)
  payTypes.value = payRes.data.map((d: any) => d.value)
  leaseTerms.value = leaseRes.data.map((d: any) => d.value)
  facilityOptions.value = facRes.data.map((d: any) => d.value)
}

async function loadCommunities() {
  if (!form.area_ref) { communityOptions.value = []; return }
  const res = await api.get('/houses/dicts/', { params: { group: 'community', area: form.area_ref } })
  communityOptions.value = res.data
}

async function loadHouse() {
  if (!houseId.value) return
  pageLoading.value = true
  try {
    const res = await api.get(`/houses/${houseId.value}/`)
    const d = res.data
    Object.assign(form, {
      title: d.title || '', category: d.category || null,
      district: d.district || null, area_ref: d.area_ref || null,
      community: d.community || '', address: d.address || '',
      price: Number(d.price) || 0, deposit: Number(d.deposit) || 0,
      area_size: d.area_size || 50, room_count: d.room_count || 1,
      hall_count: d.hall_count || 1, toilet_count: d.toilet_count || 1,
      floor: d.floor || 1, total_floors: d.total_floors || 6,
      orientation: d.orientation || '', decoration: d.decoration || '',
      has_elevator: d.has_elevator || false, has_subway: d.has_subway || false,
      facilities: d.facilities || [], pay_type: d.pay_type || '',
      lease_term: d.lease_term || '', summary: d.summary || '',
      description: d.description || '',
    })
    existingImages.value = d.images || []
    // 加载小区名字典
    if (d.area_ref) await loadCommunities()
  } finally { pageLoading.value = false }
}

function onFileChange(file: UploadFile) {
  newImageFiles.value.push(file)
}
function onFileRemove(file: UploadFile) {
  newImageFiles.value = newImageFiles.value.filter(f => f.uid !== file.uid)
}

async function removeExistingImage(img: any) {
  await ElMessageBox.confirm('确定删除这张图片？', '提示', { type: 'warning' })
  await api.delete(`/houses/images/${img.id}/delete/`)
  existingImages.value = existingImages.value.filter(i => i.id !== img.id)
  ElMessage.success('已删除')
}

async function handleSave() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  saving.value = true
  try {
    let savedHouseId = houseId.value
    if (isEdit.value) {
      await api.put(`/houses/${houseId.value}/update/`, form)
      ElMessage.success('保存成功')
    } else {
      const res = await api.post('/houses/create/', form)
      savedHouseId = res.data.id
      ElMessage.success('发布成功')
    }
    // 上传新图片
    if (newImageFiles.value.length && savedHouseId) {
      const fd = new FormData()
      newImageFiles.value.forEach(f => { if (f.raw) fd.append('images', f.raw) })
      await api.post(`/houses/${savedHouseId}/images/upload/`, fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    }
    router.push('/owner/houses')
  } finally { saving.value = false }
}

onMounted(async () => {
  await loadOptions()
  if (isEdit.value) await loadHouse()
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.card-header h2 { margin: 0; font-size: 18px; }
.section-title { font-size: 15px; color: #333; border-bottom: 1px solid #eee; padding-bottom: 8px; margin: 20px 0 12px; }
.image-list { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 12px; }
.image-item { position: relative; }
.del-btn { position: absolute; top: -8px; right: -8px; }
</style>
