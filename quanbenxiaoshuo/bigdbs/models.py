from __future__ import unicode_literals
import re,json,os

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from DjangoUeditor.models import UEditorField
from django.shortcuts import reverse
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver



from categorys.models import Category
from quanbenxiaoshuo import helpers

from slugify import slugify
import emoji
from scrapy.selector import Selector





@python_2_unicode_compatible
class BigDbQuerySet(models.query.QuerySet):
    """自定义QuerySet，提高模型类的可用性"""

    def get_published(self):
        """返回已发表的文章"""
        return self.filter(status="P")




@python_2_unicode_compatible
class BigDb(models.Model):
    STATUS=(("D", "不公开"), ("P", "公开"))

    category = models.ForeignKey(Category
                                   , related_name="category_bigdb"
                                   , verbose_name='所属导航'
                                   , to_field='slug'
                                   , on_delete=models.CASCADE)

    name=models.CharField(max_length=255
                          , verbose_name='标题')

    status=models.CharField(max_length=1
                            , choices=STATUS
                            , default='D'
                            , verbose_name='状态')  # 默认存入草稿箱

    content=UEditorField('内容', height=500, width=800,
                         default=u'', blank=False,
                         imagePath="uploads/bigdbs/images/%(year)s/%(month)s/%(basename)s_%(datetime)s_%(rnd)s.%(extname)s",
                         toolbars='full',
                         filePath='uploads/bigdbs/files/%(year)s/%(month)s/%(basename)s_%(datetime)s_%(rnd)s.%(extname)s')

    title=models.CharField(max_length=255
                           , null=True
                           , blank=True
                           , verbose_name='标题(seo)'
                           , default=u''
                           , help_text="title")

    keywords=models.CharField(max_length=255
                              , null=True
                              , blank=True
                              , verbose_name='关键字(seo)'
                              , default=u''
                              , help_text="keywords")

    description=models.CharField(max_length=255
                                 , null=True
                                 , blank=True
                                 , verbose_name='描述(seo)'
                                 , default=u''
                                 , help_text="description")


    norm=models.CharField(max_length=255
                          , null=True
                          , blank=True
                          , default=u''
                          , verbose_name='来源标识')


    slug=models.SlugField(max_length=255
                          , blank=True
                          , verbose_name='(URL)别名'
                          , unique=True
                          , default=u'')

    appendix = models.TextField(blank=True
                     , null=True
                     , verbose_name='图片附件'
                     , default=u''
                     , help_text="图片附件")

    push=models.BooleanField(default=False
                             , verbose_name="推送"
                             , help_text="是否已经推送给熊掌")

    original = models.BooleanField(default=False
                             , verbose_name="是否原创"
                             , help_text="是否原创")

    created_at=models.DateTimeField(db_index=True
                                    , auto_now_add=True
                                    , verbose_name='创建时间')

    updated_at=models.DateTimeField(db_index=True
                                    , auto_now=True
                                    , verbose_name='更新时间')


    objects=BigDbQuerySet.as_manager()


    class Meta:
        index_together=[
            ('status','slug','id')
        ]
        verbose_name = '大数据'
        verbose_name_plural = verbose_name
        ordering = ("-updated_at",)


    def __str__(self):
        return self.name

    def get_comefrom(self):
        if self.original:
            return '原创'
        else:
            return '转载'

    def get_content(self):
        return emoji.emojize(self.content)


    def get_url(self):
        return reverse('bigdbs:bigdb', args=[self.slug,self.id])

    def get_debug_url(self):
        return reverse('bigdbs:bigdb-debug', args=[self.slug,self.id])


    def get_thumbnails(self):
        reg = r"""<img\s.*?\s?src\s*=\s*['|"]?([^\s'"]+).*?>"""
        pattern = re.compile(reg, re.I)
        return re.findall(pattern, self.content)

    def get_introduction(self):
        return helpers.replacenohtml(self.content)


    def get_title(self):
        if not self.title:
            return self.name

        return self.title

    def get_keywords(self):
        if not self.keywords:
            return self.name

        return self.keywords


    def get_description(self):

        if not self.description:
            return helpers.replacenohtml(self.content)
        else:
            return self.description

    def save(self, *args, **kwargs):

        if not self.slug:
            slug = slugify(self.name)
            if len(slug)>50:
                slug = helpers.Md5(slug)
            self.slug = slug


        if self.appendix:
            content = Selector(text=self.content)
            images = content.css('img::attr(src)').extract()
            images = set(images)
            appendix = self.appendix.split(',')
            appendix = set(appendix)
            for image in images:
                for r in appendix:
                    if image == r:
                        appendix.remove(r)
                        break

            for i in appendix:
                pathfile = f"{settings.APPS_DIR}{i}"
                # 判断文件是否存在
                if (os.path.exists(pathfile)):
                    os.remove(pathfile)

            self.appendix = ','.join(images)

        else:
            content = Selector(text=self.content)
            images = content.css('img::attr(src)').extract()
            images = set(images)
            if images:
                self.appendix = ','.join(images)


        super(BigDb, self).save(*args, **kwargs)





@receiver(post_delete,sender = BigDb)
def delete_post_delete_old_image(sender,instance,**kwargs):
    content=Selector(text=instance.content)
    images=content.css('img::attr(src)').extract()
    images=set(images)
    for image in images:
        pathfile=f"{settings.APPS_DIR}{image}"
        if (os.path.exists(pathfile)):
            os.remove(pathfile)

