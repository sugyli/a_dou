# -*- coding:utf-8 -*-

import datetime
import re

import sys
import os
import django


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APPS_DIR)
sys.path.insert(0, os.path.join(APPS_DIR, 'quanbenxiaoshuo'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()


from novels.models import Novel

host = 'https://www.home520.com'

def creat_xml(filename, objs):  # 生成sitemap所需要的xml方法
    header = '<?xml version="1.0" encoding="utf-8"?>\n<urlset>\n'
    file = open(filename, 'w+', encoding='utf-8')
    file.writelines(header)
    file.close()
    i = 0
    for obj in objs:
        i += 1
        url=f'{host}{obj.get_novel_url()}'
        #times = datetime.datetime.now().strftime("%Y-%m-%d")
        times = obj.created_at.strftime("%Y-%m-%d")
        url = re.sub(r"&", "&amp;", url)  # 注意这里,在URL中如果含有&将会出错,所以需要进行转义

        # 这个是生成的主体,可根据需求进行修改
        ment = "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>\n" % (url, times)

        file = open(filename, 'a', encoding='utf-8')
        file.writelines(ment)
        file.close()
        print(f"{i} 生成{url}完成")

    last = "</urlset>"
    file = open(filename, 'a', encoding='utf-8')
    file.writelines(last)
    file.close()


if __name__ == '__main__':
    objs = \
        Novel.objects.get_published().order_by('-created_at').only('slug','created_at')[:10000]

    print(f"获取到的数据总数是{objs.count()}")


    #url_list = ['https://search.google.com', 'https://www.google.com', 'https://translate.google.cn','https://www.google.com']
    creat_xml("./data/smxml_novel.xml", objs)
