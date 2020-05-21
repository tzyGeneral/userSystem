from django.core.cache import caches


class DataCache2:

    def __init__(self, cacheName='default', timeout=60*60):
        self.cache = caches[cacheName]
        self.timeout = timeout

    def cleanKeyStr(self, key: str):
        """
        清理key的不规则写法导致存入缓存失败
        :param key:
        :return:
        """
        key = str(key).replace(' ', '').strip()
        return key

    def setCache(self, key: str, value):
        """
        设置一个缓存
        :param key:
        :param value:
        :return:
        """
        key = self.cleanKeyStr(key)
        self.cache.set(key, value, self.timeout)
        return key

    def getCache(self, key: str):
        """
        获取一个缓存
        :param key:
        :param value:
        :return:
        """
        key = self.cleanKeyStr(key)
        result = self.cache.get(key)
        return result

    def checkKey(self, key: str):
        """
        判断是否存在一个键
        :param key:
        :return:
        """
        key = self.cleanKeyStr(key)
        return self.cache.has_key(key)


