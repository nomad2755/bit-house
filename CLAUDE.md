# Bit House - 比特房屋租房平台

## 项目概述
Django + Vue 3 前后端分离的房屋租赁平台，支持管理员、房东、租客三种角色。

## 技术栈
- **后端**: Django 5.x + Django REST Framework + SimpleJWT + SQLite
- **前端**: Vue 3 + Vite + Element Plus + Pinia + Vue Router
- **端口**: 后端 8000, 前端 3000 (Vite proxy → 8000)
- **仓库**: https://github.com/nomad2755/bit-house

## 目录结构
```
bit-house/
├── backend/
│   ├── bithouse/           # Django 项目配置
│   │   ├── settings.py     # AUTH_USER_MODEL='users.User', JWT, CORS
│   │   ├── urls.py         # api/auth, api/houses, api/orders, api/notices, api/finance
│   │   └── exceptions.py   # 自定义异常处理
│   ├── apps/
│   │   ├── users/          # 用户模块 (自定义User模型, 手机号/身份证号/用户名登录)
│   │   ├── houses/         # 房源模块 (House, District, Area, Dictionary, Province, City)
│   │   ├── orders/         # 合同/订单/看房请求
│   │   ├── notices/        # 公告
│   │   └── finance/        # 财务
│   ├── db.sqlite3
│   └── manage.py
└── frontend/
    └── src/
        ├── api/index.ts    # axios 实例, 请求/响应拦截器, JWT 自动刷新
        ├── stores/
        │   ├── user.ts     # 用户状态 (登录/注册/个人信息)
        │   └── location.ts # 城市选择 (持久化到 localStorage)
        ├── layouts/
        │   ├── FrontLayout.vue  # 前台头部 (导航+城市选择器)
        │   └── AdminLayout.vue  # 后台侧边栏
        ├── views/
        │   ├── front/      # Home, HouseList, HouseDetail, Login, Register, Profile, Favorites, Contracts
        │   ├── admin/      # Dashboard, HouseManage, ContractManage, UserManage, NoticeManage, CategoryManage, DictManage
        │   └── owner/      # OwnerHouseManage, OwnerHouseEdit (独立页面+图片上传)
        └── router/index.ts # 路由守卫 (requiresAuth, requiresAdmin, requiresOwner)
```

## 启动命令
```bash
# 后端
cd backend && python manage.py runserver 0.0.0.0:8000

# 前端
cd frontend && npx vite --port 3000

# 初始化种子数据 (seed.py 本地维护，不推送到远端)
cd backend && python manage.py seed
```

## 测试账号
| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 房东1 | owner1 | 123456 |
| 房东2 | owner2 | 123456 |
| 租客1 | tenant1 | 123456 |
| 租客2 | tenant2 | 123456 |

## 核心数据模型
- **User**: 自定义用户, 字段含 role/phone/id_card/display_name, phone 字段 unique=True
- **House**: 房源, 关联 owner/category/district/area_ref, 字典字段: orientation/decoration/pay_type/lease_term/facilities/community
- **Province → City → District → Area**: 四级地理层级
- **Dictionary**: 平台字典, group 分组 (orientation/decoration/pay_type/lease_term/facility/community)
- **Contract**: 合同, 关联 house/landlord/tenant
- **RentPayment**: 租金账单

## API 端点速查
```
# 认证
POST /api/auth/login/          # 登录 (用户名/手机号/身份证号)
POST /api/auth/register/       # 注册 (唯一性校验: 用户名/手机号/身份证号)
POST /api/auth/refresh/        # 刷新 token
GET/PUT /api/auth/profile/     # 个人信息

# 房源
GET  /api/houses/              # 房源列表 (支持 search/district/district__in/community/category/price 等筛选)
GET  /api/houses/{id}/         # 房源详情 (含 owner_phone, 登录可见)
POST /api/houses/create/       # 发布房源 (房东)
PUT/PATCH /api/houses/{id}/update/  # 编辑房源 (房东/管理员)
DELETE /api/houses/{id}/delete/ # 删除房源
GET  /api/houses/my/           # 房东自己的房源
POST /api/houses/{id}/images/upload/  # 上传图片
DELETE /api/houses/images/{id}/delete/ # 删除图片

# 字典
GET  /api/houses/dicts/?group=xxx                # 按分组查询字典
GET  /api/houses/dicts/?group=community&area=xx   # 按商圈查小区名
POST /api/houses/dicts/manage/                    # 新增字典项 (管理员)
PUT/DELETE /api/houses/dicts/{id}/                # 编辑/删除字典项

# 地理
GET /api/houses/provinces/     # 省份列表 (含城市)
GET /api/houses/districts/     # 区域列表 (含商圈)
GET /api/houses/categories/    # 房屋分类

# 其他
GET/POST /api/houses/favorites/    # 收藏
GET /api/houses/recommended/       # 推荐房源
GET /api/houses/latest/            # 最新房源
```

## 关键设计决策

### 登录认证
- 请求拦截器对 `/auth/login/`、`/auth/register/`、`/auth/refresh/` 不附加 Bearer token (避免失效 token 导致 401)
- AUTH_URLS 使用相对路径 (不含 `/api` 前缀，因 baseURL 已设置为 `/api`)
- 响应拦截器对登录 401 统一显示 "用户名或密码错误" (不暴露后端技术信息)
- 手机号/身份证号查找使用 `filter().first()` 而非 `get()` (防多条记录报 500)

### 字典系统
- Dictionary 模型统一管理所有下拉选项 (朝向/装修/付款/租期/配套设施/小区名)
- 小区名关联 Area (商圈)，支持按商圈筛选
- 管理员通过 `/admin/dicts` 页面配置，前端表单/筛选动态加载
- 小区数据从 58.com 抓取，通过小区详情页的 `regionName` 字段关联商圈 (189 个小区，35 个商圈)

### 城市选择
- location store 持久化到 localStorage，全局共享
- 首部城市选择器切换后，房源列表自动刷新
- HouseList 首次进入需选择城市才加载数据
- `district__in` 过滤器支持传入多个区域 ID

### 房源列表筛选
- 级联筛选: 城市 → 区域 → 商圈 → 小区 (字典数据)
- 搜索框支持标题/小区名/地址/描述搜索 (从首页跳转自动回填)
- 未选城市时显示引导提示，不加载数据

### 房东房源管理
- 独立编辑页面 (`/owner/houses/:id/edit`)，非弹窗
- 支持图片上传/删除 (后端 API: `/houses/{id}/images/upload/`, `/houses/images/{id}/delete/`)
- 小区名级联选择: 区域 → 商圈 → 小区名 (字典)
- 上下架使用 PATCH 部分更新

### 房源详情页
- 房东手机号仅登录用户可见 (未登录显示"登录后查看联系方式")
- 登录页左上角有"返回首页"按钮

## Git 提交规范
- `seed.py` 在 `.gitignore` 中，不推送到远端
- 提交前需用户确认，不擅自推送
