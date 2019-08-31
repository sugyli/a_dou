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
from .models import Category,Album,TabAlbum



class CategoryAdmin(object):
    list_display = ["name","apply_prove"]
    exclude = ["slug"]
    relfield_style='fk-ajax'

    def apply_prove(self, obj):
        return f"<a href='{obj.get_category_url()}' target='_blank'>前台</a>"
    apply_prove.short_description='操作'
    # 是否转义
    apply_prove.allow_tags=True


class AlbumAdmin(object):
    list_display = ["name","is_tab","updated_at","push","apply_prove"]
    exclude = ["slug"]
    #style_fields={"info": "ueditor"}
    list_editable=["is_tab"]
    relfield_style='fk-ajax'


    def apply_prove(self, obj):
        return f"<a href='{obj.get_album_url()}' target='_blank'>前台</a>"
    apply_prove.short_description='操作'
    # 是否转义
    apply_prove.allow_tags=True


class TabAlbuAdmin(object):
    list_display = ['name',"is_tab","updated_at"]
    exclude=["slug"]
    list_editable = ["is_tab"]
    #ordering = ['-created_at']

    def queryset(self):
        qs = super(TabAlbuAdmin, self).queryset()
        qs = qs.filter(is_tab=True)
        return qs



xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Album, AlbumAdmin)
xadmin.site.register(TabAlbum, TabAlbuAdmin)
