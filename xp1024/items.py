# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class urlItem(scrapy.Item):
    # define the fields for your item here like:
    htmlfile = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    image_urls = scrapy.Field()  # 图片的链接
    images = scrapy.Field()
    pass

    def test(self):
        print 'test item import'


class JsonItem(scrapy.Item):
    # define the fields for your item here like:
    pagecode = scrapy.Field()
    pagetitle = scrapy.Field()
