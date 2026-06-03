from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListView(generics.ListAPIView):
    """收支明细"""
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=user)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def finance_statistics(request):
    """财务统计（管理员）"""
    total_income = Transaction.objects.filter(amount__gt=0).aggregate(
        total=Sum('amount'))['total'] or 0
    total_expense = Transaction.objects.filter(amount__lt=0).aggregate(
        total=Sum('amount'))['total'] or 0
    # 按类型统计
    by_type = Transaction.objects.values('type').annotate(
        total=Sum('amount'), count=Count('id')
    )
    return Response({
        'total_income': total_income,
        'total_expense': total_expense,
        'net': total_income + total_expense,
        'by_type': list(by_type),
    })
