#!/usr/bin/env python
# encoding: utf-8

import xadmin
from .models import Category




class CategoryAdmin(object):
    list_display = ["name",'sort','show','push','category_type','parent_category','apply_prove']
    list_editable=["push", 'show', 'sort', 'mold']


    def apply_prove(self, obj):
        return f"<a href='{obj.get_url()}' target='_blank'>前端</a>&nbsp;" \
               f"<a href='{obj.get_debug_url()}' target='_blank'>调试</a>"
    apply_prove.short_description='操作'
    # 是否转义
    apply_prove.allow_tags=True

    # def save_models(self):
    #     obj = self.new_obj
    #     if not obj.user:
    #         obj.user = self.request.user
    #     obj.save()


xadmin.site.register(Category, CategoryAdmin)
