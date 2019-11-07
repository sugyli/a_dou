import math
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseNotFound

from .models import Category
from bigdbs.models import BigDb

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class CategoryDetailView(DetailView):

    model = Category
    template_name = 'categorys/category_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        bigdbs = BigDb.objects.filter(category=context['category']).get_published().select_related('category')

        #分页
        try:
            page = int(self.request.GET.get('page', 1))
        except PageNotAnInteger:
            page = 1
        pageSize = 25
        totalPage=math.ceil(len(bigdbs)/pageSize)

        if page > totalPage:
            raise Http404("Question does not exist")

        # 第二个参数代表每一页显示的个数
        p = Paginator(bigdbs , pageSize, request=self.request)
        page_bigdbs = p.page(page)
        context['bigdbs'] = page_bigdbs

        return context

