from userSystem.models import *
from rest_framework import serializers


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        # exclude = ('createTime', 'updateTime')
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"
        depth = 3


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        depth = 2
