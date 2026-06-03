from django.urls import path
from . import views

app_name = 'notices'

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='notice-list'),
    path('create/', views.NoticeCreateView.as_view(), name='notice-create'),
    path('<int:pk>/', views.NoticeDetailView.as_view(), name='notice-detail'),
    path('<int:pk>/update/', views.NoticeUpdateView.as_view(), name='notice-update'),
    path('<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='notice-delete'),
]
