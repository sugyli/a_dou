# -*- coding: utf-8 -*-
import scrapy

import requests,traceback,re
from urllib import parse
from scrapy.selector import Selector

from ..help import start_urls,parse_info
from novels.models import Novel,Chapter,Content

from scrapy.utils.project import get_project_settings



settings = get_project_settings()
'''
a>b 就搜索a下面的子元素b
a b b是a下面所有元素包括孙子辈
'''





class My2852Spider(scrapy.Spider):
    name = 'my2852'
    allowed_domains = ['www.my2852.com']
    #start_urls = ['http://www.my2852.com/yq/l/lsf/xlqy/index.htm']
    start_urls=start_urls()


    custom_settings = {
        "UserAgentList": settings['UserAgentList'],
    }


    def parse(self, response):

        try:
            novel_dict = parse_info(response,'安彤')

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

                if not chaptertext:
                    chaptertext=response.css("center>table:nth-child(2) td").extract()

                if not chaptertext:
                    chaptertext=response.css("center>div>table td").extract()

                if not chaptertext:
                    chaptertext=response.css("div table>tr:nth-child(4)>td table>tr>td").extract()

                if not chaptertext:
                    chaptertext=response.css("div table.tb5 table.tb3 td").extract()

                if not chaptertext:
                    chaptertext=response.css("div table.tb5 .td6>div>div table td table td").extract()

                # if not chaptertext:
                #     chaptertext=response.css("div table>tr:nth-child(3)>td table>tr>td").extract()

                # if not chaptertext:
                #     chaptertext=response.css("center>table:nth-child(1) td").extract()




                # 组装分卷和章节
                for row in chaptertext:
                    selector=Selector(text=row)

                    chapters=selector.css("a")

                    if chapters:
                        i=0
                        name=''
                        for row in chapters:
                            i+=1
                            chapter=get_chaptet_obj()
                            chapter['url']=parse.urljoin(response.url, row.css('a::attr(href)').extract()[0].strip())
                            # matchObj = re.match(r'http://www.my2852.com/wuxia/nk/zqsj/(\d+)htm', chapter['url'],re.M|re.I)
                            # if matchObj:
                            #     chapter['url']=f'http://www.my2852.com/wuxia/nk/zqsj/{matchObj.group(1)}.htm'

                            # if "/jn/33.htm" in str(chapter['url']):
                            #     continue



                            if i>1:
                                get_name=row.css('a>span::text').extract_first(
                                    "").strip()
                                if not get_name:
                                    chapter['name']="{}{}".format(name,
                                                                  row.css(
                                                                      'a::text').extract()[
                                                                      0].strip())
                                else:
                                    chapter['name']="{}{}".format(name,
                                                                  get_name)

                            else:
                                name=chapter['name']= \
                                row.css('a::text').extract()[0].strip()

                            chapters_dict.append(chapter)
                    else:

                        muluname=selector.css(".tdw3::text").extract_first("").strip()
                        if not muluname:
                            muluname=selector.css("td::text").extract_first("").replace('附：','').strip()

                        if not muluname:
                            muluname=selector.css("td>span::text").extract_first("").strip()

                        if not muluname:
                            muluname=selector.css("td>span>b::text").extract_first("").strip()

                        if muluname:
                            chapter=get_chaptet_obj()
                            chapter['ismulu']=True
                            chapter['name']=muluname
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
                            if not text:
                                text=selector.css(
                                    "center>table tr:nth-child(4) *::text").extract()


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
                            text = text.replace('𠴂','口').replace('&#134402;','口').strip()
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
                                    novel.status = 'P'
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
                    "小说 {} 规则有问题手动调试 {}".format(novel_dict['name'],response.url))


        except Exception:
            self.logger.error('------------------------------------')
            raise Exception(traceback.format_exc())

