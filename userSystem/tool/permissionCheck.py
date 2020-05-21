from userSystem.models import *


class AddUserPermission(object):

    def has_permission(self, request, view):
        requestMethod = request.method

        # 这里可能有的问题，就是用户被修改了角色之后，无法立即刷新，可能还是需要每次验证，查询一次数据库
        userObj = request.auth
        roles = userObj.roles.all()
        # 这里可以改成 x.id ，然后用id去判断是否有权限
        roleList = [x.name for x in roles]

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