from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, NumberFilter, CharFilter, BooleanFilter
from django.db import models
from .models import House, HouseImage, HouseCategory, District, Area, Favorite, Dictionary, Province, City
from .serializers import (
    HouseListSerializer, HouseDetailSerializer, HouseCreateUpdateSerializer,
    HouseCategorySerializer, DistrictSerializer, DistrictWithAreasSerializer,
    AreaSerializer, HouseImageSerializer, FavoriteSerializer, DictionarySerializer,
    ProvinceWithCitiesSerializer,
)


class HouseFilter(FilterSet):
    """房源筛选"""
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')
    min_area = NumberFilter(field_name='area_size', lookup_expr='gte')
    max_area = NumberFilter(field_name='area_size', lookup_expr='lte')
    room_count = NumberFilter(field_name='room_count')
    orientation = CharFilter(field_name='orientation')
    floor_level = CharFilter(field_name='floor_level')
    has_elevator = BooleanFilter(field_name='has_elevator')
    has_subway = BooleanFilter(field_name='has_subway')
    decoration = CharFilter(field_name='decoration')
    pay_type = CharFilter(field_name='pay_type')
    lease_term = CharFilter(field_name='lease_term')
    district = NumberFilter(field_name='district_id')
    district__in = CharFilter(method='filter_district_in')
    area = NumberFilter(field_name='area_ref_id')
    community = CharFilter(field_name='community')
    category = NumberFilter(field_name='category_id')
    status = NumberFilter(field_name='status')
    search = CharFilter(method='filter_search')

    def filter_district_in(self, queryset, name, value):
        ids = [int(i) for i in value.split(',') if i.strip().isdigit()]
        return queryset.filter(district_id__in=ids) if ids else queryset

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(community__icontains=value) |
            models.Q(address__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(summary__icontains=value)
        )

    def filter_district_in(self, queryset, name, value):
        ids = [int(i) for i in value.split(',') if i.strip().isdigit()]
        return queryset.filter(district_id__in=ids) if ids else queryset

    class Meta:
        model = House
        fields = []


class HouseListView(generics.ListAPIView):
    """房源列表（支持多条件筛选+排序）"""
    serializer_class = HouseListSerializer
    filterset_class = HouseFilter
    ordering_fields = ['price', 'area_size', 'created_at', 'view_count']
    ordering = ['-is_sticky', '-created_at']

    def get_queryset(self):
        qs = House.objects.select_related('category', 'district', 'area_ref', 'owner')
        # 默认只显示出租中
        if 'status' not in self.request.query_params:
            qs = qs.filter(status=0)
        return qs


class HouseDetailView(generics.RetrieveAPIView):
    """房源详情"""
    serializer_class = HouseDetailSerializer
    queryset = House.objects.select_related('category', 'district', 'area_ref', 'owner')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 浏览量+1
        House.objects.filter(pk=instance.pk).update(view_count=instance.view_count + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class HouseCreateView(generics.CreateAPIView):
    """发布房源"""
    serializer_class = HouseCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        house = serializer.save()
        # 处理图片上传
        images = request.FILES.getlist('images')
        for i, img in enumerate(images):
            HouseImage.objects.create(house=house, image=img, sort=i)
        return Response(
            HouseDetailSerializer(house, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )


class HouseUpdateView(generics.UpdateAPIView):
    """编辑房源"""
    serializer_class = HouseCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return House.objects.all()
        return House.objects.filter(owner=user)


class HouseDeleteView(generics.DestroyAPIView):
    """删除房源"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return House.objects.all()
        return House.objects.filter(owner=user)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_house_image(request, pk):
    """删除房源图片"""
    try:
        img = HouseImage.objects.select_related('house').get(pk=pk)
    except HouseImage.DoesNotExist:
        return Response({'error': '图片不存在'}, status=404)
    if img.house.owner != request.user and not request.user.is_staff:
        return Response({'error': '无权操作'}, status=403)
    img.delete()
    return Response({'msg': '已删除'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_house_images(request, pk):
    """为已有房源上传图片"""
    try:
        house = House.objects.get(pk=pk)
    except House.DoesNotExist:
        return Response({'error': '房源不存在'}, status=404)
    if house.owner != request.user and not request.user.is_staff:
        return Response({'error': '无权操作'}, status=403)
    images = request.FILES.getlist('images')
    if not images:
        return Response({'error': '请选择图片'}, status=400)
    max_sort = house.images.aggregate(m=models.Max('sort'))['m'] or 0
    created = []
    for i, img in enumerate(images):
        obj = HouseImage.objects.create(house=house, image=img, sort=max_sort + i + 1)
        created.append(HouseImageSerializer(obj, context={'request': request}).data)
    return Response(created, status=status.HTTP_201_CREATED)


class MyHouseListView(generics.ListAPIView):
    """房东自己的房源列表"""
    serializer_class = HouseListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = House.objects.filter(owner=self.request.user).select_related(
            'category', 'district', 'area_ref', 'owner'
        )
        status_param = self.request.query_params.get('status')
        if status_param is not None and status_param != '':
            qs = qs.filter(status=int(status_param))
        return qs


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def recommended_houses(request):
    """推荐房源"""
    houses = House.objects.filter(is_recommended=True, status=0)[:6]
    serializer = HouseListSerializer(houses, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def latest_houses(request):
    """最新房源"""
    houses = House.objects.filter(status=0).order_by('-created_at')[:6]
    serializer = HouseListSerializer(houses, many=True, context={'request': request})
    return Response(serializer.data)


class CategoryListView(generics.ListAPIView):
    """分类列表"""
    queryset = HouseCategory.objects.all()
    serializer_class = HouseCategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ProvinceListView(generics.ListAPIView):
    """省份列表（含城市）"""
    queryset = Province.objects.prefetch_related('cities').all()
    serializer_class = ProvinceWithCitiesSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class DistrictListView(generics.ListAPIView):
    """区域列表（含商圈）"""
    queryset = District.objects.select_related('city__province').prefetch_related('areas').all()
    serializer_class = DistrictWithAreasSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class FavoriteListCreateView(generics.ListCreateAPIView):
    """收藏列表/添加收藏"""
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related(
            'house__category', 'house__district', 'house__area_ref'
        )

    def create(self, request, *args, **kwargs):
        house_id = request.data.get('house')
        fav, created = Favorite.objects.get_or_create(
            user=request.user, house_id=house_id
        )
        if not created:
            # 已收藏则取消
            fav.delete()
            return Response({'is_favorited': False})
        return Response({'is_favorited': True}, status=status.HTTP_201_CREATED)


class DictionaryListView(generics.ListAPIView):
    """字典列表（公开接口，按 group 过滤）"""
    serializer_class = DictionarySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        qs = Dictionary.objects.filter(is_active=True)
        group = self.request.query_params.get('group')
        area = self.request.query_params.get('area')
        if group:
            qs = qs.filter(group=group)
        if area:
            qs = qs.filter(area_id=area)
        return qs


class DictionaryManageView(generics.ListCreateAPIView):
    """字典管理（管理员 CRUD）"""
    serializer_class = DictionarySerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = None

    def get_queryset(self):
        qs = Dictionary.objects.all()
        group = self.request.query_params.get('group')
        if group:
            qs = qs.filter(group=group)
        return qs


class DictionaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """字典项详情/编辑/删除"""
    serializer_class = DictionarySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Dictionary.objects.all()
