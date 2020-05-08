from userSystem.models import *
from userSystem.cache.datacache import RolesCache


class AddUserPermission(object):

    def has_permission(self, request, view):
        cacheTool = RolesCache(model=UserInfo)
        key = 'rolesCache+' + str(request.user)
        roleList = cacheTool.getRolesFromCache(key)

        if '管理员' in roleList:
            return True
        return False