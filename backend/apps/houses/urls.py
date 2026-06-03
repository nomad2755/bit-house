from django.urls import path
from . import views

app_name = 'houses'

urlpatterns = [
    path('', views.HouseListView.as_view(), name='house-list'),
    path('my/', views.MyHouseListView.as_view(), name='my-house-list'),
    path('create/', views.HouseCreateView.as_view(), name='house-create'),
    path('<int:pk>/', views.HouseDetailView.as_view(), name='house-detail'),
    path('<int:pk>/update/', views.HouseUpdateView.as_view(), name='house-update'),
    path('<int:pk>/delete/', views.HouseDeleteView.as_view(), name='house-delete'),
    path('images/<int:pk>/delete/', views.delete_house_image, name='house-image-delete'),
    path('<int:pk>/images/upload/', views.upload_house_images, name='house-images-upload'),
    path('recommended/', views.recommended_houses, name='recommended'),
    path('latest/', views.latest_houses, name='latest'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('districts/', views.DistrictListView.as_view(), name='district-list'),
    path('provinces/', views.ProvinceListView.as_view(), name='province-list'),
    path('favorites/', views.FavoriteListCreateView.as_view(), name='favorite-list'),
    path('dicts/', views.DictionaryListView.as_view(), name='dict-list'),
    path('dicts/manage/', views.DictionaryManageView.as_view(), name='dict-manage'),
    path('dicts/<int:pk>/', views.DictionaryDetailView.as_view(), name='dict-detail'),
]
