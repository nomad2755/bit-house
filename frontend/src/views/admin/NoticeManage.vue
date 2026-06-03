<template>
  <div>
    <h2>公告管理</h2>
    <el-button type="primary" style="margin-bottom:16px" @click="showDialog()">发布公告</el-button>
    <el-table :data="notices" stripe v-loading="loading">
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="is_published" label="状态" width="80">
        <template #default="{ row }"><el-tag :type="row.is_published?'success':'info'">{{ row.is_published?'已发布':'草稿' }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160" />
    </el-table>

    <el-dialog v-model="dialogVisible" title="发布公告" width="500">
      <el-form :model="form" label-width="60px">
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="摘要"><el-input v-model="form.summary" /></el-form-item>
        <el-form-item label="内容"><el-input v-model="form.content" type="textarea" :rows="6" /></el-form-item>
        <el-form-item label="发布"><el-switch v-model="form.is_published" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

const loading = ref(false)
const notices = ref<any[]>([])
const dialogVisible = ref(false)
const form = reactive({ title: '', summary: '', content: '', is_published: false })

function showDialog() { Object.assign(form, { title: '', summary: '', content: '', is_published: false }); dialogVisible.value = true }

async function handleSave() {
  await api.post('/notices/create/', form)
  ElMessage.success('公告已发布')
  dialogVisible.value = false
  fetchNotices()
}

async function fetchNotices() {
  loading.value = true
  try { const res = await api.get('/notices/'); notices.value = res.data.results || res.data }
  finally { loading.value = false }
}

onMounted(fetchNotices)
</script>
