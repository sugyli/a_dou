# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback,os
from scrapy.pipelines.images import ImagesPipeline

from novels.models import Novel
from albums.models import Album



from articles.models import Article
from albums.models import Category

from django.conf import settings



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
            if self.images_urls_field in item:
                for ok, value in results:
                    image_file_path = value["path"]
                item[self.images_urls_field] = image_file_path
            else:
                item[self.images_urls_field] = ''

        except Exception:
            item[self.images_urls_field]=''

        return item




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
