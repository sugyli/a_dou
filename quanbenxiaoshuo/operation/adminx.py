import xadmin
from .models import Compose



class ComposeAdmin(object):
    list_display = ["name","updated_at","push","apply_prove"]
    #exclude = ["slug"]
    #style_fields={"info": "ueditor"}
    list_editable=["push"]
    # 筛选
    list_filter=['push']
    relfield_style='fk-ajax'
    ordering=['-updated_at']


    def apply_prove(self, obj):
        return f"{obj.get_compose_url()}"
        # return f"<a href='{obj.get_compose_url()}' target='_blank'>前端</a>&nbsp;" \
        #        f"<a href='{obj.get_debug_compose_url()}' target='_blank'>调试</a>"

    apply_prove.short_description='操作'
    # 是否转义
    apply_prove.allow_tags=True


xadmin.site.register(Compose, ComposeAdmin)
