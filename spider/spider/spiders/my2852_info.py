# -*- coding: utf-8 -*-
import scrapy

import requests,traceback
from urllib import parse
from scrapy.selector import Selector



from novels.models import Novel

from ..items import NovelInfospiderItem
from ..help import start_urls,parse_info


from scrapy.utils.project import get_project_settings
settings = get_project_settings()



class My2852InfoSpider(scrapy.Spider):
    name = 'my2852-info'
    allowed_domains = ['www.my2852.com']
    start_urls = start_urls()


    #9 先执行  10 后执行
    custom_settings = {
        "IMAGES_URLS_FIELD": 'cover',
        "UserAgentList": settings['UserAgentList'],
        "ITEM_PIPELINES": {
            'spider.pipelines.NovelImagePipeline': 9,
            'spider.pipelines.NovelInfoSpiderPipeline': 10,
        }
    }

    def parse(self, response):

        try:
            novel_dict = parse_info(response,'柏衣')
            albums=['柏衣小说全集']
            tags=['言情小说']

            novel = Novel.objects.filter(**novel_dict).first()
            if not novel:
                print(f"小说 {novel_dict['name']} 不存在准备入库 {response.url}")
                #novel_dict['title'] = novel_dict['name']
                #novel_dict['keywords'] = novel_dict['name']
                novel_dict['info'] = \
                        response.css(
                            "table.tbw2 .zhj *::text").extract()


                if not novel_dict['info']:
                    novel_dict['info'] = \
                            response.css(
                                "center>table:nth-child(1)>tr>td:nth-child(1) *::text").extract()


                if not novel_dict['info']:
                    novel_dict['info'] = \
                            response.css(
                                "table.tbw2 tr td *::text").extract()


                if not novel_dict['info']:
                    panduan = response.css(
                            "div table>tr:nth-child(3)>td>table>tr:nth-child(1)>td:nth-child(1) table tr:nth-child(1)>td:nth-child(1) a").extract()

                    if not panduan:
                        novel_dict['info']= \
                            response.css(
                                "div table>tr:nth-child(3)>td>table>tr:nth-child(1)>td:nth-child(1) table tr:nth-child(1)>td:nth-child(1) *::text").extract()


                if not novel_dict['info']:
                    panduan=response.css(
                        "div table>tr:nth-child(4)>td>table>tr:nth-child(1)>td:nth-child(1) a").extract()

                    if not panduan:
                        novel_dict['info'] = \
                                response.css(
                                    "div table>tr:nth-child(4)>td>table>tr:nth-child(1)>td:nth-child(1) *::text").extract()

                if not novel_dict['info']:
                    novel_dict['info']= \
                        response.css(
                            "div table.tb5 table.tb5 table.tb6 td *::text").extract()





                novel_dict['info'] = ''.join(novel_dict['info'])
                novel_dict['info'] = novel_dict['info'].strip()

                cover= \
                    response.css(
                        "center>table>tr>td:nth-child(2) img::attr(src)").extract_first("").strip()

                if not cover:
                    cover= \
                        response.css(
                            "table.tbw2 .fmk img::attr(src)").extract_first("").strip()

                if not cover:
                    cover= \
                        response.css(
                            "div table>tr:nth-child(3)>td>table>tr:nth-child(1)>td:nth-child(2) img::attr(src)").extract_first("").strip()


                if not cover:
                    cover= \
                        response.css(
                            "div table.tb5 table.tb5 .td5 img::attr(src)").extract_first("").strip()



                #进入入库部分
                item = NovelInfospiderItem()
                if cover:
                    item['cover'] = [parse.urljoin(response.url, cover)]
                else:
                    item['cover'] = []

                novel_dict['is_machine'] = True

                item['novel'] = novel_dict
                item['albums'] = albums
                item['tags'] = tags
                yield item

            else:
                print(f"小说 {novel_dict['name']} 已经入库 {response.url}")


        except Exception:
            self.logger.error('----------------------------------')
            raise Exception(traceback.format_exc())
