from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('statistics/', views.finance_statistics, name='finance-statistics'),
]
