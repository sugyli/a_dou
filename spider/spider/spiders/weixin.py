# -*- coding: utf-8 -*-
import scrapy,traceback,copy


from api import WechatSogouAPI



from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class WeixinSpider(scrapy.Spider):
    name = 'weixin'


    headers = {
        "HOST": "weixin.sogou.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
    }

    #9 先执行  10 后执行
    custom_settings = {
        "IMAGES_URLS_FIELD": 'images',
        "UserAgentList": settings['UserAgentList'],
        # "ITEM_PIPELINES": {
        #     'spider.pipelines.ArticleImagePipeline': 9,
        #     'spider.pipelines.ArticleSpiderPipeline': 10,
        # }
    }

    def start_requests(self):
        try:
            parameter=[
                {
                    'url1': 'https://weixin.sogou.com/pcindex/pc/pc_10/pc_10.html',
                    'url2': 'https://weixin.sogou.com/pcindex/pc/pc_10/@@@@@@.html',
                    'category': '育儿',
                    'num': 10
                }
            ]
            for row in parameter:
                for i in range(row['num']):
                    if i == 0:
                        url=row['url1']
                    else:
                        url=row['url2'].replace('@@@@@@',str(i))

                    headers=copy.deepcopy(self.headers)
                    headers['Referer']='https://weixin.sogou.com/'
                    yield scrapy.Request(url
                                        , meta={
                                                'category':row['category'],
                                            }
                                        , headers = headers
                                        , callback=self.parse_list)



        except Exception:
            raise Exception('start_requests 开头', traceback.format_exc())


    def parse_list(self, response):
        try:
            category=response.meta.get("category")





        except Exception:
            raise Exception('parse_list 开头', traceback.format_exc())
        print(response.url)



    # def parse(self, response):
    #     ws_api = WechatSogouAPI()
    #     res = ws_api.get_article_content(
    #         'https://mp.weixin.qq.com/s?src=3&timestamp=1568816146&ver=1&signature=gqWYbEzogdm0djogoXttRSFUYci51XD0vys-JDC-lXsJMlHsaEoAFk9SN609vtwq4vDKp*F1m4da*HpTbaHBdlIDK4FxeHo*OmLLCyk7lrV09dDULZTyChFmad*ZeMV-dW1XalhMt**ie0tfiQMtbm1BMpLLh8V7J4tvEjMfvxg=')
    #
    #     # 进入入库部分
    #     item = ArticlespiderItem()
    #     cover = res['content_img_list']
    #     if cover:
    #         item['cover'] = cover
    #     else:
    #         item['cover']=[]
    #
    #     item['content']=res['content_html']
    #     yield item







