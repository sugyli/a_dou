#!/usr/bin/env python
# encoding: utf-8

import xadmin
from .models import Article


class ArticleAdmin(object):
    list_display = ["name",'status','push','apply_prove']
    style_fields={
        "content": "ueditor",
        "compose": "m2m_transfer",
    }
    exclude=['user']
    list_editable=["push",'status']

    def apply_prove(self, obj):
        return f"<a href='{obj.get_article_url()}' target='_blank'>前端</a>"
    apply_prove.short_description='操作'
    # 是否转义
    apply_prove.allow_tags=True

    def save_models(self):
        obj = self.new_obj
        if not obj.user:
            obj.user = self.request.user
        obj.save()


xadmin.site.register(Article, ArticleAdmin)

