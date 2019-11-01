from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.shortcuts import reverse

from slugify import slugify

@python_2_unicode_compatible
class CategoryQuerySet(models.query.QuerySet):
    def get_published(self):
        return self.filter(show=True).order_by('sort')



@python_2_unicode_compatible
class Category(models.Model):

    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )


    name=models.CharField(default=""
                          , max_length=30
                          , verbose_name="分类名"
                          , help_text="分类名"
                          , unique=True)

    category_type=models.IntegerField(choices=CATEGORY_TYPE
                                      ,verbose_name="类目级别"
                                      , help_text="类目级别")

    parent_category=models.ForeignKey("self"
                                      , null=True
                                      , blank=True
                                      , verbose_name="父类目级别"
                                      , help_text="父目录"
                                      , related_name="sub_cat"
                                      , on_delete=models.CASCADE)


    title = models.CharField(max_length=255, verbose_name='标题(seo)', default=u'',help_text="title")
    keywords = models.CharField(max_length=255, verbose_name='关键字(seo)', default=u'',help_text="keywords")
    description =models.CharField(max_length=255, verbose_name='描述(seo)', default=u'',help_text="description")

    slug=models.SlugField(max_length=255
                          , blank=True
                          , verbose_name='(URL)别名'
                          , unique=True
                          , default=u'')


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
        verbose_name="大数据分类"
        verbose_name_plural=verbose_name
        ordering=("sort",)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('categorys:category', args=[self.slug])

    def get_debug_url(self):
        return reverse('categorys:debug-category', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            # 根据作者和标题生成文章在URL中的别名
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
