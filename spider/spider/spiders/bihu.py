# -*- coding: utf-8 -*-
import scrapy
import json,traceback,re,emoji
from urllib import parse

from articles.models import Article
from quanbenxiaoshuo import helpers
from ..items import ArticlespiderItem
from scrapy.selector import Selector
from django.db.models import Q


from scrapy.utils.project import get_project_settings
settings = get_project_settings()

"""
datas=json.dumps(response.text, ensure_ascii=False, indent=4, separators=(',',': '))
json_data=json.loads(datas).encode('utf-8').decode('unicode_escape')
print(json_data)
"""


class BihuSpider(scrapy.Spider):
    name = 'bihu'
    allowed_domains = ['bihu.com','be02.bihu.com','oss02.bihu.com']

    #start_urls = ['https://bihu.com/']
    headers={
        'Content-Type': 'application/json;'
    }
    #9 先执行  10 后执行
    custom_settings = {
        "IMAGES_URLS_FIELD": 'cover',
        "UserAgentList": settings['UserAgentList'],
        "ITEM_PIPELINES": {
            'spider.pipelines.ArticleImagePipeline': 9,
            'spider.pipelines.ArticleSpiderPipeline': 10,
        }
    }


    def start_requests(self):
        try:
            url = 'https://be02.bihu.com/bihube-pc/api/content/show/hotArtList'
            for x in range(1,30):

                data={"pageNum":str(x),"version":""}
                # yield scrapy.FormRequest(url, method = 'POST', headers = headers, body=json.dumps(data), callback = self.parse_list, dont_filter = True)
                #重复爬取的地址需要设置 dont_filter = True

                yield scrapy.FormRequest(url
                                         , method='POST'
                                         , headers=self.headers
                                         , body=json.dumps(data)
                                         , callback=self.parse_list
                                         , dont_filter = False)
        except Exception:
            raise Exception(traceback.format_exc())

    def parse_list(self, response):
        try:
            url='https://be02.bihu.com/bihube-pc/api/content/show/getArticle2?secret='
            # 返回的是json数据
            # 转换为python中的字典
            rs=json.loads(response.body.decode('utf-8'))
            if rs.get('resMsg')=='success':
                for row in rs['data']['list']:
                    #查询数据库有无此文章
                    name = row['title'].strip()

                    obj = Article.objects.filter(Q(name=name)|Q(norm=str(row['id']))).first()

                    if not obj:

                        data={"artId": row['id']}
                        #data={"artId": '1887485021'}
                        yield scrapy.FormRequest(url
                                                 , method='POST'
                                                 , meta={"norm": row['id']}
                                                 , headers=self.headers
                                                 , body=json.dumps(data)
                                                 , callback=self.parse
                                                 , dont_filter=False)
                    else:
                        print(f"{name} 已经存在不添加")

            else:
                raise Exception("parse_list 请求数据有问题")

        except Exception:

            raise Exception(traceback.format_exc())




    def parse(self, response):
        try:
            norm=response.meta.get("norm")
            article = {}
            article['norm'] = norm
            rs=json.loads(response.body.decode('utf-8'))

            if rs.get('resMsg')=='success':
                url = parse.urljoin('https://oss02.bihu.com', rs['data']['content'])
                #url = 'https://oss02.bihu.com/article/2019/0930/1_1569795606094_U0z8YfrY.txt'
                article['name']=rs['data']['title'].strip()
                article['description'] = helpers.descriptionreplace(rs['data']['brief'])
                article['keywords'] = rs['data']['keywords']
                article['status']= 'P'

                yield scrapy.Request(url
                                     , meta={"article": article}
                                     , headers=self.headers
                                     , callback=self.content_parse
                                     , dont_filter=False)

            else:
                raise Exception("parse 请求数据有问题")


        except Exception:
            raise Exception(traceback.format_exc())

    def content_parse(self, response):
        try:
            content=response.body.decode('utf-8')
            article=response.meta.get("article")
            content = \
                content.replace('<p></p>', '')\
                    .replace('<section style=\"\"><img src=\"\" style=\"display: block;\"></section>','')\
                    .replace('<p><br></p>','')


            re_div1 = re.compile('<\s*div[^>]*>',re.I)
            re_div2 = re.compile('<\s*/\s*div\s*>', re.I)

            re_a1=re.compile('<\s*a[^>]*>', re.I)
            re_a2=re.compile('<\s*/\s*a\s*>', re.I)



            content = re_div1.sub('', content)
            content = re_div2.sub('', content)
            content = re_a1.sub('', content)
            content = re_a2.sub('', content)


            content=emoji.demojize(content)
            article['content'] = content
            selector=Selector(text=article['content'])
            cover = selector.css("img::attr(src)").extract()
            cover = [i for i in cover if i.strip()]


            # 进入入库部分
            item = ArticlespiderItem()
            item['article']=article
            item['cover']=cover
            item['categorys']=['区块链']
            yield item

        except Exception:
            raise Exception(traceback.format_exc())
