# -*- coding: utf-8 -*-
import scrapy,traceback,json,emoji,html
import  logging
logger = logging.getLogger(__name__)

import helpers,re
from bigdbs.models import BigDb
from ..items import BigDbSpiderItem

from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class A360docSpider(scrapy.Spider):
    name = '360doc'
    #allowed_domains = ['www.360doc.com','www.360doc.cn','image109.360doc.cn']

    headers = {
        "HOST": "www.360doc.com",
        "Referer": "http://www.360doc.com/index.html",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
    }

    wapheaders = {
        "HOST": "www.360doc.cn",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
    }


    #9 先执行  10 后执行
    custom_settings = {
        "IMAGES_URLS_FIELD": 'images',
        "UserAgentList": settings['UserAgentList'],
        "ITEM_PIPELINES": {
            'spider.pipelines.BigDbImagePipeline': 9,
            'spider.pipelines.BigDbSpiderPipeline': 10,
        }
    }
    noneedurl=[
        'http://www.360doc.cn/article/14020892_871182943.html',
        'http://www.360doc.cn/article/54623748_871222082.html',
        'http://www.360doc.cn/article/28625038_871239766.html'
    ]

    def start_requests(self):
        try:
            parameter = [
                {
                    'url':'http://www.360doc.com/ajax/ReadingRoom/getZCData.json?artNum=20&classId=10&subClassId=0&iIscream=0&iSort=1&nPage=@@@@@&nType=11',
                    'category': '教育',
                    'num': 30
                },
                {
                    'url':'http://www.360doc.com/ajax/ReadingRoom/getZCData.json?artNum=20&classId=6&subClassId=0&iIscream=0&iSort=1&nPage=@@@@@&nType=11',
                    'category': '健康',
                    'num': 30
                },
                {
                    'url':'http://www.360doc.com/ajax/ReadingRoom/getZCData.json?artNum=20&classId=7&subClassId=0&iIscream=0&iSort=1&nPage=@@@@@&nType=11',
                    'category': '文化',
                    'num': 30
                },
                {
                    'url': 'http://www.360doc.com/ajax/ReadingRoom/getZCData.json?artNum=20&classId=9&subClassId=0&iIscream=0&iSort=1&nPage=@@@@@&nType=11',
                    'category': '社会',
                    'num': 30
                },
                {
                    'url': 'http://www.360doc.com/ajax/ReadingRoom/getZCData.json?artNum=20&classId=163&subClassId=0&iIscream=0&iSort=1&nPage=@@@@@&nType=11',
                    'category': '人生',
                    'num': 30
                },
                {
                    'url': 'http://www.360doc.com/ajax/ReadingRoom/getZCData.json?artNum=20&classId=2&subClassId=0&iIscream=0&iSort=1&nPage=@@@@@&nType=11',
                    'category': '生活',
                    'num': 30
                },
                {
                    'url': 'http://www.360doc.com/ajax/ReadingRoom/getZCData.json?artNum=20&classId=3&subClassId=0&iIscream=0&iSort=1&nPage=@@@@@&nType=11',
                    'category': '职场',
                    'num': 30
                },
                {
                    'url': 'http://www.360doc.com/ajax/ReadingRoom/getZCData.json?artNum=20&classId=440&subClassId=0&iIscream=0&iSort=1&nPage=@@@@@&nType=11',
                    'category': '财经',
                    'num': 30
                },
                {
                    'url': 'http://www.360doc.com/ajax/ReadingRoom/getZCData.json?artNum=20&classId=5&subClassId=0&iIscream=0&iSort=1&nPage=@@@@@&nType=11',
                    'category': '娱乐',
                    'num': 30
                }
            ]

            for row in parameter:
                for i in range(1, row['num']):
                    url =row['url'].replace('@@@@@',str(i))

                    yield scrapy.Request(url
                                        , meta={
                                                'category':row['category']
                                            }
                                        , headers=self.headers
                                        , callback=self.parse_list)
        except Exception:
            raise Exception('start_requests 开头',traceback.format_exc())


    def parse_list(self, response):
        try:
            category=response.meta.get("category")
            if response.status ==200:
                rs=json.loads(response.body.decode('utf-8'))
                if len(rs) > 0:
                    for row in rs[0]['data']:
                        name = row['StrArtidetitle']
                        weburl = row['StrUrl']
                        urllist = weburl.split('/')
                        wapurl = 'http://www.360doc.cn/article/{}'.format(urllist[-1].replace("shtml", "html"))

                        if wapurl not in self.noneedurl:
                            obj = BigDb.objects.filter(norm=wapurl)
                            if not obj:
                                yield scrapy.Request(wapurl
                                                     , meta={
                                                            "norm": wapurl,
                                                            "name": name,
                                                            "category":category
                                                         }
                                                     , headers=self.wapheaders
                                                     , callback=self.parse)

                            else:
                                print(f"{name} 已经存在不添加")
                        else:
                            print(f"{wapurl} 设置不采集")
            else:
                logger.error(f"出错来源 {response.url} 请求失败 状态码 {response.status}")
        except Exception:
            raise Exception('parse_list 开头',traceback.format_exc())

    def parse(self, response):
        """
            tempstr = "hello you hello python are you ok"
            import re
            rex = r'(hello|Use)'
            print re.sub(rex,"Bye",tempstr)
        """

        try:
            rep_image = "%%%%%%%%%%"
            rep_p = "$$$$$$p$$$$$$"
            rep_endp="$$$$$$endp$$$$$$"
            htmlstr = response.css('#artcontentdiv').extract()[0]

            images  = response.css('#artcontentdiv img::attr(src)').extract()

            rex = r"""(<img\s.*?\s?src\s*=\s*['|"]?[^\s'"]+.*?>)"""
            #new_text, n = re.subn 替换的次数
            htmlstr = re.sub(rex, rep_image, htmlstr)
            #替换p 标签
            rex_p = r"""(<\s*p[^>]*>)"""
            htmlstr=re.sub(rex_p, rep_p, htmlstr)

            rex_endp=r"""(<\s*/\s*p\s*>)"""
            htmlstr=re.sub(rex_endp, rep_endp, htmlstr)

            #过滤
            htmlstr=htmlstr\
                .replace('\r', '')\
                .replace('\t', '')\
                .replace('\n', '')
            #过滤空格
            re_stopwords=re.compile('\u3000', re.I)
            htmlstr=re_stopwords.sub('', htmlstr)
            re_stopwords2=re.compile('\xa0', re.I)
            htmlstr=re_stopwords2.sub('', htmlstr)
            #过滤垃圾
            re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)  # Script
            re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)  # style
            re_a=re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>', re.I)  # a
            htmlstr=re_script.sub('', htmlstr)
            htmlstr=re_style.sub('', htmlstr)
            htmlstr=re_a.sub('', htmlstr)
            #过滤HTML
            htmlstr = helpers.strip_tags(htmlstr)
            #转译emoji
            htmlstr=emoji.demojize(htmlstr)
            # 过滤空格
            htmlstr=htmlstr.replace(' ', '')
            # 遗漏的HTML转义
            htmlstr=html.unescape(htmlstr)
            htmlstr=html.escape(htmlstr)

            item = BigDbSpiderItem()
            item['images'] = images
            item['bigdb'] = {
                'name': response.meta.get("name"),
                'norm': response.meta.get("norm"),
                'content': htmlstr,
                'normslug': '360doc',
                'status': 'P'
            }
            item['category'] = response.meta.get("category")
            item['rep'] = {
                'rep_image':rep_image,
                'rep_p': rep_p,
                'rep_endp': rep_endp
            }

            yield item


        except Exception:
            raise Exception('parse 开头',traceback.format_exc())

