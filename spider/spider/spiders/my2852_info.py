# -*- coding: utf-8 -*-
import scrapy


import requests,traceback
from urllib import parse
from scrapy.selector import Selector



from novels.models import Novel
from ..items import NovelInfospiderItem


from scrapy.utils.project import get_project_settings
settings = get_project_settings()


def start_urls():
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    res = requests.get("http://www.my2852.com/wuxia/gulong/index.htm", headers=headers)
    if res.status_code == 200:
        selector=Selector(text=res.content.decode('gbk','ignore'))
        all_href = selector.css(".jz table a::attr(href)").extract()
        all_href =  list(set(all_href))
        full_all_href = []
        for href in all_href:
            full_all_href.append(parse.urljoin('http://www.my2852.com/wuxia/gulong/index.htm', href))
        return full_all_href
    else:
        raise Exception('start_urls 方法 网络请求失败')

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
            novel_dict={}

            novel_dict['name']=\
                response.css(
                    "table .tdw::text").extract()[0].strip()

            novel_dict['author']= \
                response.css(
                    "table .tdw2::text").extract()[0].replace('作者：'
                                                              ,'').strip()

            novel = Novel.objects.filter(**novel_dict).first()


            if not novel:
                print(f"小说 {novel_dict['name']} 不存在准备入库 {response.url}")
                novel_dict['title'] = novel_dict['name']
                novel_dict['keywords'] = novel_dict['name']
                novel_dict['info'] = \
                        response.css(
                            "table.tbw2 .zhj *::text").extract()

                novel_dict['info'] = ''.join(novel_dict['info'])


                #进入入库部分
                item = NovelInfospiderItem()
                cover = \
                    response.css(
                        "table.tbw2 .fmk img::attr(src)").extract()[0].strip()

                item['cover'] = [parse.urljoin(response.url, cover)]
                item['novel'] = novel_dict
                yield item

            else:
                print(f"小说 {novel_dict['name']} 已经入库 {response.url}")


        except Exception:
            self.logger.error(response.url+' 出错地址')
            raise Exception(traceback.format_exc())
