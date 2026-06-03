<template>
  <div class="front-layout">
    <header class="front-header">
      <div class="header-content">
        <router-link to="/" class="logo">
          <el-icon><HomeFilled /></el-icon>
          <span>Bit House</span>
        </router-link>
        <nav class="nav-links">
          <router-link to="/">首页</router-link>
          <router-link to="/houses">房源</router-link>
          <template v-if="userStore.isLoggedIn">
            <router-link to="/contracts">我的合同</router-link>
            <router-link to="/favorites">收藏</router-link>
            <router-link v-if="userStore.isOwner || userStore.isAdmin" to="/owner/houses">我的房源</router-link>
            <router-link to="/profile">个人中心</router-link>
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                {{ userStore.username }}
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-if="userStore.isAdmin" command="admin">后台管理</el-dropdown-item>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <router-link to="/login">登录</router-link>
          </template>
        </nav>
        <!-- 位置选择器 - 最右侧 -->
        <div class="location-selector">
          <el-dropdown trigger="click" @command="handleCityCommand">
            <span class="location-btn">
              <el-icon><Location /></el-icon>
              {{ locationStore.cityName || '选择城市' }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <div class="city-panel">
                  <div v-for="p in locationStore.provinces" :key="p.id" class="province-group">
                    <span class="province-name">{{ p.name }}</span>
                    <span v-for="c in p.cities" :key="c.id"
                      class="city-item"
                      :class="{ active: locationStore.selectedCity === c.id }"
                      @click="handleCityCommand({ provinceId: p.id, cityId: c.id, name: c.name })">
                      {{ c.name }}
                    </span>
                  </div>
                </div>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>
    <main class="front-main">
      <router-view />
    </main>
    <footer class="front-footer">
      <p>&copy; 2026 Bit House - 比特房屋租房平台</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useLocationStore } from '@/stores/location'

const router = useRouter()
const userStore = useUserStore()
const locationStore = useLocationStore()

onMounted(() => { locationStore.loadProvinces() })

function handleCityCommand(data: { provinceId: number; cityId: number; name: string }) {
  locationStore.selectCity(data.provinceId, data.cityId, data.name)
}

function handleCommand(cmd: string) {
  if (cmd === 'admin') router.push('/admin')
  else if (cmd === 'logout') {
    userStore.logout()
    router.push('/')
  }
}
</script>

<style scoped>
.front-layout { min-height: 100vh; display: flex; flex-direction: column; }
.front-header { background: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 100; }
.header-content { max-width: 1200px; margin: 0 auto; padding: 0 20px; height: 60px; display: flex; align-items: center; gap: 16px; }
.logo { display: flex; align-items: center; gap: 8px; font-size: 20px; font-weight: bold; color: #409eff; text-decoration: none; }
.nav-links { display: flex; align-items: center; gap: 20px; flex: 1; }
.nav-links a { color: #333; text-decoration: none; font-size: 14px; }
.nav-links a:hover, .nav-links a.router-link-exact-active { color: #409eff; }
.user-info { cursor: pointer; display: flex; align-items: center; gap: 4px; font-size: 14px; }
.location-selector { flex-shrink: 0; margin-left: auto; }
.location-btn { display: flex; align-items: center; gap: 4px; cursor: pointer; font-size: 14px; color: #333; }
.location-btn:hover { color: #409eff; }
.front-main { flex: 1; max-width: 1200px; width: 100%; margin: 0 auto; padding: 20px; }
.front-footer { background: #f5f5f5; text-align: center; padding: 20px; color: #999; font-size: 12px; }
.city-panel { padding: 12px 16px; max-width: 400px; }
.province-group { margin-bottom: 8px; display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.province-name { font-weight: bold; color: #333; font-size: 13px; min-width: 40px; }
.city-item { cursor: pointer; font-size: 13px; color: #666; padding: 2px 8px; border-radius: 4px; }
.city-item:hover { color: #409eff; background: #ecf5ff; }
.city-item.active { color: #409eff; font-weight: bold; }
</style>
