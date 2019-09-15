# -*- coding: utf-8 -*-
import scrapy


class Shushu8InfoSpider(scrapy.Spider):
    name = 'shushu8-info'
    allowed_domains = ['www.shushu8.com']
    start_urls = ['http://www.shushu8.com/']

    def parse(self, response):
        pass
