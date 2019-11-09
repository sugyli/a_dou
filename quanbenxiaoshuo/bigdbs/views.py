from django.views.generic import ListView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import BigDb


class BigDbListView(ListView):
    """已发布的文章列表"""
    model = BigDb
    paginate_by = 15
    context_object_name = "bigdbs"
    template_name = "bigdbs/bigdb_list.html"  # 可省略

    def get_queryset(self, **kwargs):
        return BigDb.objects.get_published().select_related('category')



class BigDbDetailView(DetailView):
    """文章详情"""
    model = BigDb
    template_name = 'bigdbs/bigdb_detail.html'

    def get_queryset(self):
        return BigDb.objects.get_published().select_related('category')


class DeBugBigDbDetailView(LoginRequiredMixin,BigDbDetailView):
    def get_queryset(self, **kwargs):
        return BigDb.objects.select_related('category')
