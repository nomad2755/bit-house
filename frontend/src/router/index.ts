import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // 前台页面
  {
    path: '/',
    component: () => import('@/layouts/FrontLayout.vue'),
    children: [
      { path: '', name: 'Home', component: () => import('@/views/front/Home.vue') },
      { path: 'houses', name: 'HouseList', component: () => import('@/views/front/HouseList.vue') },
      { path: 'houses/:id', name: 'HouseDetail', component: () => import('@/views/front/HouseDetail.vue') },
      { path: 'profile', name: 'Profile', component: () => import('@/views/front/Profile.vue'), meta: { requiresAuth: true } },
      { path: 'favorites', name: 'Favorites', component: () => import('@/views/front/Favorites.vue'), meta: { requiresAuth: true } },
      { path: 'contracts', name: 'Contracts', component: () => import('@/views/front/Contracts.vue'), meta: { requiresAuth: true } },
      { path: 'contracts/:id', name: 'ContractDetail', component: () => import('@/views/front/ContractDetail.vue'), meta: { requiresAuth: true } },
      // 房东专属
      { path: 'owner/houses', name: 'OwnerHouses', component: () => import('@/views/owner/OwnerHouseManage.vue'), meta: { requiresAuth: true, requiresOwner: true } },
      { path: 'owner/houses/create', name: 'OwnerHouseCreate', component: () => import('@/views/owner/OwnerHouseEdit.vue'), meta: { requiresAuth: true, requiresOwner: true } },
      { path: 'owner/houses/:id/edit', name: 'OwnerHouseEdit', component: () => import('@/views/owner/OwnerHouseEdit.vue'), meta: { requiresAuth: true, requiresOwner: true } },
    ],
  },
  { path: '/login', name: 'Login', component: () => import('@/views/front/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('@/views/front/Register.vue') },

  // 后台管理
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: '', name: 'Dashboard', component: () => import('@/views/admin/Dashboard.vue') },
      { path: 'houses', name: 'AdminHouses', component: () => import('@/views/admin/HouseManage.vue') },
      { path: 'contracts', name: 'AdminContracts', component: () => import('@/views/admin/ContractManage.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('@/views/admin/UserManage.vue') },
      { path: 'notices', name: 'AdminNotices', component: () => import('@/views/admin/NoticeManage.vue') },
      { path: 'categories', name: 'AdminCategories', component: () => import('@/views/admin/CategoryManage.vue') },
      { path: 'dicts', name: 'AdminDicts', component: () => import('@/views/admin/DictManage.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('access_token')
  const role = localStorage.getItem('role')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresAdmin && role !== 'admin') {
    next('/')
  } else if (to.meta.requiresOwner && role !== 'owner' && role !== 'admin') {
    next('/')
  } else {
    next()
  }
})

export default router
