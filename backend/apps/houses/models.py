from django.db import models


class Province(models.Model):
    """省份"""
    name = models.CharField('省份', max_length=20, unique=True)
    sort = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'province'
        verbose_name = '省份'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.name


class City(models.Model):
    """城市"""
    name = models.CharField('城市', max_length=20)
    province = models.ForeignKey(Province, on_delete=models.CASCADE,
                                 related_name='cities', verbose_name='所属省份')
    sort = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'city'
        verbose_name = '城市'
        verbose_name_plural = verbose_name
        ordering = ['sort']
        unique_together = ('province', 'name')

    def __str__(self):
        return f'{self.province.name} - {self.name}'


class District(models.Model):
    """区域"""
    name = models.CharField('区域名称', max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE,
                             related_name='districts', verbose_name='所属城市',
                             null=True, blank=True)
    sort = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'district'
        verbose_name = '区域'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.name


class Area(models.Model):
    """商圈"""
    name = models.CharField('商圈名称', max_length=30)
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                  related_name='areas', verbose_name='所属区域')
    sort = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'area'
        verbose_name = '商圈'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return f'{self.district.name} - {self.name}'


class HouseCategory(models.Model):
    """房屋分类"""
    name = models.CharField('分类名称', max_length=20, unique=True)
    sort = models.IntegerField('排序', default=0)
    description = models.TextField('描述', blank=True, default='')

    class Meta:
        db_table = 'house_category'
        verbose_name = '房屋分类'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.name


class House(models.Model):
    """房源"""
    STATUS_CHOICES = [
        (0, '出租中'),
        (1, '已租出'),
        (2, '已下架'),
    ]

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE,
                               related_name='houses', verbose_name='房东')
    title = models.CharField('标题', max_length=100)
    description = models.TextField('详细描述', blank=True, default='')
    summary = models.CharField('摘要', max_length=200, blank=True, default='')
    category = models.ForeignKey(HouseCategory, on_delete=models.SET_NULL,
                                  null=True, related_name='houses', verbose_name='分类')
    district = models.ForeignKey(District, on_delete=models.SET_NULL,
                                  null=True, related_name='houses', verbose_name='区域')
    area_ref = models.ForeignKey(Area, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='houses', verbose_name='商圈')
    community = models.CharField('小区名', max_length=50, blank=True, default='')
    address = models.CharField('详细地址', max_length=200, blank=True, default='')
    price = models.DecimalField('月租金(元)', max_digits=10, decimal_places=2)
    deposit = models.DecimalField('押金(元)', max_digits=10, decimal_places=2, default=0)
    area_size = models.FloatField('面积(㎡)')
    room_count = models.IntegerField('卧室数', default=1)
    hall_count = models.IntegerField('客厅数', default=1)
    toilet_count = models.IntegerField('卫生间数', default=1)
    layout_desc = models.CharField('户型描述', max_length=20, blank=True, default='')
    floor = models.IntegerField('当前楼层', default=1)
    total_floors = models.IntegerField('总楼层', default=1)
    floor_level = models.CharField('楼层等级', max_length=5, blank=True, default='',
                                    help_text='低楼层/中楼层/高楼层')
    orientation = models.CharField('朝向', max_length=10, blank=True, default='',
                                    help_text='南/北/东/西/南北/东南/西南')
    decoration = models.CharField('装修', max_length=10, blank=True, default='',
                                   help_text='毛坯/简装/精装/豪装')
    has_elevator = models.BooleanField('有电梯', default=False)
    has_subway = models.BooleanField('近地铁', default=False)
    facilities = models.JSONField('配套设施', default=list, blank=True,
                                   help_text='["空调","冰箱","洗衣机","WiFi"]')
    pay_type = models.CharField('付款方式', max_length=10, blank=True, default='',
                                 help_text='押一付一/押一付三')
    lease_term = models.CharField('租期', max_length=20, blank=True, default='',
                                   help_text='月租/年租/1-3个月')
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=0)
    is_recommended = models.BooleanField('推荐', default=False)
    is_sticky = models.BooleanField('置顶', default=False)
    is_new = models.BooleanField('新上', default=False)
    is_vr = models.BooleanField('VR房源', default=False)
    view_count = models.IntegerField('浏览量', default=0)
    favorite_count = models.IntegerField('收藏数', default=0)
    created_at = models.DateTimeField('发布时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'house'
        verbose_name = '房源'
        verbose_name_plural = verbose_name
        ordering = ['-is_sticky', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.layout_desc:
            self.layout_desc = f'{self.room_count}室{self.hall_count}厅{self.toilet_count}卫'
        if not self.floor_level and self.total_floors > 0:
            ratio = self.floor / self.total_floors
            if ratio <= 0.33:
                self.floor_level = '低楼层'
            elif ratio <= 0.66:
                self.floor_level = '中楼层'
            else:
                self.floor_level = '高楼层'
        super().save(*args, **kwargs)


class HouseImage(models.Model):
    """房源图片"""
    house = models.ForeignKey(House, on_delete=models.CASCADE,
                               related_name='images', verbose_name='房源')
    image = models.ImageField('图片', upload_to='houses/')
    sort = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'house_image'
        verbose_name = '房源图片'
        verbose_name_plural = verbose_name
        ordering = ['sort']


class Favorite(models.Model):
    """收藏"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                              related_name='favorites', verbose_name='用户')
    house = models.ForeignKey(House, on_delete=models.CASCADE,
                               related_name='favorites', verbose_name='房源')
    created_at = models.DateTimeField('收藏时间', auto_now_add=True)

    class Meta:
        db_table = 'favorite'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'house')
        ordering = ['-created_at']


class Dictionary(models.Model):
    """平台字典（统一管理下拉选项）"""
    GROUP_CHOICES = [
        ('orientation', '朝向'),
        ('decoration', '装修'),
        ('pay_type', '付款方式'),
        ('lease_term', '租期'),
        ('facility', '配套设施'),
        ('community', '小区名'),
    ]

    group = models.CharField('分组', max_length=20, choices=GROUP_CHOICES, db_index=True)
    label = models.CharField('显示名', max_length=50)
    value = models.CharField('值', max_length=50)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='communities', verbose_name='所属商圈',
                             help_text='仅小区名分组需要关联商圈')
    sort = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('启用', default=True)

    class Meta:
        db_table = 'dictionary'
        verbose_name = '字典'
        verbose_name_plural = verbose_name
        ordering = ['group', 'sort']
        unique_together = ('group', 'value')

    def __str__(self):
        return f'[{self.get_group_display()}] {self.label}'
