from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.shortcuts import reverse


from slugify import slugify
from quanbenxiaoshuo.storage import ImageStorage
from quanbenxiaoshuo import helpers




@python_2_unicode_compatible
class Compose(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True,verbose_name='标题')

    image=models.ImageField(upload_to='compose/%Y/%m'
                            , storage=ImageStorage()
                            , verbose_name='聚合封面'
                            , null=True
                            , blank=True)

    info=models.TextField(verbose_name=u"简介")


    slug=models.SlugField(max_length=255, blank=True, verbose_name='(URL)别名',unique=True,default=u'')

    title=models.CharField(max_length=255, verbose_name='标题(seo)', default=u'',help_text="title")
    keywords=models.CharField(max_length=255, verbose_name='关键字(seo)',default=u'', help_text="keywords")
    description=models.CharField(max_length=255,null=True, blank=True, verbose_name='描述(seo)',default=u'', help_text="description")

    push=models.BooleanField(default=False
                             , verbose_name="推送"
                             , help_text="是否已经推送给熊掌")

    created_at=models.DateTimeField(db_index=True,auto_now_add=True,verbose_name='创建时间')

    updated_at=models.DateTimeField(db_index=True
                                    , auto_now=True
                                    , verbose_name='更新时间')

    class Meta:
        verbose_name="聚合"
        verbose_name_plural=verbose_name
        ordering=("-updated_at",)

    def __str__(self):
        return self.name

    def get_compose_url(self):
        return '/'
        #return reverse('operation:compose', args=[self.slug])

    def get_debug_compose_url(self):
        return reverse('operation:debugcompose', args=[self.slug])

    def get_description(self):

        if not self.description:
            return helpers.descriptionreplace(self.info)
        else:
            return self.description

    def get_info(self):
        return helpers.contentreplace(self.info,out=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if hasattr(self,'info') and self.info.strip():
            self.info = helpers.contentreplace(self.info,out=False)

        super(Compose, self).save(*args, **kwargs)
