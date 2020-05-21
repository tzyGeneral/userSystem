from django.core.cache import cache
from userSystem.models import *
from userSystem.cache.datacache import DataCache
from userSystem.serialzer import PermissionsSerializer


def checkUserNmaeTool(userName: str):
    """
    查询 user_name -> user_id 的缓存
    :param userName:
    :return:
    """
    key = 'usernameCache+' + str(userName)
    if cache.has_key(key):
        # 缓存中有则返回user_id
        return cache.get(key)
    else:
        # 没有返回None，视图层再做操作
        return None


def checkUserInfoTool(user_id: str):
    """
    查询 user_info -> user_id 的缓存
    :param user_id:
    :return:
    """
    key = 'userIdCache+' + str(user_id)
    if cache.has_key(key):
        # 缓存中存在则返回True
        return True
    else:
        # 没有返回False, 试图层再做操作
        return False


def setUsername2UseridToCache(username: str):
    """
    通过user_name从DB中存储user_id
    :param username:
    :return:
    """
    key = 'usernameCache+' + str(username)
    # 通过用户名user_name查询用户的user_id
    user = UserInfo.objects.get(username=username)
    if user:
        # 将user_id存入缓存中， key：user_name, value: user_id
        DataCache(timeout=60 * 60 * 3).setCache(key=key, value=user.id)
        return user.id

def setUserid2UserInfoToCache(user_id: str):
    """
    根据user_id查询user_info包含角色，权限，存入缓存
    :param user_id:
    :return:
    """
    key = 'permissionCache+' + str(user_id)
    # 通过用户的id获取该用户的角色信息
    user = UserInfo.objects.get(id=user_id)
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

    # 将user_info(包含角色，权限)存入缓存中
    DataCache(timeout=60 * 60 * 3).setCache(key=key, value=result)
