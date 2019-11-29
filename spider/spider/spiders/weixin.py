# -*- coding: utf-8 -*-
import scrapy,traceback,copy,re
from scrapy.selector import Selector
from api import WechatSogouAPI

from bigdbs.models import BigDb

import logging
logger = logging.getLogger(__name__)

from ..items import BigDbSpiderItem

from scrapy.utils.project import get_project_settings
settings = get_project_settings()

from .. import help
from quanbenxiaoshuo import helpers


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
        "ITEM_PIPELINES": {
            'spider.pipelines.BigDbImagePipeline': 9,
            'spider.pipelines.BigDbSpiderPipeline': 10,
        }
    }
    temp='ABTEST=8|1573827016|v1; SUID=9FA664722028940A000000005DCEB1C8; weixinIndexVisited=1; SUV=008F98E47264A69F5DCEB1C97A780461; JSESSIONID=aaa1OIQWMMIwf5NF2xx4w; IPLOC=CN3405; CXID=B65EC80FC86B47999A15AFB9037BDBB6; ad=bb9nFyllll2NCM6$lllllVTgfvolllllT@pcxZllllwlllllVklll5@@@@@@@@@@; SUID=9A6460723565860A5BDC44E50005B54F'
    cookies={}
    for i in temp.split('; '):
        cookies[i.split('=')[0]]=i.split('=')[1]

    def start_requests(self):
        try:
            parameter=[
                {
                    'url': 'https://weixin.sogou.com/wapindex/wap/0612/wap_10/@@@@@@.html',
                    'category': '育儿',
                    'num': 10
                }
            ]
            for row in parameter:
                for i in range(row['num']):
                    url=row['url'].replace('@@@@@@', str(i))
                    headers=copy.deepcopy(self.headers)
                    headers['Referer']='https://weixin.sogou.com/'

                    yield scrapy.Request(url
                                        , meta={
                                                'category':row['category'],
                                            }
                                        , headers = headers
                                        , cookies=self.cookies
                                        , callback=self.parse_list)


        except Exception:
            raise Exception('start_requests 开头', traceback.format_exc())


    def parse_list(self, response):
        try:
            category=response.meta.get("category")
            if response.status==200:
                names = response.css(".list-txt h4 *::text").extract()
                nameurls = response.css(".list-txt h4 a::attr(href)").extract()
                nicknames = response.css(".list-txt .s2::text").extract()
                if len(names) != len(nameurls)!= len(nicknames) or len(names)==0:
                    logger.error(f"{response.url} 规则有问题")
                    return

                for row in zip(names,nameurls,nicknames):
                    name = row[0]
                    norm = row[1]
                    slug = helpers.Md5(str(row[2]) + str(name))

                    obj=BigDb.objects.filter(slug = slug)
                    if not obj:
                        ws_api = WechatSogouAPI()
                        res = ws_api.get_article_content(norm)
                        htmlstr=res['content_html']

                        compile_br=re.compile(r'<\s*br[^>]*>', re.I)
                        htmllist = compile_br.split(htmlstr)
                        if len(htmllist)>1:
                            htmlstr= \
                                ''.join(['<p>{}</p>'.format(s) for s in htmllist if
                                         s.strip()])

                        selector = Selector(text=htmlstr)
                        images=selector.css('img::attr(src)').extract()

                        rep_image="%%%%%%%%%%"
                        rex=r"""(<img\s.*?\s?src\s*=\s*['|"]?[^\s'"]+.*?>)"""
                        # 这么写的目的是不区分大小
                        compile_img=re.compile(rex, re.I)
                        htmlstr=compile_img.sub(rep_image, htmlstr)

                        htmlstr = help.handle_content(htmlstr)

                        if htmlstr:
                            item=BigDbSpiderItem()
                            item['images']=images
                            item['image_headers']={

                            }
                            item['bigdb']={
                                'name': name,
                                'norm': norm,
                                'content': htmlstr,
                                'normslug': 'weixin',
                                'slug': slug,
                                'status': 'P'
                            }
                            item['category']=category
                            item['rep']={
                                'rep_image': rep_image
                            }
                            item['image_prefix']='weixin'
                            yield item
                        else:
                            logger.error(f"{name} 内容为空 不入库 出错来源 {norm}")

                    else:
                        print(f"{name} 已经存在不添加")

            else:
                logger.error(f"出错来源 {response.url} 请求失败 状态码 {response.status}")



        except Exception:
            raise Exception('parse_list 开头', traceback.format_exc())











