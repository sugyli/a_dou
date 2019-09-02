from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.shortcuts import reverse

from albums.models import Album,Category
#from DjangoUeditor.models import UEditorField
from slugify import slugify
from taggit.managers import TaggableManager
from quanbenxiaoshuo.storage import ImageStorage
from quanbenxiaoshuo import helpers


@python_2_unicode_compatible
class NovelQuerySet(models.query.QuerySet):
    def get_published(self):
        """返回已发表的小说"""
        return self.filter(status="P")

    def get_drafts(self):
        """返回草稿箱的小说"""
        return self.filter(status="D")

    def get_counted_tags(self):
        """统计所有已发布的文章中，每一个标签的数量(大于0的)"""
        tag_dict = {}
        for obj in self.all():
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:
                    tag_dict[tag] += 1
        return tag_dict.items()

@python_2_unicode_compatible
class Novel(models.Model):
    STATUS=(("D", "不公开"), ("P", "公开"))

    name = models.CharField(max_length=255,null=False,blank=False,verbose_name='标题')
    author=models.CharField(max_length=255
                            , null=False
                            , blank=False
                            , verbose_name=u"作者")

    image=models.ImageField(upload_to='novel/%Y/%m'
                            , storage=ImageStorage()
                            , verbose_name='小说封面'
                            , null=True
                            , blank=True)


    tags=TaggableManager(help_text='多个标签使用,(英文)隔开', verbose_name='小说类型')
    album = models.ManyToManyField(Album
                                   ,blank=True
                                   ,related_name="album_novel"
                                   ,verbose_name='专辑')

    category = models.ManyToManyField(Category
                                      ,blank=True
                                      ,related_name="category_novel"
                                      ,verbose_name='类别')

    info = models.TextField(verbose_name=u"简介")


    title=models.CharField(max_length=255, verbose_name='标题(seo)', default=u'',
                           help_text="title")
    keywords=models.CharField(max_length=255, verbose_name='关键字(seo)',
                              default=u'', help_text="keywords")

    description=models.CharField(max_length=255
                                 , null=True
                                 , blank=True
                                 , verbose_name='描述(seo)'
                                 , default=u''
                                 , help_text="description")

    status=models.CharField(max_length=1
                            , choices=STATUS
                            , default='D'
                            , verbose_name='状态')  # 默认存入草稿箱

    slug=models.SlugField(max_length=255
                          , blank=True
                          , verbose_name='(URL)别名'
                          , unique=True
                          , default=u'')

    is_full = models.BooleanField(default=False, verbose_name='是否完本')

    push=models.BooleanField(default=False
                             , verbose_name="推送"
                             , help_text="是否已经推送给熊掌")

    created_at=models.DateTimeField(db_index=True,auto_now_add=True,verbose_name='创建时间')
    updated_at=models.DateTimeField(db_index=True,auto_now=True, verbose_name='更新时间')

    objects=NovelQuerySet.as_manager()

    class Meta:
        unique_together=[
            ('name', 'author')
        ]
        index_together=[
            ('status','slug')
        ]
        verbose_name=u'小说'
        verbose_name_plural=verbose_name
        ordering=("-updated_at",)

    def __str__(self):
        return self.name

    def get_is_full(self):
        if self.is_full:
            return '完本'
        else:
            return '连载中'

    def get_novel_url(self):
        return reverse('novels:novel', args=[self.slug])

    def get_description(self):

        if not self.description:
            return helpers.descriptionreplace(self.info)
        else:
            return self.description

    def get_info(self):
        return helpers.contentreplace(self.info,out=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            # 根据作者和标题生成文章在URL中的别名
            self.slug = slugify(str(self.name)+str(self.author))

        if hasattr(self,'info') and self.info.strip():

            self.info = helpers.contentreplace(self.info,out=False)

        super(Novel, self).save(*args, **kwargs)




@python_2_unicode_compatible
class ChapterQuerySet(models.query.QuerySet):
    def get_published(self):

        return self.filter(novel__status="P",is_tab=0).select_related('novel')

class Chapter(models.Model):

    is_tab=models.BooleanField(default=False, verbose_name="是否目录")

    novel=models.ForeignKey(Novel
                            , on_delete=models.CASCADE
                            , verbose_name=u"小说名称"
                            , related_name="novel_chapter"
                            , default=u'')
    #1对1
    # content=models.OneToOneField(Content
    #                              , default=u''
    #                              , on_delete=models.CASCADE
    #                              , verbose_name=u"内容")

    name = models.CharField(max_length=255, verbose_name=u"章节名")

    order = models.SmallIntegerField(default=0
                                     ,db_index=True
                                     ,blank=True
                                     ,verbose_name=u"排序"
                                     ,help_text='自动递增')

    insert = models.SmallIntegerField(default=0
                                     ,blank=True
                                     ,null=True
                                     ,verbose_name=u"插入章节"
                                     ,help_text='插入章节order')

    slug=models.SlugField(max_length=255
                          , unique=True
                          , blank=True
                          , verbose_name='(URL)别名'
                          , default=u'')

    push=models.BooleanField(default=False
                             , verbose_name="推送"
                             , help_text="是否已经推送给熊掌")

    created_at=models.DateTimeField(db_index=True,auto_now_add=True,verbose_name='创建时间')
    updated_at=models.DateTimeField(db_index=True,auto_now=True, verbose_name='更新时间')
    objects=ChapterQuerySet.as_manager()

    class Meta:
        index_together=[
            ('novel','slug','is_tab'),
            ('novel', 'order','is_tab')
        ]
        verbose_name = u"章节"
        verbose_name_plural = verbose_name
        ordering=("order",)

    def __str__(self):
        return self.name

    def get_chapter_url(self):
        return reverse('novels:chapter', args=[self.slug])

    def get_chapter_content(self):
        #获取内容
        return Content.objects.filter(chapter=self).only('content').first()


    def save(self, *args, **kwargs):

        if not self.order:
            chapter=Chapter.objects.filter(novel=self.novel).order_by('-order').first()
            if chapter:
                self.order=chapter.order+1
            else:
                self.order=1

        if not self.slug:
            # 根据作者和标题生成文章在URL中的别名
            self.slug =f"{slugify(self.novel.slug)}_{self.order}"

        super(Chapter, self).save(*args, **kwargs)




class Content(models.Model):

    chapter=models.ForeignKey(Chapter
                            , on_delete=models.CASCADE
                            , verbose_name=u"小说章节"
                            , related_name="chapter_content"
                            , default=u'')

    content = models.TextField(verbose_name=u"小说内容")

    created_at=models.DateTimeField(db_index=True,auto_now_add=True, verbose_name='创建时间')
    updated_at=models.DateTimeField(db_index=True,auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.chapter.name} 的内容'

    def get_content(self):
        return helpers.contentreplace(self.content,out=True)

    def save(self, *args, **kwargs):

        if hasattr(self,'content') and self.content.strip():

            self.content = helpers.contentreplace(self.content,out=False)

        super(Content, self).save(*args, **kwargs)



