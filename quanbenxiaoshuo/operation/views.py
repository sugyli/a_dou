from django.views.generic import ListView,DetailView

from albums.models import Album
from novels.models import Novel
from operation.models import Compose



class IndexListView(ListView):
    model=Album
    context_object_name="albums"
    template_name="home/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(IndexListView, self).get_context_data(*args, **kwargs)
        #首页底部最新专栏
        context['newalbums'] = Album.objects.filter(is_tab=False).only('name','slug','image')[:200]
        #最新小说
        context['newnovels'] = Novel.objects.get_published().only('name','author','slug','image')[:200]

        return context

    def get_queryset(self, **kwargs):
        return Album.objects.filter(is_tab=True).select_related('category').defer('info','created_at')[:6]



class ComposeDetailView(DetailView):
    model = Compose
    template_name="operation/compose_detail.html"


class DeBugComposeDetailView(ComposeDetailView):
    pass

