# -*- coding: utf-8 -*-
import scrapy
import os
import codecs
import traceback
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

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from xp1024.settings import TESTFLAG, TESTPAGECODE, CRAWLDOWNLOADED


def convert_html(html, subpath):
    """将html中img标签的src属性改为本地链接"""
#     soup = BeautifulSoup(html, 'lxml')
    # save_item_page函数中使用BeautifulSoup解析网页时，传入本函数的参数类型是Tag,可直接赋值给soup进行处理
    soup = html
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
    name = 'xp1024'
#     allowed_domains = ['c2.1024mx.org']
#     start_urls = ['http://c2.1024mx.org/pw/thread.php?fid=3/']
    allowed_domains = ['x2.pix378.net']
    start_urls = ['http://x2.pix378.net/pw/thread.php?fid=3']

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

            item = urlItem()
            item['link'] = sel.xpath('@href').extract()
            baseurl = u'http://c2.1024mx.org/pw/'
            url = urljoin_rfc(baseurl, item['link'][0])
#             print url

#             测试用，仅对一个文件进行分析
            if TESTFLAG and url.find(TESTPAGECODE) < 0:
                continue
            print sel
            print sel.xpath('text()').extract()
            jsonItem = JsonItem()
            try:
                jsonItem['pagetitle'] = sel.xpath('text()').extract()[0]
                jsonItem['pagecode'] = page_code(item['link'][0])
                yield jsonItem
            except IndexError:
                self.logger.warning('fail parse:%s', repr(sel))
            else:
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

    def save_item_page(self, response):
        # 网页主要部分保存到文件
        filename = 'static/html/' + response.url.split('/')[-1]
        self.logger.debug('response charset: %s' % response.encoding)

#         exp = u'//div[contains(@id, "read_tpc")]'
#         exp = u'//div[contains(@id, "read_tpc")]'
#         exp = u'//th[contains(@id, "td_tpc")]'
# #         html = response.xpath(exp).extract()
#         # 改用Selector的方法进行解析
#         sel = Selector(response)
#         html = sel.xpath(exp).extract()
#         html = sel.xpath(u'//div[re:test(@id, "read_tpc")]').extract()

        # 因网页含有空字符（nul）导致原解析方法失败，改用BeautifulSoup解析
        soup = BeautifulSoup(response.body, 'lxml')
        html = soup.find_all(id='td_tpc')
#         print '=' * 80
#         print html
#         print '=' * 80

        if TESTFLAG:
            testfilename = ('static/html/' + 'test' +
                            response.url.split('/')[-1])
            try:
                testfile = codecs.open(testfilename, 'wb', encoding='utf-8')
                #                     response.body = response.body.decode('utf-8')
#                 print '-' * 80
#                 print repr(response.body)
                testfile.write(response.body.decode('utf-8'))
            except Exception, e:
                print 'str(Exception):\t', str(Exception)
                print 'str(e):\t\t', str(e)
                print 'repr(e):\t', repr(e)
                print 'e.message:\t', e.message
                print 'traceback.print_exc():'
                traceback.print_exc()
                print 'traceback.format_exc():\n%s' % traceback.format_exc()
#             print '-' * 80
            testfile.close()

        subpath = response.url.split('/')[-1].split('.')[0]
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
        with codecs.open(filename, 'wb', encoding='utf-8') as f:
            f.write(html)
            f.close()

    def parse_item(self, response):
        self.save_item_page(response)
        item = urlItem()
#         exp = '//div[contains(@id, "read_tpc")]//img/@src'
#         exp = u'//th[contains(@id, "td_tpc")]/div//img/@src'
        #         hxs = Selector(text=response.body)
        # #         detail_url_list = hxs.xpath('//li[@class="good-list"]/@href').extract()
        #         urls = hxs.xpath(exp).extract()
#         urls = response.xpath(exp).extract()
        # 因网页含有空字符（nul）导致原解析方法失败，改用BeautifulSoup解析
        soup = BeautifulSoup(response.body, 'lxml')
        maincontent = soup.find_all(id='td_tpc')[0]
        urls = []
        imgs = maincontent.find_all('img')
        for img in imgs:
            urls.append(img['src'])
        print urls
        undown_url = []
        subpath = response.url.split('/')[-1].split('.')[0]
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


def runscrapy():
    # 方法一
    process = CrawlerProcess(get_project_settings())

    # 'followall' is the name of one of the spiders of the project.
    process.crawl('xp1024')
    # the script will block here until the crawling is finished
    process.start()

# 方法二
#     runner = CrawlerRunner()
#
#     d = runner.crawl(Xp1024spiderSpider)
#     d.addBoth(lambda _: reactor.stop())
# reactor.run()  # the script will block here until the crawling is
# finished


if __name__ == '__main__':
    try:
        runscrapy()
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'repr(e):\t', repr(e)
        print 'e.message:\t', e.message
        print 'traceback.print_exc():'
        traceback.print_exc()
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
