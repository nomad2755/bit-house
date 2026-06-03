# 🏠 Bit House - 比特房屋租房平台

一个全功能房屋租赁平台，支持管理员、房东、租客三种角色。

## ✨ 功能特性

### 前台（租客/房东）
- 🔍 多维度房源搜索（省→市→区→商圈级联筛选）
- 🏘️ 房源详情浏览（图片、户型、朝向、装修、配套设施）
- ❤️ 收藏房源
- 📋 合同管理（签约、缴纳租金、退房）
- 👤 个人中心（昵称、手机号、身份证号管理）

### 房东后台
- 📝 房源发布与编辑（独立页面，支持图片上传）
- 📊 房源状态管理（上架/下架/已租出）
- 🔑 支持用户名/手机号/身份证号登录

### 管理员后台
- 📊 数据仪表盘
- 🏠 房源管理
- 📋 合同管理
- 👥 用户管理
- 📢 公告管理
- 📂 分类管理
- 📖 字典管理（朝向/装修/付款方式/租期/配套设施/小区名）

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 5 + Django REST Framework + SimpleJWT |
| 前端 | Vue 3 + Vite + Element Plus + Pinia + Vue Router |
| 数据库 | SQLite（开发） |
| 认证 | JWT（支持用户名/手机号/身份证号登录） |

## 📁 项目结构

```
bit-house/
├── backend/                    # Django 后端
│   ├── bithouse/              # 项目配置
│   ├── apps/
│   │   ├── users/             # 用户模块
│   │   ├── houses/            # 房源模块（含字典、省市区）
│   │   ├── orders/            # 合同/订单
│   │   ├── notices/           # 公告
│   │   └── finance/           # 财务
│   └── manage.py
└── frontend/                   # Vue 3 前端
    └── src/
        ├── api/               # axios 拦截器
        ├── stores/            # Pinia 状态管理
        ├── layouts/           # 布局组件
        └── views/             # 页面
```

## 🚀 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+

### 后端启动
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed          # 初始化种子数据
python manage.py runserver     # http://localhost:8000
```

### 前端启动
```bash
cd frontend
npm install
npm run dev                    # http://localhost:3000
```

## 🔑 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 房东 | owner1 | 123456 |
| 房东 | owner2 | 123456 |
| 租客 | tenant1 | 123456 |
| 租客 | tenant2 | 123456 |

## 📡 API 端点

```
POST /api/auth/login/              # 登录
POST /api/auth/register/           # 注册
GET  /api/houses/                  # 房源列表
GET  /api/houses/{id}/             # 房源详情
POST /api/houses/create/           # 发布房源
GET  /api/houses/dicts/?group=xxx  # 字典查询
GET  /api/houses/provinces/        # 省份列表
GET  /api/houses/districts/        # 区域列表
```

## 📸 页面预览

| 页面 | 说明 |
|------|------|
| 首页 | 推荐房源、最新房源、搜索框 |
| 房源列表 | 城市→区域→商圈级联筛选、搜索、排序 |
| 房源详情 | 图片轮播、户型/朝向/装修等详细信息 |
| 房东房源管理 | 发布/编辑/上下架/删除房源 |
| 管理员后台 | 字典/分类/用户/合同/公告管理 |

## 📄 License

MIT
