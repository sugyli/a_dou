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
    list_display = ["name"]
    exclude = ["slug"]
    relfield_style='fk-ajax'


class AlbumAdmin(object):
    list_display = ["name"]
    exclude = ["slug"]
    style_fields={"info": "ueditor"}
    ordering=['-updated_at']
    relfield_style='fk-ajax'


class TabAlbuAdmin(object):
    list_display = ['name']
    exclude=["slug"]
    ordering = ['-created_at']

    def queryset(self):
        qs = super(TabAlbuAdmin, self).queryset()
        qs = qs.filter(is_tab=True)
        return qs



xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Album, AlbumAdmin)
xadmin.site.register(TabAlbum, TabAlbuAdmin)
