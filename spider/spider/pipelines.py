# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback
from scrapy.pipelines.images import ImagesPipeline

from novels.models import Novel
from albums.models import Album



class NovelInfoSpiderPipeline(object):
    def process_item(self, item, spider):
        try:
            novel = item['novel']
            novel['image'] = item['cover']

            novel_obj = Novel.objects.create(**novel)
            novel_obj.tags.add(*item['tags'])

            albums = Album.objects.filter(name__in=item['albums'])
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
