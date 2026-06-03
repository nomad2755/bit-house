from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型，支持房东/租客/管理员三种角色"""

    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('owner', '房东'),
        ('tenant', '租客'),
    ]

    display_name = models.CharField('昵称', max_length=50, blank=True, default='')
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='tenant')
    phone = models.CharField('手机号', max_length=11, blank=True, default='', unique=True)
    id_card = models.CharField('身份证号', max_length=18, blank=True, default='')
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, default='')
    balance = models.DecimalField('账户余额', max_digits=10, decimal_places=2, default=0)
    email = models.EmailField('邮箱', blank=True, default='')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.display_name or self.username
