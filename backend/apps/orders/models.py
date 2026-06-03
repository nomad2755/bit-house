from django.db import models
import uuid
from datetime import date, timedelta


def generate_contract_no():
    """生成合同编号: HT-YYYYMMDD-XXXX"""
    today = date.today().strftime('%Y%m%d')
    return f'HT-{today}-{uuid.uuid4().hex[:4].upper()}'


class ViewRequest(models.Model):
    """看房预约"""
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已看房'),
        ('cancelled', '已取消'),
    ]

    tenant = models.ForeignKey('users.User', on_delete=models.CASCADE,
                                related_name='view_requests', verbose_name='租客')
    house = models.ForeignKey('houses.House', on_delete=models.CASCADE,
                               related_name='view_requests', verbose_name='房源')
    view_date = models.DateField('预约看房日期')
    view_time = models.CharField('预约时间段', max_length=20,
                                  help_text='如: 10:00-11:00')
    contact_phone = models.CharField('联系电话', max_length=11)
    remark = models.TextField('备注', blank=True, default='')
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'view_request'
        verbose_name = '看房预约'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.tenant} 预约看房 {self.house}'


class Contract(models.Model):
    """租赁合同 - 核心模型

    生命周期: draft(草稿) → pending_sign(待签约) → active(生效中) → expired(到期)
                                                                ↗ renewed(续签→新合同)
                                                                ↘ terminated(提前解约)
    """
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('pending_sign', '待签约'),
        ('active', '生效中'),
        ('expired', '已到期'),
        ('terminated', '已解约'),
        ('renewed', '已续签'),
    ]

    PAYMENT_CYCLE_CHOICES = [
        ('monthly', '月付'),
        ('quarterly', '季付'),
        ('semi_annual', '半年付'),
        ('annual', '年付'),
    ]

    SIGN_METHOD_CHOICES = [
        ('paper', '纸质签约'),
        ('electronic', '电子签约'),
    ]

    # --- 合同元信息 ---
    contract_no = models.CharField('合同编号', max_length=30, unique=True,
                                    default=generate_contract_no)
    status = models.CharField('合同状态', max_length=15, choices=STATUS_CHOICES, default='draft')

    # --- 当事人信息 ---
    landlord = models.ForeignKey('users.User', on_delete=models.CASCADE,
                                  related_name='landlord_contracts', verbose_name='甲方(出租方)')
    tenant = models.ForeignKey('users.User', on_delete=models.CASCADE,
                                related_name='tenant_contracts', verbose_name='乙方(承租方)')

    # --- 房屋信息 ---
    house = models.ForeignKey('houses.House', on_delete=models.CASCADE,
                               related_name='contracts', verbose_name='租赁房屋')
    property_address = models.CharField('房屋地址', max_length=200, help_text='签约时锁定的完整地址')
    property_area = models.FloatField('房屋面积(㎡)')
    property_desc = models.TextField('房屋现状及设施', blank=True, default='',
                                      help_text='家具家电清单、装修状况等')

    # --- 租赁条款 ---
    start_date = models.DateField('租赁起始日')
    end_date = models.DateField('租赁终止日')
    rent_amount = models.DecimalField('月租金(元)', max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField('押金(元)', max_digits=10, decimal_places=2)
    payment_cycle = models.CharField('付款周期', max_length=15,
                                      choices=PAYMENT_CYCLE_CHOICES, default='quarterly')
    payment_day = models.IntegerField('付款日', default=1, help_text='每月几号付款')

    # --- 签约信息 ---
    sign_method = models.CharField('签约方式', max_length=10,
                                    choices=SIGN_METHOD_CHOICES, default='paper')
    signed_at = models.DateTimeField('签约时间', null=True, blank=True)
    contract_pdf = models.FileField('合同PDF', upload_to='contracts/', blank=True, default='')

    # --- 交房验收 ---
    move_in_date = models.DateField('实际入住日', null=True, blank=True)
    move_in_water = models.FloatField('入住水表读数', null=True, blank=True)
    move_in_electric = models.FloatField('入住电表读数', null=True, blank=True)
    move_in_gas = models.FloatField('入住燃气表读数', null=True, blank=True)
    move_in_notes = models.TextField('入住验收备注', blank=True, default='')

    # --- 退房验收 ---
    move_out_date = models.DateField('实际退房日', null=True, blank=True)
    move_out_water = models.FloatField('退房水表读数', null=True, blank=True)
    move_out_electric = models.FloatField('退房电表读数', null=True, blank=True)
    move_out_gas = models.FloatField('退房燃气表读数', null=True, blank=True)
    move_out_notes = models.TextField('退房验收备注', blank=True, default='')
    deposit_refund_amount = models.DecimalField('押金退还金额', max_digits=10,
                                                 decimal_places=2, null=True, blank=True)
    deposit_refund_date = models.DateField('押金退还日期', null=True, blank=True)

    # --- 解约/续签 ---
    termination_reason = models.TextField('解约原因', blank=True, default='')
    termination_date = models.DateField('解约日期', null=True, blank=True)
    early_termination_penalty = models.DecimalField('违约金', max_digits=10,
                                                     decimal_places=2, default=0)
    renewal_count = models.IntegerField('续签次数', default=0)
    parent_contract = models.ForeignKey('self', on_delete=models.SET_NULL,
                                         null=True, blank=True,
                                         related_name='renewals',
                                         verbose_name='原合同(续签用)')

    # --- 备案信息 ---
    government_filing_status = models.CharField('备案状态', max_length=10,
                                                 default='pending',
                                                 help_text='pending/filed/not_required')
    government_filing_number = models.CharField('备案编号', max_length=50,
                                                 blank=True, default='')

    # --- 特别约定 ---
    special_terms = models.TextField('特别约定', blank=True, default='',
                                      help_text='宠物条款、装修限制、转租规则等')

    # --- 备注 ---
    remark = models.TextField('备注', blank=True, default='')

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'contract'
        verbose_name = '租赁合同'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'合同 {self.contract_no}'

    @property
    def lease_months(self):
        """租期月数"""
        return max(1, (self.end_date.year - self.start_date.year) * 12
                   + self.end_date.month - self.start_date.month)

    @property
    def total_rent(self):
        """租金总额"""
        return self.rent_amount * self.lease_months

    @property
    def days_until_expire(self):
        """距到期天数"""
        if self.end_date:
            return (self.end_date - date.today()).days
        return None

    @property
    def is_expiring_soon(self):
        """是否即将到期(30天内)"""
        days = self.days_until_expire
        return days is not None and 0 < days <= 30


class RentPayment(models.Model):
    """租金缴纳记录"""
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('overdue', '已逾期'),
        ('confirmed', '已确认'),
    ]

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE,
                                  related_name='payments', verbose_name='合同')
    period_start = models.DateField('账期开始')
    period_end = models.DateField('账期结束')
    amount = models.DecimalField('应付金额', max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField('实付金额', max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField('应付日期')
    paid_date = models.DateTimeField('支付时间', null=True, blank=True)
    payment_method = models.CharField('支付方式', max_length=20, blank=True, default='',
                                       help_text='微信/支付宝/银行转账/平台钱包')
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='pending')
    remark = models.CharField('备注', max_length=200, blank=True, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'rent_payment'
        verbose_name = '租金缴纳'
        verbose_name_plural = verbose_name
        ordering = ['period_start']

    def __str__(self):
        return f'{self.contract.contract_no} | {self.period_start}~{self.period_end}'

    @property
    def is_overdue(self):
        return self.status == 'pending' and self.due_date < date.today()
