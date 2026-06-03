from django.db import models


class Transaction(models.Model):
    """收支明细"""
    TYPE_CHOICES = [
        ('rent', '租金'),
        ('deposit', '押金'),
        ('refund', '退款'),
        ('recharge', '充值'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                              related_name='transactions', verbose_name='用户')
    contract = models.ForeignKey('orders.Contract', on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='transactions',
                                  verbose_name='关联合同')
    amount = models.DecimalField('金额', max_digits=10, decimal_places=2,
                                  help_text='正=收入/负=支出')
    type = models.CharField('类型', max_length=10, choices=TYPE_CHOICES)
    description = models.CharField('描述', max_length=200, blank=True, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'transaction'
        verbose_name = '收支明细'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.amount}'
