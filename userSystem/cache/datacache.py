from django.core.cache import cache
from userSystem.models import *
from userSystem.serialzer import PermissionsSerializer


class DataCache:

    def __init__(self, timeout=60*60):
        self.timeout = timeout

    def cacheTest(self):
        if cache.has_key('hello'):
            result = cache.get('hello')
        else:
            result = {'toekn': 'hello', 'user': '233'}
            cache.set('hello', result, self.timeout)
        return result

    def createOrUpdateToken(self, key: str, dic: dict):
        cache.set(key, dic, self.timeout)
        return key

    def getTokenFromCache(self, key: str):
        if cache.has_key(key):
            result = cache.get(key)
        else:
            result = {}
        return result


class RolesCache:

    def __init__(self, model, timeout=60*60*3):
        self.model = model
        self.timeout = timeout

    def getRolesFromCache(self, key: str):
        userId = key.split('+')[1]
        result = cache.get(key)
        if not result:
            user = self.model.objects.get(id=userId)
            roles = user.roles.all()
            result = [x.name for x in roles]
            cache.set(key, result, self.timeout)
        return result


class PermissionCache:

    def __init__(self, timeout=60*60*3):
        self.timeout = timeout

    def getPermissionFromCache(self, key: str):
        userId = key.split('+')[1]
        result = cache.get(key)
        if not result:
            # 通过用户的id获取该用户的角色信息
            user = UserInfo.objects.get(id=userId)
            # 该用户关联的角色（用户角色多对多）
            role = user.roles.all()
            # 该用户单独关联的权限（用户角色多对多）
            userPermission = user.permissions.all()
            userPermission = PermissionsSerializer(userPermission, many=True)
            result = userPermission.data
            rolesIdList = [x.id for x in role]
            # 通过角色信息获取所有的权限（角色权限多对多）
            for onerole in rolesIdList:
                permission = Role.objects.get(id=onerole)
                permission = permission.permissions.all()
                permission = PermissionsSerializer(permission, many=True)
                result += permission.data
            cache.set(key, result, self.timeout)
        return result

