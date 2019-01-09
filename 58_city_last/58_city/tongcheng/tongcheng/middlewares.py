# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pymysql
import redis

from scrapy import signals
from scrapy import http
from scrapy.conf import settings
from tongcheng.proxy_start import get_proxy

# 去重中间件没加到配置中
class TongchengSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TongchengDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # proxy = get_proxy()
        # request.meta['proxy'] ="http://" + proxy

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UrlFilter(object):
        # 初始化过滤器（使用mysql过滤）
        # def __init__(self):
        #     self.settings = settings
        #     self.client_mysql = pymysql.connect(
        #         host=self.settings.get('MYSQL_HOST'),
        #         port= self.settings.get('MYSQL_PROT'),
        #         db=self.settings.get('MYSQL_DBNAME'),
        #         user=self.settings.get('MYSQL_USER'),
        #         passwd=self.settings.get('MYSQL_PASSWD'),
        #         charset='utf8',
        #         use_unicode=True)
        #     self.curser_redis = redis.Redis(
        #         host=settings.REDIS_HOST,
        #         port=settings.REDIS_PORT,
            #     db=settings/.REDIS_DBNAME
            # )
            # self.redis_key = settings.REDIS_KEY
            # self.curser = self.client_mysql.cursor()

        def process_request(self, request, spider):
            # # 获取数据库中的url，并且将url进行对比
            # self.curser.execute("""SELECT sort_id FROM shop_detail where sort_id={}""".format(request.url))
            # # 获取数据内容
            # url_list = self.curser.fetchall()
            # if not url_list:
            #     return
            # url_list = [i[0] for i in url_list]
            # # 我用列表做的判断，数据量特别大的时候就会出现速度降低的情况，可酌情修改
            # if request.url in url_list:
            #     # 在其中则表示数据重复，直接返回None
            #     return http.Response(url=request.url, body=None)
            # return None
            pass

        # def process_response(self, response, spider):
        #     pass