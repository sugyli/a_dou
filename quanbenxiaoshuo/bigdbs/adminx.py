#!/usr/bin/env python
# encoding: utf-8

import xadmin
from .models import BigDb




class BigDbAdmin(object):
    list_display = ["name",'status','push','category','normslug','updated_at','apply_prove']
    style_fields={
        "content": "ueditor"
    }
    # 筛选
    list_filter=['push','status','created_at','updated_at','category','normslug']

    list_editable=["push",'status','name']
    search_fields=['name','slug']
    readonly_fields=['appendix','thumbnails']
    ordering=['-created_at']

    def apply_prove(self, obj):
        return f"<a href='{obj.get_url()}' target='_blank'>前端</a>&nbsp;" \
               f"<a href='{obj.get_debug_url()}' target='_blank'>调试</a>&nbsp;" \
               f"<a href='{obj.norm}' target='_blank'>来源</a>"
    apply_prove.short_description='操作'
    # 是否转义
    apply_prove.allow_tags=True

    # def save_models(self):
    #     obj = self.new_obj
    #     if not obj.user:
    #         obj.user = self.request.user
    #     obj.save()


xadmin.site.register(BigDb, BigDbAdmin)
