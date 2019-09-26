# -*- coding: utf-8 -*-
import scrapy


from api import WechatSogouAPI
from ..items import ArticlespiderItem


from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class WeixinSpider(scrapy.Spider):
    name = 'weixin'
    allowed_domains = ['weixin.sogou.com']
    start_urls = ['https://mp.weixin.qq.com/s?src=3&timestamp=1568794373&ver=1&signature=gqWYbEzogdm0djogoXttRSFUYci51XD0vys-JDC-lXsJMlHsaEoAFk9SN609vtwq4vDKp*F1m4da*HpTbaHBdlIDK4FxeHo*OmLLCyk7lrV09dDULZTyChFmad*ZeMV-4MMvffMR-fEp5lCSrIReZbR5YIzoVIV7Lx3pmtGlw7g=']


    #9 先执行  10 后执行
    custom_settings = {
        "IMAGES_URLS_FIELD": 'cover',
        "UserAgentList": settings['UserAgentList'],
        "ITEM_PIPELINES": {
            'spider.pipelines.ArticleImagePipeline': 9,
            'spider.pipelines.ArticleSpiderPipeline': 10,
        }
    }



    def parse(self, response):
        ws_api = WechatSogouAPI()
        res = ws_api.get_article_content(
            'https://mp.weixin.qq.com/s?src=3&timestamp=1568816146&ver=1&signature=gqWYbEzogdm0djogoXttRSFUYci51XD0vys-JDC-lXsJMlHsaEoAFk9SN609vtwq4vDKp*F1m4da*HpTbaHBdlIDK4FxeHo*OmLLCyk7lrV09dDULZTyChFmad*ZeMV-dW1XalhMt**ie0tfiQMtbm1BMpLLh8V7J4tvEjMfvxg=')

        # 进入入库部分
        item = ArticlespiderItem()
        cover = res['content_img_list']
        if cover:
            item['cover'] = cover
        else:
            item['cover']=[]

        item['content']=res['content_html']
        yield item







