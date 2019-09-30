#!/usr/bin/env python
# encoding: utf-8

import xadmin
from .models import Article


class ArticleAdmin(object):
    list_display = ["name",'status','push','updated_at','apply_prove']
    style_fields={
        "content": "ueditor",
        "compose": "m2m_transfer",
        "category": "m2m_transfer"
    }
    # 筛选
    list_filter=['push','status']

    exclude=['user']
    list_editable=["push",'status']

    def apply_prove(self, obj):
        return f"<a href='{obj.get_article_url()}' target='_blank'>前端</a>&nbsp;" \
               f"<a href='{obj.get_debug_article_url()}' target='_blank'>调试</a>"
    apply_prove.short_description='操作'
    # 是否转义
    apply_prove.allow_tags=True

    def save_models(self):
        obj = self.new_obj
        if not obj.user:
            obj.user = self.request.user
        obj.save()


xadmin.site.register(Article, ArticleAdmin)

