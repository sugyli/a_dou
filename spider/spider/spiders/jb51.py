# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Jb51Spider(CrawlSpider):
    name = 'jb51'
    allowed_domains = ['www.jb51.net']
    start = 0
    start_urls = ['https://www.jb51.net/list/list_3_1.htm']

    rules = (
        Rule(LinkExtractor(allow=r'article/\d+\.htm'), callback='parse_list', follow=False),
    )


    def parse_list(self, response):
        print('sss')
        yield scrapy.Request(response.url
                             , callback=self.parse_item
                             , dont_filter=False)






    def parse_item(self, response):
        print('22')
        self.start += 1

        print(self.start,response.url)

        return
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
