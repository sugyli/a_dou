from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.shortcuts import reverse
from django.conf import settings

#from DjangoUeditor.models import UEditorField
from slugify import slugify
from quanbenxiaoshuo.storage import ImageStorage
from quanbenxiaoshuo import helpers

@python_2_unicode_compatible
class CategoryQuerySet(models.query.QuerySet):
    def get_published(self):
        return self.filter(show=True).order_by('sort')

@python_2_unicode_compatible
class Category(models.Model):
    MOLD=(("Z", "专栏"), ("W", "文章"))

    mold=models.CharField(max_length=1
                            , choices=MOLD
                            , default='Z'
                            , verbose_name='类型')

    name=models.CharField(default="", max_length=30, verbose_name="类别名",
                          help_text="类别名",unique=True)


    title = models.CharField(max_length=255, verbose_name='标题(seo)', default=u'',help_text="title")
    keywords = models.CharField(max_length=255, verbose_name='关键字(seo)', default=u'',help_text="keywords")
    description =models.CharField(max_length=255, verbose_name='描述(seo)', default=u'',help_text="description")

    slug=models.SlugField(max_length=255, blank=True, verbose_name='(URL)别名',
                          unique=True, default=u'')


    sort = models.SmallIntegerField(default=0
                                     ,blank=True
                                     ,null=True
                                     ,db_index=True
                                     ,verbose_name=u"排序")

    show=models.BooleanField(default=True
                             , verbose_name="导航显示"
                             , help_text="在导航显示")

    push=models.BooleanField(default=False
                             , verbose_name="推送"
                             , help_text="是否已经推送给熊掌")

    created_at=models.DateTimeField(db_index=True,auto_now_add=True,verbose_name='创建时间')

    objects = CategoryQuerySet.as_manager()

    class Meta:
        verbose_name="分类"
        verbose_name_plural=verbose_name
        ordering=("sort",)

    def __str__(self):
        return self.name

    def get_category_url(self):
        return reverse('albums:category', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            # 根据作者和标题生成文章在URL中的别名
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)



@python_2_unicode_compatible
class Album(models.Model):
    category=models.ForeignKey(Category, related_name="category_album",on_delete=models.CASCADE, verbose_name='类别',default=u'')

    name = models.CharField(max_length=255, null=False, unique=True,verbose_name='标题')

    image=models.ImageField(upload_to='album/%Y/%m', storage=ImageStorage(),
                            verbose_name='专辑封面', null=True, blank=True)

    info=models.TextField(verbose_name=u"简介")


    slug=models.SlugField(max_length=255, blank=True, verbose_name='(URL)别名',unique=True,default=u'')

    title=models.CharField(max_length=255, verbose_name='标题(seo)', default=u'',help_text="title")
    keywords=models.CharField(max_length=255, verbose_name='关键字(seo)',default=u'', help_text="keywords")
    description=models.CharField(max_length=255,null=True, blank=True, verbose_name='描述(seo)',default=u'', help_text="description")

    is_tab=models.BooleanField(default=False,
                               verbose_name="编辑推荐", help_text="首页编辑推荐显示")

    push=models.BooleanField(default=False
                             , verbose_name="推送"
                             , help_text="是否已经推送给熊掌")

    is_machine=models.BooleanField(default=False,
                               verbose_name="是否机器提交", help_text="是否采集提交")

    created_at=models.DateTimeField(db_index=True,auto_now_add=True,verbose_name='创建时间')

    updated_at=models.DateTimeField(db_index=True
                                    , auto_now=True
                                    , verbose_name='更新时间')

    class Meta:
        verbose_name="专辑"
        verbose_name_plural=verbose_name
        ordering=("-updated_at",)

    def __str__(self):
        return self.name

    def get_album_url(self):
        return reverse('albums:album', args=[self.slug])

    def get_debug_album_url(self):
        return reverse('albums:debugalbum', args=[self.slug])

    def get_description(self):

        if not self.description:
            return helpers.descriptionreplace(self.info)
        else:
            return self.description

    def get_info(self):
        return helpers.contentreplace(self.info,out=True)


    def save(self, *args, **kwargs):

        if not self.image and not self.is_machine:
            self.image = settings.DEF_IMAGE


        if not self.slug:
            # 根据作者和标题生成文章在URL中的别名
            self.slug = slugify(self.name)

        if hasattr(self,'info') and self.info.strip():
            self.info = helpers.contentreplace(self.info,out=False)

        super(Album, self).save(*args, **kwargs)



class TabAlbum(Album):
    class Meta:
        verbose_name = "推荐专辑"
        verbose_name_plural = verbose_name
        proxy = True
