from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from DjangoUeditor.models import UEditorField
from django.shortcuts import reverse

from categorys.models import Category
from quanbenxiaoshuo import helpers

from slugify import slugify




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


    def get_url(self):
        return reverse('bigdbs:bigdb', args=[self.slug,self.id])

    def get_debug_url(self):
        return reverse('bigdbs:debug-bigdb', args=[self.slug,self.id])



    def save(self, *args, **kwargs):

        if not self.slug:
            slug = slugify(self.name)
            if len(slug)>50:
                slug = helpers.Md5(slug)
            self.slug = slug


        super(BigDb, self).save(*args, **kwargs)
