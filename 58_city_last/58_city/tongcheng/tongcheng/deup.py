from scrapy.dupefilter import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

"""
1. 根据配置文件找到 DUPEFILTER_CLASS = 'xianglong.deup.MyDupeFilter'
2. 判断是否存在from_settings
    如果有：
        obj = MyDupeFilter.from_settings()
    否则：
        obj = MyDupeFilter()
"""

class MyDupeFilter(BaseDupeFilter):

    def __init__(self):
        self.record = set()

    @classmethod
    def from_settings(cls, settings):
        return cls()

    #:return: True表示已经访问过；False表示未访问过
    def request_seen(self, request):
        ident = request_fingerprint(request)
        if ident in self.record:
            print('已经访问过了', request.url)
            return True
        self.record.add(ident)

    def open(self):  # can return deferred
        pass

    def close(self, reason):  # can return a deferred
        pass