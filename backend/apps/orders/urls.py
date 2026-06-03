from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # 看房预约
    path('view-requests/', views.ViewRequestListView.as_view(), name='view-request-list'),
    path('view-requests/create/', views.ViewRequestCreateView.as_view(), name='view-request-create'),
    path('view-requests/<int:pk>/confirm/', views.confirm_view_request, name='view-request-confirm'),
    path('view-requests/<int:pk>/complete/', views.complete_view_request, name='view-request-complete'),
    path('view-requests/<int:pk>/cancel/', views.cancel_view_request, name='view-request-cancel'),

    # 租赁合同
    path('contracts/', views.ContractListView.as_view(), name='contract-list'),
    path('contracts/create/', views.ContractCreateView.as_view(), name='contract-create'),
    path('contracts/<int:pk>/', views.ContractDetailView.as_view(), name='contract-detail'),
    path('contracts/<int:pk>/review/', views.landlord_review_contract, name='contract-review'),
    path('contracts/<int:pk>/sign/', views.sign_contract, name='contract-sign'),
    path('contracts/<int:pk>/terminate/', views.terminate_contract, name='contract-terminate'),
    path('contracts/<int:pk>/checkout/', views.checkout_contract, name='contract-checkout'),
    path('contracts/<int:pk>/renew/', views.renew_contract, name='contract-renew'),

    # 租金缴纳
    path('payments/', views.RentPaymentListView.as_view(), name='payment-list'),
    path('payments/<int:pk>/pay/', views.pay_rent, name='payment-pay'),
    path('payments/<int:pk>/confirm/', views.confirm_rent_payment, name='payment-confirm'),
]
