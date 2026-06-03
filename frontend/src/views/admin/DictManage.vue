<template>
  <div>
    <h2>字典管理</h2>
    <el-tabs v-model="activeGroup" @tab-change="loadDicts">
      <el-tab-pane v-for="g in groups" :key="g.value" :label="g.label" :name="g.value" />
    </el-tabs>

    <el-button type="primary" style="margin-bottom:16px" @click="openDialog()">新增{{ currentGroupLabel }}项</el-button>

    <el-table :data="dicts" v-loading="loading" stripe>
      <el-table-column prop="label" label="显示名" />
      <el-table-column prop="value" label="值" />
      <el-table-column v-if="activeGroup==='community'" prop="area_name" label="所属商圈" />
      <el-table-column prop="sort" label="排序" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active?'success':'info'">{{ row.is_active?'启用':'禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="openDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑字典项' : '新增字典项'" width="480px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="分组">
          <el-input :model-value="currentGroupLabel" disabled />
        </el-form-item>
        <el-form-item label="显示名" required>
          <el-input v-model="form.label" placeholder="如：精装" />
        </el-form-item>
        <el-form-item label="值" required>
          <el-input v-model="form.value" placeholder="如：精装" :disabled="!!editingId" />
        </el-form-item>
        <el-form-item v-if="activeGroup==='community'" label="商圈">
          <el-select v-model="form.area" placeholder="选择商圈" style="width:100%">
            <el-option v-for="a in areas" :key="a.id" :label="`${a.district_name} - ${a.name}`" :value="a.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort" :min="0" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const groups = [
  { value: 'orientation', label: '朝向' },
  { value: 'decoration', label: '装修' },
  { value: 'pay_type', label: '付款方式' },
  { value: 'lease_term', label: '租期' },
  { value: 'facility', label: '配套设施' },
  { value: 'community', label: '小区名' },
]

const activeGroup = ref('orientation')
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const editingId = ref<number | null>(null)
const dicts = ref<any[]>([])
const areas = ref<any[]>([])

const currentGroupLabel = computed(() => groups.find(g => g.value === activeGroup.value)?.label || '')

const form = reactive({ label: '', value: '', area: null as number | null, sort: 0, is_active: true })

async function loadDicts() {
  loading.value = true
  try {
    const res = await api.get('/houses/dicts/', { params: { group: activeGroup.value } })
    dicts.value = res.data
  } finally { loading.value = false }
}

async function loadAreas() {
  const res = await api.get('/houses/districts/')
  areas.value = res.data.flatMap((d: any) => d.areas.map((a: any) => ({ ...a, district_name: d.name })))
}

function openDialog(row?: any) {
  if (row) {
    editingId.value = row.id
    Object.assign(form, { label: row.label, value: row.value, area: row.area || null, sort: row.sort, is_active: row.is_active })
  } else {
    editingId.value = null
    Object.assign(form, { label: '', value: '', area: null, sort: 0, is_active: true })
  }
  dialogVisible.value = true
}

async function handleSave() {
  if (!form.label || !form.value) return ElMessage.warning('请填写显示名和值')
  saving.value = true
  try {
    const payload: any = { group: activeGroup.value, label: form.label, value: form.value, sort: form.sort, is_active: form.is_active }
    if (activeGroup.value === 'community') payload.area = form.area
    if (editingId.value) {
      await api.put(`/houses/dicts/${editingId.value}/`, payload)
      ElMessage.success('更新成功')
    } else {
      await api.post('/houses/dicts/manage/', payload)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    loadDicts()
  } finally { saving.value = false }
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm(`确定删除「${row.label}」？`, '提示', { type: 'warning' })
  await api.delete(`/houses/dicts/${row.id}/`)
  ElMessage.success('已删除')
  loadDicts()
}

onMounted(() => {
  loadDicts()
  loadAreas()
})
</script>
