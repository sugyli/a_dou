# -*- coding: utf-8 -*-
import scrapy,traceback,json,emoji,html,copy
import logging
logger = logging.getLogger(__name__)
from urllib import parse

import helpers,re
from bigdbs.models import BigDb
from ..items import BigDbSpiderItem
from .. import help

from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class A360docSpider(scrapy.Spider):
    name = '360doc'
    #allowed_domains = ['www.360doc.com','www.360doc.cn','image109.360doc.cn']

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
        'http://www.360doc.cn/article/28625038_871239766.html',
        'http://www.360doc.cn/article/273090_240724762.html',
        'http://www.360doc.cn/article/52901360_871157169.html',
        'http://www.360doc.cn/article/6748870_871057964.html',
        'http://www.360doc.cn/article/1427138_873834882.html',
        'http://www.360doc.cn/article/10813888_870045548.html',
        'http://www.360doc.cn/article/34614342_760046274.html'
    ]

    def start_requests(self):

        try:
            parameter = [

                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '社会',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1',
                        'classid': '9',
                        'subclassid': '0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '文化',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1',
                        'classid': '7',
                        'subclassid': '0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '人生',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1',
                        'classid': '163',
                        'subclassid': '0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '生活',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1',
                        'classid': '2',
                        'subclassid': '0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '健康',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1',
                        'classid': '6',
                        'subclassid': '0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '教育',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1',
                        'classid': '10',
                        'subclassid': '0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '职场',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1',
                        'classid': '3',
                        'subclassid': '0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '财经',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1',
                        'classid': '440',
                        'subclassid': '0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '娱乐',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1',
                        'classid': '5',
                        'subclassid': '0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '艺术',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1',
                        'classid': '1',
                        'subclassid': '0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getReadRooms.ashx',
                    'category': '上网',
                    'num': 30,
                    'data': {
                        'topnum':'20',
                        'pagenum':'1',
                        'classid':'12',
                        'subclassid':'0'
                    }
                },
                {
                    'url': 'http://www.360doc.cn/ajax/index/getOriginal.ashx',
                    'category': '综合',
                    'num': 30,
                    'data': {
                        'topnum': '20',
                        'pagenum': '1'
                    }
                }

            ]

            for row in parameter:
                for i in range(1, row['num']):
                    # url =row['url'].replace('@@@@@',str(i))
                    #
                    # if row['type'] == 'web':
                    #     yield scrapy.Request(url
                    #                         , meta={
                    #                                 'category':row['category'],
                    #                                 'type': row['type']
                    #                             }
                    #                         , headers=self.headers
                    #                         , callback=self.parse_list)
                    #

                    headers = copy.deepcopy(self.wapheaders)
                    headers['Origin'] = 'http://www.360doc.cn'
                    headers['Referer']='http://www.360doc.cn/index.html?classid=13&subclassid=0'
                    headers['X-Requested-With']='XMLHttpRequest'
                    headers['Content-Type']='application/x-www-form-urlencoded; charset=UTF-8'
                    row['data']['pagenum'] = str(i)
                    yield scrapy.FormRequest(row['url']
                                             , method='POST'
                                             , meta={
                                                    'category': row['category'],
                                                }
                                             , headers=headers
                                             #, body=json.dumps(row['data'])
                                             , formdata=row['data']
                                             , callback=self.parse_list)

        except Exception:
            raise Exception('start_requests 开头',traceback.format_exc())

    #从列表中获取到了内容地址 这个位置可以调试
    def parse_list(self, response):
        try:
            category=response.meta.get("category")

            if response.status ==200:
                rs=json.loads(response.body.decode('utf-8'))
                if len(rs['data'])>0:
                    for row in rs['data']:
                        name = row['articletitle']
                        wapurl = row['arttitleurl']
                        if wapurl not in self.noneedurl:
                            obj=BigDb.objects.filter(norm=wapurl)
                            if not obj:
                                yield scrapy.Request('http://www.360doc.cn/article/66088856_872433994.html'
                                                     , meta={
                                                            "norm": wapurl,
                                                            "name": name,
                                                            "category": category
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

            htmlstr = response.css('#artcontentdiv').extract()[0]
            compile_br = re.compile(r'<\s*br[^>]*>', re.I)
            htmllist = compile_br.split(htmlstr)

            if len(htmllist)>1:
                htmlstr = \
                    ''.join(['<p>{}</p>'.format(s) for s in htmllist if s.strip()])


            images  = response.css('#artcontentdiv img::attr(src)').extract()
            #检查图片地址完整
            for i in range(len(images)):
                if not re.match(r'^https?:/{2}\w.+$', images[i]):
                    images[i] = parse.urljoin(response.url,images[i])

            rep_image="%%%%%%%%%%"
            rex=r"""(<img\s.*?\s?src\s*=\s*['|"]?[^\s'"]+.*?>)"""
            # 这么写的目的是不区分大小
            compile_img=re.compile(rex, re.I)
            htmlstr=compile_img.sub(rep_image, htmlstr)

            htmlstr = help.handle_content(htmlstr)

            if htmlstr or len(images) > 0:
                item = BigDbSpiderItem()
                item['images'] = images
                item['image_headers']={

                }
                item['bigdb'] = {
                    'name': response.meta.get("name"),
                    'norm': response.meta.get("norm"),
                    'content': htmlstr,
                    'normslug': '360doc',
                    'status': 'P'
                }
                item['category'] = response.meta.get("category")
                item['rep'] = {
                    'rep_image':rep_image
                }
                item['image_prefix']= '360doc'
                yield item
            else:
                logger.error(f"{response.meta.get('name')} 内容为空 不入库 {response.meta.get('norm')}")


        except Exception:
            raise Exception('parse 开头',traceback.format_exc())

