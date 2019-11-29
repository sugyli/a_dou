# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelInfospiderItem(scrapy.Item):
    cover = scrapy.Field()
    novel = scrapy.Field()
    albums = scrapy.Field()
    tags = scrapy.Field()


class ArticlespiderItem(scrapy.Item):
    cover = scrapy.Field()
    article = scrapy.Field()
    categorys = scrapy.Field()

class BigDbSpiderItem(scrapy.Item):
    images = scrapy.Field()
    bigdb = scrapy.Field()
    category = scrapy.Field()
    rep =  scrapy.Field()
    image_headers = scrapy.Field()
    image_prefix=scrapy.Field()
