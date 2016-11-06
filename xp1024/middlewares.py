# -*- coding: utf-8 -*-
'''
Created on 2016年11月5日

@author: who8736
'''

# import random
# import urllib2
import logging
import traceback
import urllib

from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import get_meta_refresh
# from scrapy import log
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

logger = logging.getLogger()
# logger.warning("This is a warning")


def get_host(url):
    proto, rest = urllib.splittype(url)
    host, rest = urllib.splithost(rest)
    host, port = urllib.splitport(host)
    return host


class CustomRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        # 跳过成功抓取的页面
        if response.status == 200:
            return response
        url = response.url
        if response.status in [301, 307]:
            #             req = urllib2.Request(url='http://imgs.co/u/16/10/06/JmQo.jpg')
            #             opener = urllib2.build_opener()
            #             reponse = opener.open(req)
            #             return reponse

            #             interval, redirect_url = get_meta_refresh(response)
            #             log.msg('redirect response.body:%s' %
            #                     response.body.extract(), level=log.INFO)
            #             url = request.meta['redirect_urls']
            #             url = 'https:' + url[5:]
            #             log.msg("response redirect_url: %s" % redirect_url, level=log.INFO)
            #             log.msg("request.headers: %s" % repr(request.headers))
            #             log.msg("request.body: %s" % repr(request.body))
            #             log.msg("response.headers: %s" % repr(response.headers))
            #             log.msg("response.request type: %s" %
            #                     type(response.request), level=log.INFO)
            #             log.msg("response type: %s" %
            #                     type(response), level=log.INFO)
            #             request.headers['Accept-Encoding'] = 'identity'
            #             request.headers['Host'] = 'imgs.co'
            #             request.headers['Connection'] = 'close'
            #             del request.headers['Accept-Language']
            #             del request.headers['Accept']
            # #             del request.headers['Cookie']
            #             request.meta['dont_merge_cookies'] = True

            #             """
            #
            #             'Accept-Language': ['en'],
            #             'Accept-Encoding': ['identity'],
            #             'Host': ['imgs.co'],
            #             'Accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'],
            #             'User-Agent': ['Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'], 'Connection': ['close'], 'Referer': ['http://c2.1024mx.org/pw/htm_data/3/1611/470074.html'],
            #             'Cookie': ['__cfduid=dc80e726a73461e3823f2a312eb2b34cd1478357543']
            #             """

            #             log.msg("trying to redirect us: %s" % url, level=log.INFO)
            url = response.headers['Location']
            logger.info("trying to redirect us: %s" % url)
            reason = 'redirect %d' % response.status
#             return response.request
            return self._retry(request, reason, spider) or response
#         else:
#             return response

        # get_meta_refresh方法导致 'Response' object has no attribute 'text'
        # 下段暂时通过try进行包装处理

        try:
            # handle meta redirect
            interval, redirect_url = get_meta_refresh(response)
            if redirect_url:
                #             log.msg("trying to redirect us: %s" % url, level=log.INFO)
                logger.info("trying to redirect us: %s" % url)
                reason = 'meta'
                return self._retry(request, reason, spider) or response
        except Exception, e:
            print 'str(Exception):\t', str(Exception)
            print 'str(e):\t\t', str(e)
            print 'repr(e):\t', repr(e)
            print 'e.message:\t', e.message
            print 'traceback.print_exc():'
            traceback.print_exc()
            print 'traceback.format_exc():\n%s' % traceback.format_exc()

        # test for captcha page
        hxs = HtmlXPathSelector(response)
        captcha = hxs.select(
            ".//input[contains(@id, 'captchacharacters')]").extract()
        if captcha:
            #             log.msg("captcha page %s" % url, level=log.INFO)
            logger.info("captcha page %s" % url)
            reason = 'capcha'
            return self._retry(request, reason, spider) or response
        return response


class ProxyMiddleware(object):
    # overwrite process request

    def process_request(self, request, spider):
        # Set the location of the proxy
        whitelist = []
        url = request.url
        host = get_host(url)
        if host in whitelist:
            #             log.msg("[no proxy]crawl url: %s" % url, level=log.INFO)
            logger.info("[no proxy]crawl url: %s" % url)
            return
#         log.msg("[proxy]crawl url: %s" % url, level=log.INFO)
        logger.info("[proxy]crawl url: %s" % url)
        proxy_ip = 'https://127.0.0.1:8087'
        request.meta['proxy'] = proxy_ip
#         print 'u' * 80


class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        #         ua = random.choice(self.user_agent_list)
        ua = ('Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) '
              'Gecko/20100101 Firefox/49.0')
        if ua:
            # 显示当前使用的useragent
            #             print "********Current UserAgent:%s************" % ua

            # 记录
            #             log.msg('Current UserAgent: ' + ua, level=log.INFO)
            request.headers.setdefault('User-Agent', ua)
#             request.headers.setdefault('Referer',
#                                        'http://c2.1024mx.org/pw/htm_data/3/1611/470074.html')

    # the default user_agent_list composes chrome,I E,
    # firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in
    # http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
         "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"),
        ("Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
         "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"),
        ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
         "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"),
        ("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
         "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"),
        ("Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
         "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"),
        ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
         "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"),
        ("Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
         "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5"),
        ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"),
        ("Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"),
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"),
        ("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"),
        ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"),
        ("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"),
        ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"),
        ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"),
        ("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
         "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3"),
        ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
         "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"),
        ("Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
         "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24")
    ]
