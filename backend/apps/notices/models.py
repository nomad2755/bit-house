from django.db import models


class Notice(models.Model):
    """公告"""
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    summary = models.CharField('摘要', max_length=200, blank=True, default='')
    is_published = models.BooleanField('是否发布', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'notice'
        verbose_name = '公告'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title
