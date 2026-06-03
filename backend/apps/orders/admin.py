from django.contrib import admin
from .models import ViewRequest, Contract, RentPayment


@admin.register(ViewRequest)
class ViewRequestAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'house', 'view_date', 'view_time', 'status', 'created_at']
    list_filter = ['status']


class RentPaymentInline(admin.TabularInline):
    model = RentPayment
    extra = 0
    readonly_fields = ['period_start', 'period_end', 'amount', 'due_date']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['contract_no', 'house', 'landlord', 'tenant', 'status',
                    'start_date', 'end_date', 'rent_amount']
    list_filter = ['status', 'payment_cycle', 'sign_method']
    search_fields = ['contract_no']
    inlines = [RentPaymentInline]


@admin.register(RentPayment)
class RentPaymentAdmin(admin.ModelAdmin):
    list_display = ['contract', 'period_start', 'period_end', 'amount',
                    'due_date', 'status']
    list_filter = ['status']
