# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import os
# import urllib
import logging

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
# from scrapy import log

# import settings
from items import urlItem, JsonItem

logger = logging.getLogger()


class Xp1024Pipeline(ImagesPipeline):  # 继承ImagesPipeline这个类，实现这个功能

    # 重写ImagesPipeline   get_media_requests方法
    def get_media_requests(self, item, info):
        '''
        :param item:
        :param info:
        :return:
        在工作流程中可以看到，
        管道会得到文件的URL并从项目中下载。
        为了这么做，你需要重写 get_media_requests() 方法，
        并对各个图片URL返回一个Request:
        '''
        print type(item)
        if isinstance(item,  urlItem):
            print type(item)
            image_urls, subpath = item['image_urls']
            for image_url in image_urls:
                print '****', image_url
                yield scrapy.Request(image_url, meta={'subpath': subpath})

    def item_completed(self, results, item, info):
        '''

        :param results:
        :param item:
        :param info:
        :return:
        当一个单独项目中的所有图片请求完成时（要么完成下载，要么因为某种原因下载失败），
         item_completed() 方法将被调用。
        '''
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        image_name = request.url.split('/')[-1]
        subpath = request.meta.get('subpath')
#         print 'subpath: ', subpath
#         if not os.path.exists(subpath):
#             os.makedirs(subpath)
#         image_name = subpath + image_name
#         image_path = request.meta.get('path', request.url.split('/')[-1])
#         print image_name
        logger.info('generate a local image')
        return 'full/%s/%s' % (subpath, image_name)


class SaveJsonPipeline(object):

    def __init__(self):
        #         self.file = codecs.open(
        #             'scraped_data.json', 'rb', encoding='utf-8')
        #         #         target = json.JSONDecoder().decode(self.file)
        #         #         print target
        #         jsonstr = self.file.read()
        # #         jsonstr = open('scraped_data.json', 'rb').read()
        #         print 'jsonstr' * 11
        #         print repr(jsonstr)
        # #         print jsonstr.decode('utf-8')
        #         print isinstance(jsonstr, unicode)
        #         print jsonstr.encode('GBK')
        # #         jsonobject = json.loads()
        # # #         jsonobject = json.loads(file('scraped_data.json'))
        # #         print 'jsonobject' * 10
        # # #         print json.dump(jsonobject)
        # #         print jsonobject
        self.lines = []

        self.file = codecs.open(
            'scraped_data.json', 'a', encoding='utf-8')
        self.page_dict = {}

    def process_item(self, item, spider):
        if isinstance(item, JsonItem):
            # print 'name', item['name']
            # self.page_dict[item['pagecode']] = item['pagetitle']
            # jsonstr = json.dumps(self.page_dict, ensure_ascii=False) + '\n'
            # print '#' * 80
            # print jsonstr.encode('gb18030')

            # line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            # line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            jsonstr = json.dumps(dict(item), ensure_ascii=False) + '\n'
            print 'pipelines_SaveJsonPipeline_process_item'
            print '=' * 80
            print jsonstr.encode('gb18030')
            self.file.write(jsonstr)
        return item

    def spider_closed(self, spider):
        logger.info('spider closed')
        self.file.close()
