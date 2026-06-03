from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import models
from django.utils import timezone
from datetime import date
from .models import ViewRequest, Contract, RentPayment
from .serializers import (
    ViewRequestSerializer, ViewRequestCreateSerializer,
    ContractListSerializer, ContractDetailSerializer, ContractCreateSerializer,
    ContractSignSerializer, ContractCheckoutSerializer,
    RentPaymentSerializer,
)


# ========== 看房预约 ==========

class ViewRequestCreateView(generics.CreateAPIView):
    """创建看房预约"""
    serializer_class = ViewRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ViewRequestListView(generics.ListAPIView):
    """看房预约列表"""
    serializer_class = ViewRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ViewRequest.objects.all()
        # 房东看自己房源的预约，租客看自己的预约
        return ViewRequest.objects.filter(
            models.Q(tenant=user) | models.Q(house__owner=user)
        ).distinct()


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def confirm_view_request(request, pk):
    """房东确认看房预约"""
    try:
        vr = ViewRequest.objects.get(pk=pk, house__owner=request.user, status='pending')
    except ViewRequest.DoesNotExist:
        return Response({'error': '预约不存在或无权操作'}, status=404)
    vr.status = 'confirmed'
    vr.save()
    return Response(ViewRequestSerializer(vr).data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def complete_view_request(request, pk):
    """标记已看房"""
    try:
        vr = ViewRequest.objects.get(pk=pk, status='confirmed')
        if request.user != vr.tenant and request.user != vr.house.owner:
            return Response({'error': '无权操作'}, status=403)
    except ViewRequest.DoesNotExist:
        return Response({'error': '预约不存在'}, status=404)
    vr.status = 'completed'
    vr.save()
    return Response(ViewRequestSerializer(vr).data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def cancel_view_request(request, pk):
    """取消看房"""
    try:
        vr = ViewRequest.objects.get(pk=pk, tenant=request.user)
        if vr.status in ('cancelled', 'completed'):
            return Response({'error': '当前状态不可取消'}, status=400)
    except ViewRequest.DoesNotExist:
        return Response({'error': '预约不存在'}, status=404)
    vr.status = 'cancelled'
    vr.save()
    return Response(ViewRequestSerializer(vr).data)


# ========== 租赁合同 ==========

class ContractCreateView(generics.CreateAPIView):
    """起草合同(租客发起)"""
    serializer_class = ContractCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContractListView(generics.ListAPIView):
    """合同列表"""
    serializer_class = ContractListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Contract.objects.select_related('house', 'landlord', 'tenant').all()
        return Contract.objects.filter(
            models.Q(tenant=user) | models.Q(landlord=user)
        ).select_related('house', 'landlord', 'tenant').distinct()


class ContractDetailView(generics.RetrieveAPIView):
    """合同详情"""
    serializer_class = ContractDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Contract.objects.all()
        return Contract.objects.filter(
            models.Q(tenant=user) | models.Q(landlord=user)
        ).distinct()


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def landlord_review_contract(request, pk):
    """房东审核合同(草稿→待签约)"""
    try:
        contract = Contract.objects.get(pk=pk, landlord=request.user, status='draft')
    except Contract.DoesNotExist:
        return Response({'error': '合同不存在或无权操作'}, status=404)
    action = request.data.get('action')
    if action == 'approve':
        contract.status = 'pending_sign'
        contract.save()
        return Response({'status': 'pending_sign', 'msg': '已通过审核，等待签约'})
    elif action == 'reject':
        contract.status = 'terminated'
        contract.termination_reason = request.data.get('reason', '房东拒绝')
        contract.save()
        return Response({'status': 'terminated', 'msg': '已拒绝'})
    return Response({'error': '请提供 action: approve/reject'}, status=400)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def sign_contract(request, pk):
    """签约(双方确认→合同生效)

    流程: 双方各自确认签约，最后确认的一方完成时合同变为 active
    并自动生成首期和后续的租金缴纳计划
    """
    try:
        contract = Contract.objects.get(pk=pk, status='pending_sign')
        if request.user != contract.tenant and request.user != contract.landlord:
            return Response({'error': '无权操作'}, status=403)
    except Contract.DoesNotExist:
        return Response({'error': '合同不存在或状态不正确'}, status=404)

    # 记录签约
    serializer = ContractSignSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if request.user == contract.landlord:
        contract.landlord_signed = True  # 用 remark 标记
        contract.remark += f'\n[房东签约确认 {timezone.now()}]'
    else:
        contract.remark += f'\n[租客签约确认 {timezone.now()}]'
        # 填充入住验收数据
        for field in ['move_in_water', 'move_in_electric', 'move_in_gas', 'move_in_notes']:
            if field in serializer.validated_data:
                setattr(contract, field, serializer.validated_data[field])

    # 如果两方都确认了(通过 remark 判断)，合同生效
    if '[房东签约确认' in contract.remark and '[租客签约确认' in contract.remark:
        contract.status = 'active'
        contract.signed_at = timezone.now()
        contract.move_in_date = contract.start_date
        contract.save()
        # 房源标记已租出
        contract.house.status = 1
        contract.house.save()
        # 自动生成租金缴纳计划
        _generate_payment_schedule(contract)
        return Response({'status': 'active', 'msg': '合同已生效'})
    else:
        contract.save()
        return Response({'status': 'pending_sign', 'msg': '已确认签约，等待对方确认'})


def _generate_payment_schedule(contract):
    """根据合同生成租金缴纳计划"""
    from dateutil.relativedelta import relativedelta
    payments = []
    cycle_months = {
        'monthly': 1, 'quarterly': 3,
        'semi_annual': 6, 'annual': 12,
    }
    step = cycle_months.get(contract.payment_cycle, 3)
    current = contract.start_date
    while current < contract.end_date:
        period_end = min(
            current + relativedelta(months=step) - relativedelta(days=1),
            contract.end_date
        )
        due_day = current.replace(day=min(contract.payment_day, 28))
        payments.append(RentPayment(
            contract=contract,
            period_start=current,
            period_end=period_end,
            amount=contract.rent_amount * step,
            due_date=due_day,
        ))
        current = current + relativedelta(months=step)
    RentPayment.objects.bulk_create(payments)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def terminate_contract(request, pk):
    """提前解约"""
    try:
        contract = Contract.objects.get(pk=pk, status='active')
        if request.user != contract.tenant and request.user != contract.landlord:
            return Response({'error': '无权操作'}, status=403)
    except Contract.DoesNotExist:
        return Response({'error': '合同不存在或状态不正确'}, status=404)

    contract.status = 'terminated'
    contract.termination_date = date.today()
    contract.termination_reason = request.data.get('reason', '')
    contract.early_termination_penalty = request.data.get('penalty', 0)
    contract.save()
    # 房源恢复可租
    contract.house.status = 0
    contract.house.save()
    return Response({'status': 'terminated', 'msg': '合同已解约'})


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def checkout_contract(request, pk):
    """退房验收 + 押金退还"""
    try:
        contract = Contract.objects.get(pk=pk)
        if contract.status not in ('active', 'expired'):
            return Response({'error': '合同状态不正确'}, status=400)
        if request.user != contract.tenant and request.user != contract.landlord:
            return Response({'error': '无权操作'}, status=403)
    except Contract.DoesNotExist:
        return Response({'error': '合同不存在'}, status=404)

    serializer = ContractCheckoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    contract.move_out_date = date.today()
    contract.move_out_water = data.get('move_out_water')
    contract.move_out_electric = data.get('move_out_electric')
    contract.move_out_gas = data.get('move_out_gas')
    contract.move_out_notes = data.get('move_out_notes', '')
    contract.deposit_refund_amount = data['deposit_refund_amount']
    contract.deposit_refund_date = date.today()

    # 退还押金到租客余额
    refund = data['deposit_refund_amount']
    if refund > 0:
        contract.tenant.balance += refund
        contract.tenant.save()

    contract.status = 'expired'
    contract.save()
    contract.house.status = 0
    contract.house.save()
    return Response({'status': 'expired', 'msg': f'退房完成，押金 ¥{refund} 已退还'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def renew_contract(request, pk):
    """续签合同(基于原合同生成新合同)"""
    try:
        parent = Contract.objects.get(pk=pk, status__in=('active', 'expired'))
        if request.user != parent.tenant and request.user != parent.landlord:
            return Response({'error': '无权操作'}, status=403)
    except Contract.DoesNotExist:
        return Response({'error': '原合同不存在'}, status=404)

    new_start = request.data.get('start_date', parent.end_date)
    new_end = request.data.get('end_date')
    new_rent = request.data.get('rent_amount', parent.rent_amount)

    if not new_end:
        return Response({'error': '请提供 end_date'}, status=400)

    # 原合同标记已续签
    parent.status = 'renewed'
    parent.save()

    new_contract = Contract.objects.create(
        landlord=parent.landlord,
        tenant=parent.tenant,
        house=parent.house,
        property_address=parent.property_address,
        property_area=parent.property_area,
        property_desc=parent.property_desc,
        start_date=new_start,
        end_date=new_end,
        rent_amount=new_rent,
        deposit_amount=parent.deposit_amount,
        payment_cycle=parent.payment_cycle,
        payment_day=parent.payment_day,
        sign_method=parent.sign_method,
        special_terms=parent.special_terms,
        renewal_count=parent.renewal_count + 1,
        parent_contract=parent,
        status='draft',
    )
    return Response(ContractDetailSerializer(new_contract).data, status=201)


# ========== 租金缴纳 ==========

class RentPaymentListView(generics.ListAPIView):
    """租金缴纳列表"""
    serializer_class = RentPaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return RentPayment.objects.all()
        return RentPayment.objects.filter(
            models.Q(contract__tenant=user) | models.Q(contract__landlord=user)
        ).distinct()


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def pay_rent(request, pk):
    """支付租金"""
    try:
        payment = RentPayment.objects.get(pk=pk, contract__tenant=request.user, status='pending')
    except RentPayment.DoesNotExist:
        return Response({'error': '账单不存在或无权操作'}, status=404)

    user = request.user
    if user.balance < payment.amount:
        return Response({'error': '余额不足'}, status=400)

    user.balance -= payment.amount
    user.save()
    payment.paid_amount = payment.amount
    payment.paid_date = timezone.now()
    payment.payment_method = request.data.get('payment_method', '平台钱包')
    payment.status = 'paid'
    payment.save()
    return Response(RentPaymentSerializer(payment).data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def confirm_rent_payment(request, pk):
    """房东确认收款"""
    try:
        payment = RentPayment.objects.get(
            pk=pk, contract__landlord=request.user, status='paid'
        )
    except RentPayment.DoesNotExist:
        return Response({'error': '账单不存在或无权操作'}, status=404)
    payment.status = 'confirmed'
    payment.save()
    return Response(RentPaymentSerializer(payment).data)
