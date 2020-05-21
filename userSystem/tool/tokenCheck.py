from userSystem.cache.datacache import DataCache2
from rest_framework import exceptions


class Authtication(object):

    def authenticate(self, request):
        token = request._request.GET.get('token')
        cacheTool = DataCache2(cacheName='user_token_cache', timeout=60 * 60 * 24)
        token_obj = cacheTool.getCache(key=token)
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return (token_obj.id, token_obj)
        # return (token_obj['user'], token_obj)

    def authenticate_header(self, request):
        pass
