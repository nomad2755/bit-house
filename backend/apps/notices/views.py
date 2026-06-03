from rest_framework import generics, permissions
from .models import Notice
from .serializers import NoticeListSerializer, NoticeDetailSerializer


class NoticeListView(generics.ListAPIView):
    """公告列表（只返回已发布）"""
    serializer_class = NoticeListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Notice.objects.all()
        # 非管理员只看已发布
        if not (self.request.user.is_authenticated and self.request.user.is_staff):
            qs = qs.filter(is_published=True)
        return qs


class NoticeDetailView(generics.RetrieveAPIView):
    """公告详情"""
    serializer_class = NoticeDetailSerializer
    queryset = Notice.objects.all()
    permission_classes = [permissions.AllowAny]


class NoticeCreateView(generics.CreateAPIView):
    """发布公告（管理员）"""
    serializer_class = NoticeDetailSerializer
    permission_classes = [permissions.IsAdminUser]


class NoticeUpdateView(generics.UpdateAPIView):
    """编辑公告（管理员）"""
    serializer_class = NoticeDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Notice.objects.all()


class NoticeDeleteView(generics.DestroyAPIView):
    """删除公告（管理员）"""
    permission_classes = [permissions.IsAdminUser]
    queryset = Notice.objects.all()
