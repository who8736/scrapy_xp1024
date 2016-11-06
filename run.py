# -*- coding: utf-8 -*-
'''
Created on 2016年11月1日

@author: who8736
'''
from xp1024.spiders.xp1024spider import Xp1024spiderSpider
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

'''
# scrapy api
# from scrapy import signals, log
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings


def spider_closing(spider):
    """Activates on spider closed signal"""
#     log.msg("Closing reactor", level=log.INFO)
    reactor.stop()

# log.start(loglevel=log.DEBUG)
settings = Settings()

# crawl responsibly
settings.set('USER_AGENT',
             ('Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36'
              '(KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'))
crawler = Crawler(settings)

# stop reactor when spider closes
crawler.signals.connect(spider_closing, signal=signals.spider_closed)

crawler.configure()
crawler.crawl(Xp1024Spider())
crawler.start()
reactor.run()
'''


configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(Xp1024spiderSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()  # the script will block here until the crawling is finished
