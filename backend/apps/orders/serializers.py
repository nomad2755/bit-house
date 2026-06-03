from rest_framework import serializers
from datetime import date
from .models import ViewRequest, Contract, RentPayment


class ViewRequestSerializer(serializers.ModelSerializer):
    """看房预约"""
    house_title = serializers.CharField(source='house.title', read_only=True)
    tenant_name = serializers.CharField(source='tenant.display_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ViewRequest
        fields = ['id', 'house', 'house_title', 'tenant', 'tenant_name',
                  'view_date', 'view_time', 'contact_phone', 'remark',
                  'status', 'status_display', 'created_at']
        read_only_fields = ['tenant', 'status']


class ViewRequestCreateSerializer(serializers.ModelSerializer):
    """创建看房预约"""
    class Meta:
        model = ViewRequest
        fields = ['house', 'view_date', 'view_time', 'contact_phone', 'remark']

    def create(self, validated_data):
        validated_data['tenant'] = self.context['request'].user
        return super().create(validated_data)


class RentPaymentSerializer(serializers.ModelSerializer):
    """租金缴纳记录"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = RentPayment
        fields = ['id', 'contract', 'period_start', 'period_end', 'amount',
                  'paid_amount', 'due_date', 'paid_date', 'payment_method',
                  'status', 'status_display', 'is_overdue', 'remark']


class ContractListSerializer(serializers.ModelSerializer):
    """合同列表(精简)"""
    house_title = serializers.CharField(source='house.title', read_only=True)
    landlord_name = serializers.CharField(source='landlord.display_name', read_only=True)
    tenant_name = serializers.CharField(source='tenant.display_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    days_until_expire = serializers.IntegerField(read_only=True)
    is_expiring_soon = serializers.BooleanField(read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'contract_no', 'house_title', 'landlord_name', 'tenant_name',
                  'start_date', 'end_date', 'rent_amount', 'deposit_amount',
                  'payment_cycle', 'status', 'status_display',
                  'days_until_expire', 'is_expiring_soon', 'created_at']


class ContractDetailSerializer(serializers.ModelSerializer):
    """合同详情(完整)"""
    house_title = serializers.CharField(source='house.title', read_only=True)
    landlord_name = serializers.CharField(source='landlord.display_name', read_only=True)
    tenant_name = serializers.CharField(source='tenant.display_name', read_only=True)
    landlord_phone = serializers.CharField(source='landlord.phone', read_only=True)
    tenant_phone = serializers.CharField(source='tenant.phone', read_only=True)
    landlord_id_card = serializers.CharField(source='landlord.id_card', read_only=True)
    tenant_id_card = serializers.CharField(source='tenant.id_card', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_cycle_display = serializers.CharField(source='get_payment_cycle_display', read_only=True)
    lease_months = serializers.IntegerField(read_only=True)
    total_rent = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    days_until_expire = serializers.IntegerField(read_only=True)
    payments = RentPaymentSerializer(many=True, read_only=True)
    renewals = ContractListSerializer(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'


class ContractCreateSerializer(serializers.ModelSerializer):
    """创建合同(起草)"""
    class Meta:
        model = Contract
        fields = ['landlord', 'house', 'start_date', 'end_date',
                  'rent_amount', 'deposit_amount', 'payment_cycle', 'payment_day',
                  'sign_method', 'property_desc', 'special_terms', 'remark']

    def validate(self, attrs):
        if attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError({'end_date': '终止日必须晚于起租日'})
        if attrs['start_date'] < date.today():
            raise serializers.ValidationError({'start_date': '起租日不能早于今天'})
        return attrs

    def create(self, validated_data):
        house = validated_data['house']
        # 自动填充房屋信息
        validated_data['tenant'] = self.context['request'].user
        validated_data['property_address'] = f'{house.district.name if house.district else ""} {house.community} {house.address}'
        validated_data['property_area'] = house.area_size
        contract = Contract.objects.create(**validated_data)
        return contract


class ContractSignSerializer(serializers.Serializer):
    """签约确认"""
    move_in_water = serializers.FloatField(required=False)
    move_in_electric = serializers.FloatField(required=False)
    move_in_gas = serializers.FloatField(required=False)
    move_in_notes = serializers.CharField(required=False, allow_blank=True)


class ContractCheckoutSerializer(serializers.Serializer):
    """退房验收"""
    move_out_water = serializers.FloatField(required=False)
    move_out_electric = serializers.FloatField(required=False)
    move_out_gas = serializers.FloatField(required=False)
    move_out_notes = serializers.CharField(required=False, allow_blank=True)
    deposit_refund_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
