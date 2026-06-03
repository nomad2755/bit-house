from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import (
    CustomTokenObtainSerializer,
    UserRegisterSerializer,
    UserProfileSerializer,
    UserAdminSerializer,
)


class LoginView(TokenObtainPairView):
    """登录（支持用户名或身份证号）"""
    serializer_class = CustomTokenObtainSerializer


class RegisterView(generics.CreateAPIView):
    """注册"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """个人信息查看/修改"""
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """用户列表（管理员）"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateAPIView):
    """用户详情（管理员）"""
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAdminUser]
