import datetime

import time
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from userSystem.tool.tools import md5
from userSystem.cache.datacache import DataCache2
from userSystem.cache.cacheTool import checkUserNmaeTool, checkUserInfoTool, setUserid2UserInfoToCache, setUsername2UseridToCache, getPermissionFromCache
from userSystem.tool.tokenCheck import Authtication
from userSystem.tool.permissionCheck import AddUserPermission
from userSystem import models
from userSystem.serialzer import UserInfoSerializer, PermissionsSerializer, RoleSerializer


class Hello(APIView):

    # authentication_classes = [Authtication, ]
    # permission_classes = [AddUserPermission, ]  # 权限控制，交给前端判断

    def get(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        try:
            rsp['data'] = DataCache2().checkKey('1')
        except Exception as e:
            rsp['code'] = 401
            rsp['msg'] = str(e)
        return Response(rsp)


class AuthView(APIView):
    """
    用户登陆
    """
    def post(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        errRsp = {'code': 300, 'msg': '用户名不存在'}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')

            # 查询username -> user_id 缓存
            user_id = checkUserNmaeTool(userName=user)
            # 假如user_id缓存不存在
            if not user_id:
                # 将user_name -> user_id 存入缓存中
                userId = setUsername2UseridToCache(username=user)
                # 假如用户名查询不存在，则直接返回，说明用户根本不存在
                if not userId:
                    return Response(errRsp)
                # 将user_id -> user_info 存入缓存中
                setUserid2UserInfoToCache(userId)

            # 假如user_id存在
            else:
                # 查询user_info缓存（根据user_id）
                user_info_check = checkUserInfoTool(user_id)
                # 不存在则从DB根据user_id查询user_info（包含角色，权限）
                if not user_info_check:
                    # 将user_info 存入缓存
                    setUserid2UserInfoToCache(user_id)
            # 确认用户密码
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            # 用户存在且没有被删除
            if obj is not None and not obj.isDelete:
                # 为登陆用户创建token
                token = md5(user)
                # 存在就更新，不存在就创建
                cacheTool = DataCache2(cacheName='user_token_cache', timeout=60*60*24)
                # 直接将queryset对象存入缓存中
                token = cacheTool.setCache(key=token, value=obj)
                rsp['token'] = token
                rsp['msg'] = '登陆成功'
            else:
                rsp['code'] = 300
                rsp['msg'] = '用户名或者密码错误'
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)


class TokenCheckView(APIView):
    """
    接口验证token
    """
    def get(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        token = request._request.GET.get('token')
        if not token:
            rsp['code'] = 300
            rsp['msg'] = '请携带token请求'
        else:
            cacheTool = DataCache2(cacheName='user_token_cache', timeout=60*60*24)
            tokenCheck = cacheTool.getCache(key=token)
            if not tokenCheck:
                rsp['code'] = 301
                rsp['msg'] = 'token过期请重新登陆'
            else:
                rsp['msg'] = 'token验证成功'
                rsp['data'] = tokenCheck
        return Response(rsp)


class GetPermissionsView(APIView):
    """
    当前用户的权限权限查询
    """
    authentication_classes = [Authtication, ]

    def get(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        try:
            user = request.user
            data = request.auth
            # 通过token拿到用户的信息，然后去取权限各种信息
            userPermission = getPermissionFromCache(user_id=user)
            rsp['data'] = userPermission
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)


class PermissionsView(APIView):
    """
    权限的增删改查
    """
    authentication_classes = [Authtication, ]

    def get(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        try:
            user = request.user
            permissionAll = models.Permissions.objects.filter(isDelete=False)
            permissionData = PermissionsSerializer(permissionAll, many=True)
            rsp['data'] = permissionData.data
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)

    def post(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        try:
            permissionDic = {
                "title": request._request.POST.get('title', ''),  # 需要新增的权限名
                "explain": request._request.POST.get('explain', ''),  # 权限说明
                "remarks": request._request.POST.get('remarks', ''),
                "createTime": datetime.datetime.now(),
                "createUserId": request.user,  # token验证后获取的当前用户id
                "updateTime": datetime.datetime.now(),
                "updateUserId": request.user
            }
            models.Permissions.objects.create(**permissionDic)
            rsp['msg'] = '新增权限成功'
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)

    def put(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        try:
            permissionid = request.data.get('permissionid')  # 要修改的权限的id
            permissionDic = {
                "title":  request.data.get('title',''),
                "explain": request.data.get('explain', ''),
                "remarks": request.data.get('remarks', ''),
                "updateTime": datetime.datetime.now(),
                "updateUserId": request.user
            }
            permission = models.Permissions.objects.filter(id=permissionid)
            permission.update(**permissionDic)
            rsp['msg'] = '修改权限成功'
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)

    def delete(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        try:
            permissionid = request.data.get('permissionid')  # 要删除的权限的id
            updateUserId = request.user
            updateTime = datetime.datetime.now()
            permissionObj = models.Permissions.objects.filter(id=permissionid)
            deleteDic = {
                "updateTime": updateTime,
                "updateUserId": updateUserId,
                "isDelete": True
            }
            permissionObj.update(**deleteDic)
            rsp['msg'] = '改权限已经删除'
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)


class RoleView(APIView):
    """
    角色的增删改查
    """
    authentication_classes = [Authtication, ]

    def get(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        # 查看所有用户的信息
        try:
            allRoleData = models.Role.objects.filter(isDelete=False)
            allRoleData = RoleSerializer(allRoleData, many=True)
            rsp['data'] = allRoleData.data
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)

    def post(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        try:
            # 为新增的角色添加权限(可以为多个，用+号分割)
            permission = request._request.POST.get('permission', '')
            permissionList = list(set(permission.split('+')))
            permissionList = [x for x in permissionList if x]

            role = models.Role(
                name=request._request.POST.get('name'),
                remarks=request._request.POST.get('remarks'),
                createTime=datetime.datetime.now(),
                createUserId=request.user,
                updateTime=datetime.datetime.now(),
                updateUserId=request.user
            )
            role.save()
            if permissionList:
                permissions = models.Permissions.objects.filter(id__in=permissionList)
                role.permissions.add(*permissions)
                role.save()
            rsp['msg'] = '成功添加角色'
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)

    def put(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        try:
            # 修改角色的单独权限(可以为多个，用+号分割)
            permission = request.data.get('permission', '')
            permissionList = list(set(permission.split('+')))
            permissionList = [x for x in permissionList if x]

            roleId = request.data.get('roleId')  # 要修改的角色的id
            name = request.data.get('name')
            remarks = request.data.get('remarks')
            updateTime = datetime.datetime.now()
            updateUserId = request.user

            role = models.Role.objects.get(id=roleId)
            role.name = name
            role.remarks = remarks
            role.updateTime = updateTime
            role.updateUserId = updateUserId

            if permissionList:
                permissions = models.Permissions.objects.filter(id__in=permissionList)
                role.permissions.clear()
                role.permissions.add(*permissions)
            role.save()
            rsp['msg'] = '角色信息修改成功'

        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)

    def delete(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        roleId = request.data.get('roleId')  # 要删除的角色的id
        updateUserId = request.user
        updateTime = datetime.datetime.now()
        try:
            roleObj = models.Role.objects.filter(id=roleId)
            deleteDic = {
                'updateTime': updateTime,
                'updateUserId': updateUserId,
                'isDelete': True
            }
            roleObj.update(**deleteDic)
            rsp['msg'] = '角色删除成功'
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)


class UserView(APIView):
    """
    用户的增删改查
    """
    authentication_classes = [Authtication, ]
    # permission_classes = [AddUserPermission, ]  # 权限控制，交给前端判断

    def get(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        # 查看所有用户的信息
        try:
            allUserData = models.UserInfo.objects.filter(isDelete=False)
            allUserData = UserInfoSerializer(allUserData, many=True)
            rsp['data'] = allUserData.data
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)

    def post(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        try:
            # 新增用户的角色(可以为多个，用+号分割)
            roles = request._request.POST.get('roles', '')
            rolesList = list(set(roles.split('+')))
            rolesList = [x for x in rolesList if x]
            # 新增用户的单独权限(可以为多个，用+号分割)
            permission = request._request.POST.get('permission', '')
            permissionList = list(set(permission.split('+')))
            permissionList = [x for x in permissionList if x]

            user = models.UserInfo(
                username=request._request.POST.get('username'),
                password=request._request.POST.get('password'),
                realName=request._request.POST.get('realName', ''),
                email=request._request.POST.get('email', ''),
                createTime=datetime.datetime.now(),
                createUserId=request.user,
                updateTime=datetime.datetime.now(),
                updateUserId=request.user
            )
            user.save()
            if rolesList:
                role = models.Role.objects.filter(id__in=rolesList)
                user.roles.add(*role)
            if permissionList:
                permissions = models.Permissions.objects.filter(id__in=permissionList)
                user.permissions.add(*permissions)
            user.save()
            # 通过token获取到用户的id信息
            user = request.user
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)

    def put(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        try:
            # 修改用户的角色(可以为多个，用+号分割)
            roles = request.data.get('roles','')
            rolesList = list(set(roles.split('+')))
            rolesList = [x for x in rolesList if x]
            # 修改用户的单独权限(可以为多个，用+号分割)
            permission = request.data.get('permission', '')
            permissionList = list(set(permission.split('+')))
            permissionList = [x for x in permissionList if x]

            userId = request.data.get('userId')  # 要修改的用户的id
            user = request.data.get('username')
            pwd = request.data.get('password')
            realName = request.data.get('realName')
            email = request.data.get('email')
            updateUserId = request.user
            updateTime = datetime.datetime.now()

            userInfo = models.UserInfo.objects.get(id=userId)
            userInfo.username = user
            userInfo.password = pwd
            userInfo.realName = realName
            userInfo.email = email
            userInfo.updateTime = updateTime
            userInfo.updateUserId = updateUserId

            if rolesList:
                role = models.Role.objects.filter(id__in=rolesList)
                userInfo.roles.clear()
                userInfo.roles.add(*role)
            if permission:
                permissions = models.Permissions.objects.filter(id__in=permissionList)
                userInfo.permissions.clear()
                userInfo.permissions.add(*permissions)
            userInfo.save()
            rsp['msg'] = '用户信息修改成功'
            rsp['data'] = UserInfoSerializer(userInfo).data
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)

    def delete(self, request, *args, **kwargs):
        rsp = {'code': 200, 'msg': 'ok'}
        userId = request.data.get('userId')  # 要删除的用户的id
        updateUserId = request.user
        updateTime = datetime.datetime.now()

        try:
            userInfo = models.UserInfo.objects.filter(id=userId)
            deleteDic = {
                'updateTime': updateTime,
                'updateUserId': updateUserId,
                'isDelete': True
            }
            userInfo.update(**deleteDic)
            rsp['msg'] = '用户成功删除'
        except Exception as e:
            rsp['code'] = 300
            rsp['msg'] = str(e)
        return Response(rsp)




