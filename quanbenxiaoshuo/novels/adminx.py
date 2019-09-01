#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: liyao
@license: Apache Licence 
@contact: yli@posbao.net
@site: http://www.piowind.com/
@software: PyCharm
@file: adminx.py
@time: 2017/7/4 17:04
"""
import xadmin
from .models import Novel,Chapter,Content



class ChapterInline(object):
    model = Chapter
    exclude=['slug']

    #style='table'# 列表显示，one：只显示一条  accordion：缩略列表显示，可下拉  tab：横向tab显示 stacked：块显示 table：列表
    extra = 0


class ContentInline(object):
    model = Content
    exclude=['chapter']
    extra = 0


class NovelAdmin(object):
    list_display = ["name","author",'album','category','is_full',"push",'apply_prove']
    #fields=('name', 'author')
    exclude = ["slug"]
    list_editable=['is_full',"push"]
    style_fields={
        'album':'m2m_transfer',
        'category':'m2m_transfer'
    }
    inlines=[ChapterInline]

    def apply_prove(self, obj):
        return f"<a href='{obj.get_novel_url()}' target='_blank'>前端</a>"

    apply_prove.short_description='操作'
    #是否转义
    apply_prove.allow_tags=True


class ChapterAdmin(object):
    list_display = ["name",'novel','apply_prove']
    exclude=["novel",'order','insert','is_tab','slug']
    inlines=[ContentInline]
    ordering=['-updated_at']

    def apply_prove(self, obj):
        return f"<a href='{obj.novel.get_novel_url()}' target='_blank'>目录</a>&nbsp;" \
               f"<a href='{obj.get_chapter_url()}' target='_blank'>内容</a>"

    apply_prove.short_description='操作'
    #是否转义
    apply_prove.allow_tags=True


    # def has_add_permission(self):
    #     return False

    def queryset(self):
        qs = super(ChapterAdmin, self).queryset()
        qs = qs.filter(is_tab=False)
        return qs



xadmin.site.register(Novel, NovelAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
