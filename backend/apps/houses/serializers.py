from rest_framework import serializers
from .models import House, HouseImage, HouseCategory, District, Area, Favorite, Dictionary, Province, City


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'sort']


class CitySerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'province_name', 'sort']


class ProvinceWithCitiesSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = ['id', 'name', 'sort', 'cities']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'sort']


class AreaSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'district', 'district_name', 'sort']


class DistrictWithAreasSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True, read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True, default='')
    province_name = serializers.CharField(source='city.province.name', read_only=True, default='')

    class Meta:
        model = District
        fields = ['id', 'name', 'city', 'city_name', 'province_name', 'sort', 'areas']


class HouseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseCategory
        fields = ['id', 'name', 'sort', 'description']


class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        fields = ['id', 'image', 'sort']


class HouseListSerializer(serializers.ModelSerializer):
    """房源列表（精简）"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    area_name = serializers.CharField(source='area_ref.name', read_only=True, default='')
    cover_image = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = ['id', 'title', 'category_name', 'district_name', 'area_name',
                  'community', 'price', 'area_size', 'layout_desc', 'floor_level',
                  'orientation', 'has_elevator', 'has_subway', 'is_new',
                  'status', 'cover_image', 'is_favorited', 'view_count', 'created_at']

    def get_cover_image(self, obj):
        first_img = obj.images.first()
        if first_img:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_img.image.url)
            return first_img.image.url
        return None

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False


class HouseDetailSerializer(serializers.ModelSerializer):
    """房源详情（完整）"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    area_name = serializers.CharField(source='area_ref.name', read_only=True, default='')
    owner_name = serializers.CharField(source='owner.display_name', read_only=True)
    owner_avatar = serializers.ImageField(source='owner.avatar', read_only=True)
    images = HouseImageSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = '__all__'

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False


class HouseCreateUpdateSerializer(serializers.ModelSerializer):
    """房源创建/编辑"""
    class Meta:
        model = House
        fields = ['title', 'description', 'summary', 'category', 'district',
                  'area_ref', 'community', 'address', 'price', 'deposit',
                  'area_size', 'room_count', 'hall_count', 'toilet_count',
                  'floor', 'total_floors', 'orientation', 'decoration',
                  'has_elevator', 'has_subway', 'facilities', 'pay_type',
                  'lease_term', 'status', 'is_recommended', 'is_sticky',
                  'is_new']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    house = HouseListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'house', 'created_at']


class DictionarySerializer(serializers.ModelSerializer):
    """字典项"""
    group_label = serializers.CharField(source='get_group_display', read_only=True)
    area_name = serializers.CharField(source='area.name', read_only=True, default='')

    class Meta:
        model = Dictionary
        fields = ['id', 'group', 'group_label', 'label', 'value', 'area',
                  'area_name', 'sort', 'is_active']
        read_only_fields = ['id']
