from userSystem.models import *
from userSystem.cache.datacache import DataCache2
from userSystem.serialzer import PermissionsSerializer


def checkUserNmaeTool(userName: str):
    """
    查询 user_name -> user_id 的缓存
    :param userName:
    :return:
    """
    cacheTool = DataCache2(cacheName='user_id_cache', timeout=60*60*3)
    if cacheTool.checkKey(userName):
        # 缓存中有则返回user_id
        return cacheTool.getCache(key=userName)
    else:
        # 没有返回None，视图层再做操作
        return None


def checkUserInfoTool(user_id: str):
    """
    查询 user_id -> user_info 的缓存
    :param user_id:
    :return:
    """
    cacheTool = DataCache2(cacheName='user_info_cache', timeout=60*60*3)
    if cacheTool.checkKey(user_id):
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
    cacheTool = DataCache2(cacheName='user_id_cache', timeout=60*60*3)
    # 通过用户名user_name查询用户的user_id
    user = UserInfo.objects.filter(username=username).first()
    if user:
        # 将user_id存入缓存中， key：user_name, value: user_id
        cacheTool.setCache(key=username, value=user.id)
        return user.id


def setUserid2UserInfoToCache(user_id: str):
    """
    根据user_id查询user_info包含角色，权限，存入缓存
    :param user_id:
    :return:
    """
    cacheTool = DataCache2(cacheName='user_permission_cache', timeout=60*60*3)
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
    cacheTool.setCache(key=user_id, value=result)


def getPermissionFromCache(user_id: str):
    """
    通过 user_id 获取 user_info 的权限
    :param self:
    :param key:
    :return:
    """
    cacheTool = DataCache2(cacheName='user_permission_cache', timeout=60*60*3)
    result = cacheTool.getCache(user_id)
    if not result:
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
        cacheTool.setCache(key=user_id, value=result)
    return result
