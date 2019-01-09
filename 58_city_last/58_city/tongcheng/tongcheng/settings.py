# -*- coding: utf-8 -*-

# Scrapy settings for tongcheng project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

LOG_FILE = "mySpider.log"
LOG_LEVEL = "INFO"
LOG_ENABLED = True

BOT_NAME = 'tongcheng'

SPIDER_MODULES = ['tongcheng.spiders']
NEWSPIDER_MODULE = 'tongcheng.spiders'

CITY_LIST = [
    'bj', 'sh', 'hz', 'wh', 'tj', 'nj', 'cd', 'gz', 'haikou', 'zjk', 'yinchuan', 'yc', 'xn', 'ganzhou', 'yy',
    'wuhu', 'bh', 'jj', 'yiyang', 'fy', 'zhangzhou', 'cangzhou', 'zhuzhou', 'chengde', 'hu', 'jm', 'zq', 'ha'
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'tongcheng (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

DUPEFILTER_DEBUG = False
# JOBDIR = "C:\\veuvs\\untitled1\\tongcheng\\tongcheng\\jobdir"

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'f=n; userid360_xml=183DE549B1F38F678646F56C3031E267; time_create=1547608278680; commontopbar_new_city_info=2%7C%E4%B8%8A%E6%B5%B7%7Csh; id58=c5/njVv8nJICRzH/Bd2eAg==; 58tj_uuid=d9def37c-8e1f-4023-a30c-5ffb7de97874; als=0; xxzl_deviceid=1q%2FWmAxyDalLHOm5fJ3Ao1HCraB%2BSkLu8ibArbUfU2SiSlhQXwKuORTq9R%2F24nxV; xxzl_smartid=12417b1cf6c2db6b1b9b865ed78c37a2; ppStore_fingerprint=EF3964ABBF8902466FD467D9F60446FCC8DA5927BB627C50%EF%BC%BF1544782946748; new_uv=60; utm_source=; spm=; init_refer=; new_session=0; f=n; city=sh; 58home=sh; commontopbar_new_city_info=2%7C%E4%B8%8A%E6%B5%B7%7Csh; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; JSESSIONID=D7335A45AFC592F4A09F055064E6F49D',
    'pragma': 'no-cache',
    'upgrade-insecure-requests': '1',
    'referer': 'https://sh.58.com/?PGTID=0d000000-0000-09fa-a3e1-6702f422d5ab&ClickID=1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'tongcheng.middlewares.TongchengSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'tongcheng.middlewares.TongchengDownloaderMiddleware': 543,
    'tongcheng.middlewares.UrlFilter': 500,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
   # 'tongcheng.pipelines.TongchengPipeline': 300,
    'tongcheng.pipelines.MysqlPipeline': 302,
    'tongcheng.pipelines.DuplicatesPipeline': 301,
}
IMAGES_STORE = 'E:\Tm\images'
DOWNLOAD_DELAY = 0.3

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# DUPEFILTER_CLASS = 'tongcheng.deup.MyDupeFilter'

# 连接数据库
MYSQL_HOST = "39.107.72.229"
MYSQL_PROT = 3306
MYSQL_DBNAME = "canyin"
MYSQL_USER = "root"
MYSQL_PASSWD = "cater2018Web"

# 本地mysql
# MYSQL_HOST = "127.0.0.1"
# MYSQL_PROT = 3306
# MYSQL_DBNAME = "text"
# MYSQL_USER = "root"
# MYSQL_PASSWD = "962464zsq"

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
# REDIS_DBNAME = 'a'
REDIS_KEY = 'scrapy'
REDIS_PASSWORD = 123456

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 302]

# 代理池数量界定
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 20
# 获取周期
CETTER_CYCLE = 300

# 测试API
TEST_URL = 'https://bj.58.com/'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555
