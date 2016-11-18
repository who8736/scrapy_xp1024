# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

############################################
# 自定义设置区
############################################

# 是否仅抓取一个网页做测试
# TESTFLAG = True
TESTFLAG = False
# 测试时抓取的网页代码，如'470074'， 则抓取'html/470074.html'
TESTPAGECODE = '475407'

# 是否处理已下载过的页面
CRAWLDOWNLOADED = True
# CRAWLDOWNLOADED = False

############################################
# scrapy内置参数设置区
############################################

BOT_NAME = 'xp1024'

SPIDER_MODULES = ['xp1024.spiders']
NEWSPIDER_MODULE = 'xp1024.spiders'
ITEM_PIPELINES = {
    'xp1024.pipelines.Xp1024Pipeline': 100,
    'xp1024.pipelines.SaveJsonPipeline': 40,

}
# ITEM_PIPELINES = {'tutorial.pipelines.ImagesPipeline': 1}
IMAGES_STORE = 'static/img'
DOWNLOAD_DELAY = 1

# IMAGES_THUMBS = {  # 缩略图的尺寸，设置这个值就会产生缩略图
#     'small': (50, 50),
#     'big': (200, 200),
# }

DOWNLOADER_MIDDLEWARES = {
    #     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'xp1024.middlewares.ProxyMiddleware': 100,
    'xp1024.middlewares.CustomRetryMiddleware': 120,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
    'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': None,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'xp1024.middlewares.RotateUserAgentMiddleware': 10
}

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'xp1024.log'

RETRY_ENABLED = True
RETRY_TIMES = 3

REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 3

DOWNLOAD_TIMEOUT = 15
