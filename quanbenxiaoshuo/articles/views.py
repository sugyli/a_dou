
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from articles.models import Article


# class ArticlesListView(ListView):
#     """已发布的文章列表"""
#     model = Article
#     paginate_by = 20
#     context_object_name = "articles"
#     template_name = "articles/article_list.html"  # 可省略
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
#         context['popular_tags'] = Article.objects.get_counted_tags()
#         return context
#
#     def get_queryset(self, **kwargs):
#         return Article.objects.get_published()



class DetailArticleView(DetailView):
    """文章详情"""
    model = Article
    template_name = 'articles/article_detail.html'

    def get_queryset(self):
        #return Article.objects.select_related('user').filter(slug=self.kwargs['slug'])
        return Article.objects.get_published().select_related('user')
