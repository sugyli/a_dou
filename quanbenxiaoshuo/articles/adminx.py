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
from .models import Article
"""
list_display 控制列表展示的字段
search_fields 控制可以通过搜索框搜索的字段名称，xadmin使用的是模糊查询
list_filter 可以进行过滤操作的列
ordering 默认排序的字段
readonly_fields 在编辑页面的只读字段
exclude 在编辑页面隐藏的字段
list_editable 在列表页可以快速直接编辑的字段
show_detail_fileds 在列表页提供快速显示详情信息
refresh_times 指定列表页的定时刷新
list_export 控制列表页导出数据的可选格式
show_bookmarks 控制是否显示书签功能
data_charts 控制显示图标的样式
model_icon 控制菜单的图标
"""


class ArticleAdmin(object):
    list_display = ["name",'status','push','apply_prove']
    style_fields={
        "content": "ueditor",
        "compose": "m2m_transfer"
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

