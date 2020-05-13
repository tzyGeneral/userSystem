from userSystem.models import *
from userSystem.cache.datacache import RolesCache


class AddUserPermission(object):

    def has_permission(self, request, view):
        requestMethod = request.method

        cacheTool = RolesCache(model=UserInfo)
        key = 'rolesCache+' + str(request.user)
        roleList = cacheTool.getRolesFromCache(key)

        if requestMethod == 'GET':

            # if '管理员' in roleList:
            return True

        elif requestMethod == 'POST':

            if '管理员' in roleList:
                return True

        elif requestMethod == 'PUT':

            if '管理员' in roleList:
                return True
        elif requestMethod == 'DELETE':

            if '管理员' in roleList:
                return True
        else:
            return False

        return False