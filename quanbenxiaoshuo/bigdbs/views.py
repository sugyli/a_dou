
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from .models import BigDb


class BigDbsListView(ListView):
    """已发布的文章列表"""
    model = BigDb
    paginate_by = 25
    context_object_name = "bigdbs"
    template_name = "bigdbs/bigdb_list.html"  # 可省略

    def get_context_data(self, *args, **kwargs):
        context = super(BigDbsListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self, **kwargs):
        return BigDb.objects.get_published()
