# -*- coding: utf-8 -*-
import scrapy,re

import requests
from scrapy.selector import Selector

from novels.models import Novel,Chapter,Content


from scrapy.utils.project import get_project_settings


settings = get_project_settings()

def start_urls():
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    res = requests.get("https://www.luoxia.com/jinyong/", headers=headers)
    if res.status_code == 200:
        selector=Selector(text=res.text)
        all_href = selector.css(".pop-books2 ol li a::attr(href)").extract()
        return list(set(all_href))
    else:
        raise Exception('start_urls 方法 网络请求失败')





class LuoxiaxiaoshuoSpider(scrapy.Spider):
    name = 'luoxiaxiaoshuo'
    allowed_domains = ['www.luoxia.com']
    #start_urls = ['https://www.luoxia.com/shendiao/']
    start_urls = start_urls()

    custom_settings = {
        #"IMAGES_URLS_FIELD": 'cover',
        "UserAgentList": settings['UserAgentList'],
        # "ITEM_PIPELINES": {
        #     'novelspider.pipelines.NovelImagePipeline': 9,
        #     'novelspider.pipelines.NovelspiderPipeline': 10,
        # }
    }

    def parse(self, response):
        novel_dict={}
        novel_dict['name'] = response.css(".book-describe>h1::text").extract()[0].strip()
        novel_dict['author'] = \
            response.css(".book-describe>p::text").extract()[0].replace('作者：','').strip()

        novel = Novel.objects.filter(**novel_dict).first()

        if not novel:
            print(f"小说 {novel_dict['name']} 没有入库 {response.url}")

        elif novel.is_full:
            print(f"小说 {novel_dict['name']} 已经完成不需要处理 {response.url}")

        else:
            print(f"采集 小说{novel.name} 章节和内容")
            def get_chaptet_obj():
                return {'url': '','name': '','ismulu': False}
            chapters_dict =[]
            chaptertext = response.css("#content-list>*").extract()
            #组装分卷和章节
            for row in chaptertext:
                selector = Selector(text=row)
                muluname = selector.css(".title.clearfix h3 a::text").extract_first("").strip()
                if muluname:
                    chapter=get_chaptet_obj()
                    chapter['ismulu'] = True
                    chapter['name'] = muluname
                    chapters_dict.append(chapter)

                else:
                    chapters = selector.css(".book-list.clearfix>ul li a")
                    for row in chapters:
                        chapter=get_chaptet_obj()
                        chapter['url'] = row.css('a::attr(href)').extract()[0].strip()
                        chapter['name']=row.css('a::text').extract()[0].strip()
                        chapters_dict.append(chapter)

            i = 0
            allchapter = len(chapters_dict)
            for item in chapters_dict:
                i+=1
                if item['ismulu']:
                    chapter=Chapter.objects.filter(novel=novel
                                                   ,order=i).first()
                    if chapter:
                        Content.objects.filter(chapter=chapter).delete()
                        chapter.name = item['name']
                        chapter.is_tab =True
                        chapter.order=i
                        chapter.save()
                    else:
                        chapter = Chapter()
                        chapter.name = item['name']
                        chapter.novel = novel
                        chapter.is_tab=True
                        chapter.order = i
                        chapter.save()

                    print(f"入库目录 {chapter.name} 序号{i} 小说名 {novel_dict['name']}")
                else:
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
                    res=requests.get(item['url'],headers=headers)
                    if res.status_code==200:
                        selector=Selector(text=res.text)
                        morepage = selector.css("article .apnavi")
                        text = selector.css("article #nr1 *::text").extract()
                        if morepage:
                            morepage = morepage[0]
                            pages = morepage.css('a::attr(href)').extract()
                            for page in pages:
                                print(f"请求章节分页 {page}")
                                res = requests.get(page, headers=headers)
                                if res.status_code==200:
                                    selector=Selector(text=res.text)
                                    text += selector.css("article #nr1 *::text").extract()
                                else:
                                    raise Exception(f"{item['name']} 内容分页请求失败 {page}")

                        text = ''.join(text)
                        text = text.strip()
                        if text:
                            chapter=Chapter.objects.filter(novel=novel
                                                               , order=i).first()
                            if chapter:
                                Content.objects.filter(chapter=chapter).delete()
                                chapter.name=item['name']
                                chapter.order=i
                                chapter.save()
                                Content.objects.create(content=text,chapter=chapter)
                            else:
                                chapter=Chapter()
                                chapter.name=item['name']
                                chapter.novel=novel
                                chapter.order=i
                                chapter.save()
                                Content.objects.create(content=text
                                                       ,chapter=chapter)
                            print(f"入库章节 {chapter.name} 序号{i} 小说名 {novel_dict['name']}")
                            if i == allchapter:
                                novel.is_full = True
                                novel.save()
                                print(f"{novel.name} 添加完成")
                                Chapter.objects.filter(novel=novel, order__gt=i).delete()
                                return
                        else:
                            raise Exception(f"{item['name']} 内容不存在 {item['url']}")

                    else:
                        raise Exception(f"{item['name']} 内容请求失败 {item['url']}")


            raise Exception(f"小说 {novel_dict['name']} 规则有问题手动调试 {response.url}")







