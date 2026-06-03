"""
种子数据脚本 - 武汉区域/商圈 + 测试用户 + 示例房源
运行: python manage.py seed
"""
from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.houses.models import District, Area, HouseCategory, House, HouseImage, Dictionary, Province, City


class Command(BaseCommand):
    help = '初始化种子数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化种子数据...')

        # ========== 用户 ==========
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'display_name': '系统管理员', 'role': 'admin', 'phone': '13800000001', 'is_staff': True, 'is_superuser': True}
        )
        admin.set_password('admin123')
        admin.save()

        owner1, _ = User.objects.get_or_create(
            username='owner1',
            defaults={'display_name': '张房东', 'role': 'owner', 'phone': '13800000002'}
        )
        owner1.set_password('123456')
        owner1.save()

        owner2, _ = User.objects.get_or_create(
            username='owner2',
            defaults={'display_name': '王房东', 'role': 'owner', 'phone': '13800000005'}
        )
        owner2.set_password('123456')
        owner2.save()

        tenant1, _ = User.objects.get_or_create(
            username='tenant1',
            defaults={'display_name': '李租客', 'role': 'tenant', 'phone': '13800000003'}
        )
        tenant1.set_password('123456')
        tenant1.save()

        tenant2, _ = User.objects.get_or_create(
            username='tenant2',
            defaults={'display_name': '赵租客', 'role': 'tenant', 'phone': '13800000004'}
        )
        tenant2.set_password('123456')
        tenant2.save()

        self.stdout.write(self.style.SUCCESS('[OK] 用户创建完成'))

        # ========== 省份/城市 ==========
        province, _ = Province.objects.get_or_create(name='湖北', defaults={'sort': 1})
        city, _ = City.objects.get_or_create(name='武汉', province=province, defaults={'sort': 1})

        # ========== 区域 + 商圈 ==========
        districts_data = {
            '江岸': ['后湖', '百步亭', '二七', '台北', '花桥', '球场'],
            '江汉': ['唐家墩', '万松园', '常青', '王家墩', '西北湖'],
            '硚口': ['古田', '宗关', '汉正街', '宝丰'],
            '武昌': ['首义', '中南路', '水果湖', '徐东', '南湖', '白沙洲'],
            '洪山': ['文化大道', '光谷', '关山', '鲁巷', '街道口'],
            '汉阳': ['钟家村', '王家湾', '四新', '鹦鹉洲'],
            '东湖高新': ['佛祖岭', '光谷东', '花山', '左岭'],
            '青山': ['红钢城', '和平大道', '建设路'],
            '东西湖': ['金银湖', '吴家山', '常青花园'],
            '江夏': ['纸坊', '庙山', '藏龙岛'],
            '蔡甸': ['蔡甸城区', '后官湖', '中法生态城'],
            '黄陂': ['盘龙城', '前川', '滠口'],
            '新洲': ['阳逻', '邾城'],
            '沌口': ['体育中心', '神龙大道'],
            '汉南': ['纱帽'],
        }

        sort = 0
        for dist_name, area_names in districts_data.items():
            sort += 1
            district, _ = District.objects.update_or_create(
                name=dist_name, defaults={'sort': sort, 'city': city}
            )
            for i, area_name in enumerate(area_names):
                Area.objects.get_or_create(
                    name=area_name, district=district,
                    defaults={'sort': i + 1}
                )

        self.stdout.write(self.style.SUCCESS('[OK] 区域/商圈创建完成'))

        # ========== 房屋分类 ==========
        categories = [('整租', 1, '整套出租'), ('合租', 2, '单间出租'), ('独栋', 3, '公寓/独栋')]
        for name, sort, desc in categories:
            HouseCategory.objects.get_or_create(name=name, defaults={'sort': sort, 'description': desc})

        self.stdout.write(self.style.SUCCESS('[OK] 房屋分类创建完成'))

        # ========== 示例房源 ==========
        cat_whole = HouseCategory.objects.get(name='整租')
        cat_share = HouseCategory.objects.get(name='合租')
        cat_alone = HouseCategory.objects.get(name='独栋')

        dist_hg = District.objects.get(name='洪山')
        dist_jh = District.objects.get(name='江汉')
        dist_wh = District.objects.get(name='武昌')
        dist_dh = District.objects.get(name='东湖高新')

        area_culture = Area.objects.get(name='文化大道', district=dist_hg)
        area_tang = Area.objects.get(name='唐家墩', district=dist_jh)
        area_shouyi = Area.objects.get(name='首义', district=dist_wh)
        area_fozu = Area.objects.get(name='佛祖岭', district=dist_dh)

        houses_data = [
            {
                'owner': owner1, 'title': '整租·世茂林屿岸 3室2厅 南',
                'description': '精装三房，南北通透，采光好，小区环境优美，周边配套齐全。',
                'summary': '精装三房 南北通透 近地铁',
                'category': cat_whole, 'district': dist_hg, 'area_ref': area_culture,
                'community': '世茂林屿岸', 'address': '文化大道588号',
                'price': 2000, 'deposit': 2000, 'area_size': 90.8,
                'room_count': 3, 'hall_count': 2, 'toilet_count': 1,
                'floor': 15, 'total_floors': 49, 'orientation': '南',
                'decoration': '精装', 'has_elevator': True, 'has_subway': True,
                'facilities': ['空调', '冰箱', '洗衣机', 'WiFi', '热水器', '燃气灶'],
                'pay_type': '押一付三', 'lease_term': '年租',
                'is_recommended': True, 'is_new': True, 'status': 0,
            },
            {
                'owner': owner1, 'title': '整租·顶琇国际城 2室1厅 南',
                'description': '两室一厅，精装修，拎包入住，交通便利。',
                'summary': '精装修 拎包入住 交通便利',
                'category': cat_whole, 'district': dist_jh, 'area_ref': area_tang,
                'community': '顶琇国际城', 'address': '唐家墩路18号',
                'price': 2300, 'deposit': 2300, 'area_size': 82.0,
                'room_count': 2, 'hall_count': 1, 'toilet_count': 1,
                'floor': 30, 'total_floors': 48, 'orientation': '南',
                'decoration': '精装', 'has_elevator': True, 'has_subway': True,
                'facilities': ['空调', '冰箱', '洗衣机', 'WiFi', '热水器'],
                'pay_type': '押一付三', 'lease_term': '年租',
                'is_recommended': True, 'status': 0,
            },
            {
                'owner': owner2, 'title': '整租·长城达尚城 3室2厅 西南',
                'description': '三室两厅两卫，西南朝向，采光充足，小区安静。',
                'summary': '三房两卫 采光好 安静小区',
                'category': cat_whole, 'district': dist_dh, 'area_ref': area_fozu,
                'community': '长城达尚城', 'address': '佛祖岭路99号',
                'price': 2500, 'deposit': 2500, 'area_size': 105.71,
                'room_count': 3, 'hall_count': 2, 'toilet_count': 2,
                'floor': 18, 'total_floors': 27, 'orientation': '西南',
                'decoration': '精装', 'has_elevator': True, 'has_subway': False,
                'facilities': ['空调', '冰箱', '洗衣机', '燃气灶', '热水器'],
                'pay_type': '押一付一', 'lease_term': '年租',
                'is_recommended': True, 'status': 0,
            },
            {
                'owner': owner2, 'title': '合租·南湖雅园 单间 南',
                'description': '南湖雅园单间出租，靠近街道口商圈，生活便利。',
                'summary': '单间出租 近街道口',
                'category': cat_share, 'district': dist_wh, 'area_ref': area_shouyi,
                'community': '南湖雅园', 'address': '南湖大道128号',
                'price': 1200, 'deposit': 1200, 'area_size': 18.5,
                'room_count': 1, 'hall_count': 0, 'toilet_count': 1,
                'floor': 6, 'total_floors': 11, 'orientation': '南',
                'decoration': '简装', 'has_elevator': True, 'has_subway': False,
                'facilities': ['空调', 'WiFi', '洗衣机'],
                'pay_type': '押一付一', 'lease_term': '月租',
                'is_new': True, 'status': 0,
            },
            {
                'owner': owner1, 'title': '整租·御庭园 3室1厅 东南',
                'description': '循礼门商圈，东南朝向三居室，交通便利。',
                'summary': '循礼门商圈 交通便利',
                'category': cat_whole, 'district': dist_jh, 'area_ref': area_tang,
                'community': '御庭园', 'address': '循礼门路66号',
                'price': 3200, 'deposit': 3200, 'area_size': 121.81,
                'room_count': 3, 'hall_count': 1, 'toilet_count': 1,
                'floor': 12, 'total_floors': 26, 'orientation': '东南',
                'decoration': '豪装', 'has_elevator': True, 'has_subway': True,
                'facilities': ['空调', '冰箱', '洗衣机', 'WiFi', '热水器', '燃气灶', '微波炉'],
                'pay_type': '押一付三', 'lease_term': '年租',
                'status': 0,
            },
            {
                'owner': owner2, 'title': '独栋·冠寓光谷店 开间',
                'description': '品牌公寓，拎包入住，24小时安保，免费健身房。',
                'summary': '品牌公寓 拎包入住 免费健身',
                'category': cat_alone, 'district': dist_dh, 'area_ref': area_fozu,
                'community': '冠寓光谷店', 'address': '光谷大道200号',
                'price': 1800, 'deposit': 1800, 'area_size': 35.0,
                'room_count': 1, 'hall_count': 0, 'toilet_count': 1,
                'floor': 8, 'total_floors': 15, 'orientation': '南',
                'decoration': '精装', 'has_elevator': True, 'has_subway': True,
                'facilities': ['空调', 'WiFi', '洗衣机', '热水器', '独立卫浴'],
                'pay_type': '押一付一', 'lease_term': '月租',
                'is_new': True, 'status': 0,
            },
        ]

        for data in houses_data:
            house, created = House.objects.get_or_create(
                title=data['title'], defaults=data
            )
            if created:
                self.stdout.write(f'  + {house.title}')

        self.stdout.write(self.style.SUCCESS('[OK] 示例房源创建完成'))

        # ========== 字典数据 ==========
        dict_data = {
            'orientation': [
                ('南', '南'), ('北', '北'), ('东', '东'), ('西', '西'),
                ('南北', '南北'), ('东南', '东南'), ('西南', '西南'), ('东北', '东北'),
            ],
            'decoration': [
                ('毛坯', '毛坯'), ('简装', '简装'), ('精装', '精装'), ('豪装', '豪装'),
            ],
            'pay_type': [
                ('押一付一', '押一付一'), ('押一付三', '押一付三'), ('押二付一', '押二付一'),
                ('半年付', '半年付'), ('年付', '年付'),
            ],
            'lease_term': [
                ('月租', '月租'), ('季租', '季租'), ('半年租', '半年租'), ('年租', '年租'),
            ],
            'facility': [
                ('空调', '空调'), ('冰箱', '冰箱'), ('洗衣机', '洗衣机'), ('WiFi', 'WiFi'),
                ('热水器', '热水器'), ('天然气', '天然气'), ('衣柜', '衣柜'), ('床', '床'),
                ('沙发', '沙发'), ('电视', '电视'), ('微波炉', '微波炉'), ('抽油烟机', '抽油烟机'),
                ('独立卫浴', '独立卫浴'), ('燃气灶', '燃气灶'),
            ],
        }

        sort = 0
        for group, items in dict_data.items():
            for i, (label, value) in enumerate(items):
                Dictionary.objects.get_or_create(
                    group=group, value=value,
                    defaults={'label': label, 'sort': i + 1}
                )

        # 小区名字典（按商圈关联）
        communities_data = {
            '文化大道': ['世茂林屿岸', '锦绣龙城', '保利时代', '万科城市花园'],
            '唐家墩': ['顶琇国际城', '御庭园', '华南国际广场', '新华家园'],
            '首义': ['南湖雅园', '首义小区', '紫阳金利屋'],
            '佛祖岭': ['长城达尚城', '冠寓光谷店', '佛祖岭社区', '光谷理想城'],
        }
        for area_name, communities in communities_data.items():
            try:
                area = Area.objects.get(name=area_name)
                for i, comm in enumerate(communities):
                    Dictionary.objects.get_or_create(
                        group='community', value=comm,
                        defaults={'label': comm, 'area': area, 'sort': i + 1}
                    )
            except Area.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS('[OK] 字典数据创建完成'))
        self.stdout.write(self.style.SUCCESS('种子数据初始化完成！'))
        self.stdout.write('')
        self.stdout.write('测试账号:')
        self.stdout.write('  管理员: admin / admin123')
        self.stdout.write('  房东1:  owner1 / 123456')
        self.stdout.write('  房东2:  owner2 / 123456')
        self.stdout.write('  租客1:  tenant1 / 123456')
        self.stdout.write('  租客2:  tenant2 / 123456')
