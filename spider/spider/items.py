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
