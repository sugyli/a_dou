from django.views.generic import ListView

from albums.models import Album



class IndexListView(ListView):
    model=Album
    context_object_name="albums"
    template_name="home/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(IndexListView, self).get_context_data(*args, **kwargs)
        #首页底部最新专栏
        context['newalbums'] = Album.objects.filter(is_tab=False).defer('info','created_at')[:200]
        return context
    def get_queryset(self, **kwargs):
        return Album.objects.filter(is_tab=True).select_related('category').defer('info','created_at')[:6]

