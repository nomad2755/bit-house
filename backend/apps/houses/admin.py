from django.contrib import admin
from .models import District, Area, HouseCategory, House, HouseImage, Favorite, Dictionary, Province, City


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'sort']
    list_filter = ['province']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'district', 'sort']
    list_filter = ['district']


@admin.register(HouseCategory)
class HouseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort']


class HouseImageInline(admin.TabularInline):
    model = HouseImage
    extra = 1


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'district', 'community', 'price', 'status', 'owner']
    list_filter = ['status', 'category', 'district']
    search_fields = ['title', 'community', 'address']
    inlines = [HouseImageInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'house', 'created_at']


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ['group', 'label', 'value', 'area', 'sort', 'is_active']
    list_filter = ['group', 'is_active']
    list_editable = ['sort', 'is_active']
    search_fields = ['label', 'value']
