# -*- coding: utf-8 -*-
import scrapy

import requests,traceback
from urllib import parse
from scrapy.selector import Selector

from novels.models import Novel,Chapter,Content

from scrapy.utils.project import get_project_settings


settings = get_project_settings()
'''
a>b 就搜索a下面的子元素b
a b b是a下面所有元素包括孙子辈
'''




def start_urls():
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    res = requests.get("http://www.my2852.com/wuxia/huangyi/index.htm", headers=headers)
    if res.status_code == 200:
        selector=Selector(text=res.content.decode('gbk','ignore'))
        all_href = selector.css(".jz table a::attr(href)").extract()
        all_href =  list(set(all_href))
        full_all_href = []
        for href in all_href:
            if 'index.htm' in href:
                full_all_href.append(parse.urljoin('http://www.my2852.com/wuxia/huangyi/index.htm', href))
            else:
                print(f"这个 {href} 好像不是目录")

        return full_all_href
    else:
        raise Exception('start_urls 方法 网络请求失败')


class My2852Spider(scrapy.Spider):
    name = 'my2852'
    allowed_domains = ['www.my2852.com']
    #start_urls = ['http://www.my2852.com/wuxia/huangyi/xqj/index.htm']
    start_urls=start_urls()


    custom_settings = {
        "UserAgentList": settings['UserAgentList'],
    }


    def parse(self, response):

        try:
            novel_dict={}
            novel_dict['name']=response.css("table .tdw::text").extract()[0].strip()
            novel_dict['author']= \
                response.css("table .tdw2::text").extract()[0].replace('作者：','').strip()

            novel=Novel.objects.filter(**novel_dict).first()

            if not novel:
                print(f"小说 {novel_dict['name']} 没有入库 {response.url}")

            elif novel.is_full:
                print(f"小说 {novel_dict['name']} 已经完成不需要处理 {response.url}")

            else:
                print(f"采集 小说{novel.name} 章节和内容")

                def get_chaptet_obj():
                    return {'url': '', 'name': '', 'ismulu': False}

                chapters_dict=[]
                chaptertext=response.css(".tbw3 td").extract()
                # 组装分卷和章节
                for row in chaptertext:
                    selector=Selector(text=row)
                    muluname=selector.css(".tdw3::text").extract_first("").strip()

                    if muluname:
                        chapter=get_chaptet_obj()
                        chapter['ismulu']=True
                        chapter['name']=muluname
                        chapters_dict.append(chapter)

                    else:
                        chapters=selector.css("a")
                        i = 0
                        name = ''
                        for row in chapters:
                            i+=1
                            chapter=get_chaptet_obj()
                            chapter['url'] = parse.urljoin(response.url, row.css('a::attr(href)').extract()[0].strip())
                            if i > 1:
                                chapter['name']= "{}{}".format(name,row.css('a::text').extract()[0].strip())
                            else:
                                name = chapter['name'] = row.css('a::text').extract()[0].strip()

                            chapters_dict.append(chapter)

                #处理内容部分
                i=0
                allchapter=len(chapters_dict)
                for item in chapters_dict:
                    i+=1
                    if item['ismulu']:
                        chapter=Chapter.objects.filter(novel=novel, order=i).first()
                        if chapter:
                            Content.objects.filter(chapter=chapter).delete()
                            chapter.name=item['name']
                            chapter.is_tab=True
                            chapter.order=i
                            chapter.save()
                        else:
                            chapter=Chapter()
                            chapter.name=item['name']
                            chapter.novel=novel
                            chapter.is_tab=True
                            chapter.order=i
                            chapter.save()

                        print(
                            f"入库目录 {chapter.name} 序号{i} 小说名 {novel_dict['name']}")
                    else:
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}

                        print(f"采集内容地址 {item['url']}")

                        res=requests.get(item['url'], headers=headers)
                        if res.status_code==200:
                            selector=Selector(text=res.content.decode('gbk','ignore'))
                            #分页规则
                            morepage=selector.css("article .apnavi")
                            #内容规则
                            text=selector.css("table.tb tr:nth-child(4) *::text").extract()
                            #如果存在分页
                            if morepage:
                                morepage=morepage[0]
                                pages=morepage.css('a::attr(href)').extract()
                                for page in pages:
                                    print(f"请求章节分页 {page}")
                                    res=requests.get(page, headers=headers)
                                    if res.status_code==200:
                                        selector=Selector(text=res.content.decode('gbk','ignore'))
                                        text+=selector.css("table.tb tr:nth-child(4) *::text").extract()
                                    else:
                                        raise Exception(
                                            f"{item['name']} 内容分页请求失败 {page}")

                            text=''.join(text)
                            text=text.strip()
                            if text:
                                chapter=Chapter.objects.filter(novel=novel, order=i).first()
                                if chapter:
                                    Content.objects.filter(
                                        chapter=chapter).delete()
                                    chapter.name=item['name']
                                    chapter.order=i
                                    chapter.save()
                                    Content.objects.create(content=text,
                                                           chapter=chapter)
                                else:
                                    chapter=Chapter()
                                    chapter.name=item['name']
                                    chapter.novel=novel
                                    chapter.order=i
                                    chapter.save()
                                    Content.objects.create(content=text
                                                           , chapter=chapter)

                                print(f"入库章节 {chapter.name} 序号{i} 小说名 {novel_dict['name']}")

                                if i==allchapter:
                                    novel.is_full=True
                                    novel.save()
                                    print(f"{novel.name} 添加完成")
                                    Chapter.objects.filter(novel=novel
                                                           ,order__gt=i).delete()
                                    return
                            else:
                                raise Exception(
                                    f"{item['name']} 内容不存在 {item['url']}")

                        else:
                            raise Exception(f"{item['name']} 内容请求失败 {item['url']}")

                raise Exception(
                    f"小说 {novel_dict['name']} 规则有问题手动调试 {response.url}")


        except Exception:
            self.logger.error(response.url+' 出错地址')
            raise Exception(traceback.format_exc())

