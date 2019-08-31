from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings
from django.shortcuts import reverse

from slugify import slugify
from taggit.managers import TaggableManager
# from markdownx.models import MarkdownxField
# from markdownx.utils import markdownify
from DjangoUeditor.models import UEditorField
from albums.models import Album


@python_2_unicode_compatible
class ArticleQuerySet(models.query.QuerySet):
    """自定义QuerySet，提高模型类的可用性"""

    def get_published(self):
        """返回已发表的文章"""
        return self.filter(status="P").select_related('user')

    def get_published_no_user(self):
        """返回已发表的文章"""
        return self.filter(status="P")

    def get_drafts(self):
        """返回草稿箱的文章"""
        return self.filter(status="D").select_related('user')

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
class Article(models.Model):
    STATUS = (("D", "不公开"), ("P", "公开"))

    album = models.ManyToManyField(Album
                                   , blank = True
                                   , related_name="article_album"
                                   , verbose_name='专辑')

    name = models.CharField(max_length=255, null=False, unique=True, verbose_name='标题')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,blank=True ,related_name="user_article", on_delete=models.CASCADE, verbose_name='作者')
    slug = models.SlugField(max_length=255,blank=True, verbose_name='(URL)别名',unique=True,default=u'')
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='状态')  # 默认存入草稿箱
    content = UEditorField('内容', height=500, width=800,
                         default=u'', blank=False, imagePath="uploads/articles/images/%(year)s/%(month)s/%(basename)s_%(datetime)s_%(rnd)s.%(extname)s",
                         toolbars='full', filePath='uploads/articles/files/%(year)s/%(month)s/%(basename)s_%(datetime)s_%(rnd)s.%(extname)s')

    title=models.CharField(max_length=255, verbose_name='标题(seo)', default=u'',
                           help_text="title")
    keywords=models.CharField(max_length=255, verbose_name='关键字(seo)',
                              default=u'', help_text="keywords")
    description=models.CharField(max_length=255, verbose_name='描述(seo)',
                                 default=u'', help_text="description")

    tags = TaggableManager(help_text='多个标签使用,(英文)隔开',blank=True, verbose_name='标签')

    is_notice = models.BooleanField(default=False
                                    ,verbose_name="公告消息"
                                    ,help_text="不是文章而是站内公告")

    push=models.BooleanField(default=False
                             , verbose_name="推送"
                             , help_text="推送给熊掌")

    created_at = models.DateTimeField(db_index=True,auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(db_index=True,auto_now=True, verbose_name='更新时间')
    objects = ArticleQuerySet.as_manager()

    class Meta:
        index_together=[
            ('status','slug')
        ]
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ("-updated_at",)

    def __str__(self):
        return self.name

    def get_article_url(self):
        return reverse('articles:article', args=[self.slug])



    def save(self, *args, **kwargs):
        if self.is_notice:
            self.album = ''

        if not hasattr(self,'slug') or not self.slug:
            # 根据作者和标题生成文章在URL中的别名
            self.slug = slugify(self.name)

        super(Article, self).save(*args, **kwargs)


