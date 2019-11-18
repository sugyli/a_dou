# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback,os,time,re
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
#DropItem是用来删除下载图片失败的item的
from scrapy.exceptions import DropItem

from novels.models import Novel
from albums.models import Album

import helpers

from articles.models import Article
from albums.models import Category
from bigdbs.models import BigDb
from categorys.models import Category as BigDbCategory

from django.conf import settings
from scrapy.utils.project import get_project_settings
scrapy_settings = get_project_settings()


import  logging
logger = logging.getLogger(__name__)



class NovelInfoSpiderPipeline(object):
    def process_item(self, item, spider):
        try:
            novel = item['novel']
            novel['image'] = item['cover']

            novel_obj = Novel.objects.create(**novel)
            novel_obj.tags.add(*item['tags'])

            albums = Album.objects.filter(name__in=item['albums'])
            if albums.count()>0:
                novel_obj.album.add(*albums)

            return f"{novel['name']} 入库完成"

        except Exception:

            raise Exception(traceback.format_exc())


class NovelImagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        try:
            for ok, value in results:
                image_file_path = None
                if ok:
                    image_file_path = value["path"]

            if image_file_path:
                item[self.images_urls_field] = image_file_path
            else:
                item[self.images_urls_field] = ''

            return item

        except Exception:
            raise Exception('图片采集有问题请检查 \n',traceback.format_exc())


class ArticleSpiderPipeline(object):
    def process_item(self, item, spider):
        try:
            article = item['article']
            print(f"{article['name']} 开始入库")
            for row in item['cover']:
                article['content'] = article['content']\
                    .replace(row['url'],os.path.join(settings.MEDIA_URL, row['path']))

            article['user_id'] = 1
            article_obj = Article.objects.create(**article)

            categorys = Category.objects.filter(name__in=item['categorys'])
            if categorys.count()>0:
                article_obj.category.add(*categorys)

            return f"{article_obj.name} 入库完成"


        except Exception:
            print(f"{article['name']} 出错了")
            raise Exception(traceback.format_exc())

class ArticleImagePipeline(ImagesPipeline):
    image_file_path = []

    def item_completed(self, results, item, info):
        try:
            if self.images_urls_field in item:
                for ok, value in results:
                    self.image_file_path.append(value)
                item[self.images_urls_field] = self.image_file_path
            else:
                item[self.images_urls_field] = []

        except Exception:
            item[self.images_urls_field]= []

        return item



class BigDbSpiderPipeline(object):
    def process_item(self, item, spider):

        if not item:
            return

        item['bigdb']['content'] = \
                    item['bigdb']['content']\
                        .replace(item['rep']['rep_p'], '<p>')\
                        .replace(item['rep']['rep_endp'], '</p>')

        for image in item['images']:
            item['bigdb']['content'] = \
                item['bigdb']['content']\
                    .replace(item['rep']['rep_image']
                             ,'<p class="dianshiju"><img src="{}" /></p>'.format('/'+settings.MAKEUP[-1]['prefix']+'/'+image),1)

        #过滤无用的标签
        item['bigdb']['content'] = \
            item['bigdb']['content']\
                .replace('<p></p>','')\
                .replace('<p><p>','<p>')\
                .replace('</p></p>','</p>')

        try:
            #入库
            if item['bigdb']['content'].strip():
                category = BigDbCategory.objects.get(name=item['category'])
                item['bigdb']['category'] = category
                BigDb.objects.create(**item['bigdb'])
                return f"{item['bigdb']['name']} 入库完成 {item['bigdb']['norm']}"

            else:

                print(
                    f"{item['bigdb']['name']} 内容不能为空 {item['bigdb']['norm']}")
                logger.error(
                    f"{item['bigdb']['name']} 内容不能为空 {item['bigdb']['norm']}")
                return


        except Exception:

            for image in item['images']:
                image_url = scrapy_settings['IMAGES_STORE'] +'/'+image
                # 判断文件是否存在
                if (os.path.exists(image_url)):
                    os.remove(image_url)
                    print(f"{item['bigdb']['name']} 入库失败 删除图片 {image_url} {item['bigdb']['norm']}")
            logger.error(
                f"{item['bigdb']['name']} 入库失败 {item['bigdb']['norm']}")
            return Exception(traceback.format_exc())

class BigDbImagePipeline(ImagesPipeline):


    def get_media_requests(self, item, info):

        headers={
            # "Host": "image109.360doc.cn",
            "Referer": item['bigdb']['norm'],
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
        }
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield

        for image_url in item[self.images_urls_field]:
            # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
            yield Request(image_url
                          ,headers=headers)

    # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    def file_path(self, request, response=None, info=None):
        # 定义文件名，年月日时分秒随机数
        fn = helpers.Md5(request.url)
        filename = u'360doc/{0}/{1}/{2}.jpg'.format(time.strftime('%Y'),time.strftime('%m'), fn)
        return filename

        # 项目管道里面的每一个item最终都会经过item_completd，也就是意味着有多少个item，这个item_completed函数就会被调用多少次。(不管下载成功，还是失败都会被调用)，如果不重写该方法，item默认都会返回出去。item_completed里面的return出去的item是经过整个项目管道处理完成之后的最终的一个item。
    def item_completed(self, results, item, info):
        # 在这通过debug可以看到results里数据,分下载图片成功和下载失败两种情况.
        # 如果下载成功results的结果：[(True, {'url': 'http://pics.sc.chinaz.com/Files/pic/icons128/7152/f1.png', 'path': '人物头像图标下载/f1.png', 'checksum': 'eb7f47737a062a1525457e451c41cc99'})]
        # True:代表图片下载成功
        # url：图片的地址
        # path:图片的存储路径
        # checksum:图片内容的 MD5 hash加密字符串
        # 如果下载失败results的结果:[(False, <twisted.python.failure.Failure scrapy.pipelines.files.FileException: 'NoneType' object has no attribute 'split'>)]
        # False:代表下载失败
        # error:下载失败的原因

        # 将图片的下载路径取出来(文件夹名/图片名)


        for i in range(len(results)):
            for x in range(len(item[self.images_urls_field])):
                if results[i][0]:
                    if item[self.images_urls_field][i] == results[i][1]['url']:
                        item[self.images_urls_field][i] = results[i][1]['path']
                        #break
                else:
                    for image in item[self.images_urls_field]:
                        #不是网站地址的时候
                        if not re.match(r'^https?:/{2}\w.+$', image):
                            image_url=scrapy_settings['IMAGES_STORE']+'/'+image
                            # 判断文件是否存在
                            if (os.path.exists(image_url)):
                                os.remove(image_url)
                                print(
                                    f"{item['bigdb']['name']} 下载图片失败 删除图片 {image_url} {item['bigdb']['norm']}")


                    print(f"{item['bigdb']['name']} 下载图片失败 不入库 {item['bigdb']['norm']}")
                    logger.error(f"{item['bigdb']['name']} 下载图片失败 不入库 {item['bigdb']['norm']}")
                    return []
                    #raise DropItem("图片下载失败，删除对应的item，不让该item返回出去。来源 {item['bigdb']['norm']}")

        return item

