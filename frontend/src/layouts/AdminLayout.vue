<template>
  <div class="admin-layout">
    <aside class="admin-sidebar">
      <div class="sidebar-logo">
        <el-icon><HomeFilled /></el-icon>
        <span>Bit House 管理</span>
      </div>
      <el-menu :default-active="route.path" router>
        <el-menu-item index="/admin">
          <el-icon><DataAnalysis /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/admin/houses">
          <el-icon><House /></el-icon>
          <span>房源管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/contracts">
          <el-icon><Document /></el-icon>
          <span>合同管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/notices">
          <el-icon><Bell /></el-icon>
          <span>公告管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/categories">
          <el-icon><Grid /></el-icon>
          <span>分类管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/dicts">
          <el-icon><Setting /></el-icon>
          <span>字典管理</span>
        </el-menu-item>
      </el-menu>
    </aside>
    <div class="admin-main">
      <header class="admin-header">
        <span>{{ userStore.username }} (管理员)</span>
        <el-button type="primary" link @click="goFront">前台首页</el-button>
        <el-button type="danger" link @click="handleLogout">退出</el-button>
      </header>
      <div class="admin-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

function goFront() { router.push('/') }
function handleLogout() { userStore.logout(); router.push('/') }
</script>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; }
.admin-sidebar { width: 220px; background: #304156; color: #fff; }
.sidebar-logo { height: 60px; display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 16px; font-weight: bold; }
.admin-main { flex: 1; display: flex; flex-direction: column; }
.admin-header { height: 60px; background: #fff; box-shadow: 0 1px 4px rgba(0,0,0,0.1); display: flex; align-items: center; justify-content: flex-end; gap: 16px; padding: 0 20px; }
.admin-content { flex: 1; padding: 20px; background: #f0f2f5; }
</style>
