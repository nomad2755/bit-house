from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    """自定义JWT登录：支持用户名、身份证号、手机号登录"""

    username_field = 'username'

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username:
            # 手机号（11位纯数字）查找用户
            if username.isdigit() and len(username) == 11:
                user_obj = User.objects.filter(phone=username).first()
                if user_obj:
                    attrs['username'] = user_obj.username
            # 身份证号（18位，末位可能是X）查找用户
            elif len(username) == 18:
                user_obj = User.objects.filter(id_card=username).first()
                if user_obj:
                    attrs['username'] = user_obj.username

        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['username'] = user.username
        token['display_name'] = user.display_name or user.username
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册"""
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'phone', 'role']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('该用户名已被注册')
        return value

    def validate_phone(self, value):
        import re
        if not value:
            return value
        # 大陆手机号
        mainland = r'^1[3-9]\d{9}$'
        # 香港手机号
        hongkong = r'^(\+852)?[569]\d{7}$'
        # 澳门手机号
        macau = r'^(\+853)?6\d{7}$'
        if not (re.match(mainland, value) or re.match(hongkong, value) or re.match(macau, value)):
            raise serializers.ValidationError('请输入大陆、香港或澳门手机号')
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已被注册')
        return value

    def validate_id_card(self, value):
        if value and User.objects.filter(id_card=value).exists():
            raise serializers.ValidationError('该身份证号已被注册')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password2': '两次密码不一致'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """用户个人信息"""
    class Meta:
        model = User
        fields = ['id', 'username', 'display_name', 'role', 'phone',
                  'id_card', 'avatar', 'balance', 'email', 'date_joined']
        read_only_fields = ['id', 'username', 'role', 'balance', 'date_joined']


class UserAdminSerializer(serializers.ModelSerializer):
    """管理员查看用户"""
    class Meta:
        model = User
        fields = ['id', 'username', 'display_name', 'role', 'phone',
                  'email', 'balance', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']
