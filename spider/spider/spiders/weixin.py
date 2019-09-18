# -*- coding: utf-8 -*-
import scrapy


from api import WechatSogouAPI


class WeixinSpider(scrapy.Spider):
    name = 'weixin'
    allowed_domains = ['weixin.sogou.com']
    start_urls = ['https://weixin.sogou.com/']

    def parse(self, response):
        print(response.url)
