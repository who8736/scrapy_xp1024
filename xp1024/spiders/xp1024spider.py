# -*- coding: utf-8 -*-
import scrapy
import os
import codecs
# import json
# import unicode
from xp1024.items import urlItem, JsonItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import responsetypes
from scrapy import Selector
from scrapy.utils.url import urljoin_rfc
# from scrapy.crawler import CrawlerProcess
# from scrapy import log
from bs4 import BeautifulSoup

from xp1024.settings import TESTFLAG, TESTPAGECODE, CRAWLDOWNLOADED


def convert_html(html, subpath):
    """将html中img标签的src属性改为本地链接"""
    soup = BeautifulSoup(html, 'lxml')
#     print '=' * 80
    for img in soup.findAll('img'):
        src = img['src']
        filename = '../img/full/%s/%s' % (subpath, src.split('/')[-1])
#         print src
#         print filename
        img['src'] = filename
#     print soup
    return soup.prettify()


def repl_fun(matched):
    filename = matched.split('/')[-1]
    return '../img/full/%s' % filename


def page_code(page_url):
    return page_url.split('/')[-1].split('.')[0]


class Xp1024spiderSpider(scrapy.Spider):
    # class Xp1024Spider(CrawlSpider):
    name = "xp1024"
    allowed_domains = ["c2.1024mx.org"]
    start_urls = ['http://c2.1024mx.org/pw/thread.php?fid=3/']

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接
        # 没有callback意味着follow默认为True
        Rule(LinkExtractor(allow=('category\.php', ),
                           deny=('subsection\.php', ))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        #         Rule(LinkExtractor(allow=('htm_data/3/1610/466125\.html', )),
        #              callback='parse_item'),
        Rule(LinkExtractor(allow=('\thread\.php', )),
             callback='parse_item'),
        Rule(LinkExtractor(allow=('\d{6}\.html', )),
             callback='parse_item'),
        #         Rule(LinkExtractor(allow=('\d{6}\.html', )),
        #              callback='parse_item'),
    )

    def parse(self, response):
        """分析start_urls指向的页面，保存该页面"""
        filename = 'xp1024test.html'

        with open(filename, 'wb') as f:
            f.write(response.body)

        for sel in response.xpath('//h3/a[contains(@href, "htm_data")]'):

            jsonItem = JsonItem()
            item = urlItem()
            item['link'] = sel.xpath('@href').extract()
            #             print sel
            #             item = urlItem()

            jsonItem['pagetitle'] = sel.xpath('text()').extract()[0]
            jsonItem['pagecode'] = page_code(item['link'][0])
            yield jsonItem
#             print jsonItem['name'], jsonItem['htmlfile']

            baseurl = u'http://c2.1024mx.org/pw/'
#             url = [urljoin_rfc(baseurl, u) for u in item['link']]
            url = urljoin_rfc(baseurl, item['link'][0])
#             print url

#             测试用，仅对一个文件进行分析
#             print url.find('468932')
            if TESTFLAG and url.find('470074') < 0:
                continue

            # 已保存的文件不再处理
            filename = './html/' + url.split('/')[-1]
            if CRAWLDOWNLOADED and os.path.isfile(filename):
                continue

            yield scrapy.Request(url, callback=self.parse_item)
#             yield item
#         return item

#     def parse_main(self, response):
#         filename = 'xp1024test.html'
#         with open(filename, 'wb') as f:
#             f.write(response.body)

    def parse_item(self, response):
        #         print response.url
        #         print '=================================='
        #         filename = 'xp1024test.html'

        # 网页主要部分保存到文件
        filename = 'static/html/' + response.url.split('/')[-1]
        subpath = response.url.split('/')[-1].split('.')[0]
        with codecs.open(filename, 'wb', encoding='utf-8') as f:
            exp = '//div[contains(@id, "read_tpc")]'
            html = response.xpath(exp).extract()
            html = convert_html(html[0], subpath)
            html = """
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
            <meta http-equiv="Content-Type" content="text/html;
            charset=utf-8">
            </head>""" + html + '</html>'


#             html = unicode.encode(html[0], 'utf-8')
#             print '-' * 33
#             print repr(html[0].decode('unicode_escape'))
            self.logger.info('save html file: %s' % filename)
            f.write(html)
            f.close()
#             f.write(response.body)

#         for img in response.xpath('//div[contains(@id, "read_tpc")]'
#                                   '//img//@src').extract():
            #             print '-' * 20
            #             url = sel.xpath('@src').extract()
            #             print imgurl
#
#             print img
#             item = urlItem()
# #             item['image_urls'] = img.xpath('/img/@src').extract()
#             item['image_urls'] = [img]
# #             print item['image_urls']
#             yield item
#             item.test()
#             print '-' * 20

#             item = picItem()
#             item['name'] = sel.xpath('src').extract()
#             item['link'] = sel.xpath('a/@href').extract()

# ==========================================
        item = urlItem()
        exp = '//div[contains(@id, "read_tpc")]//img/@src'
#         hxs = Selector(text=response.body)
# #         detail_url_list = hxs.xpath('//li[@class="good-list"]/@href').extract()
#         urls = hxs.xpath(exp).extract()
        urls = response.xpath(exp).extract()
        undown_url = []
        for url in urls:
            image_name = 'img/full/%s/%s' % (subpath, url.split('/')[-1])
            if not os.path.isfile(image_name):
                undown_url.append(url)
        if undown_url:
            item['image_urls'] = (undown_url, subpath)
#             print item['image_urls']
#             print '1' * 80
#             print type(item)
#             print item
#
            yield item  # 注释这行，暂不下载图片

    def close(self):
        self.logger.info('Xp1024spiderSpider close')
