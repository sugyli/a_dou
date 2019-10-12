from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


from albums.models import Category,Album
from novels.models import Novel
from articles.models import Article



class CategoryDetailView(DetailView):
    model = Category
    #context_object_name="categorybyalbums"
    template_name="albums/category_detail.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        if context['category'].mold == 'Z':
            context['albums']=Album.objects.filter(
                category=context['category']).defer('info', 'created_at','is_tab')[:1000]

        if context['category'].mold == 'W':
            context['articles'] = Article.objects.get_published_no_user().filter(
                category=context['category']).only('name', 'slug','updated_at')[:1000]

        return context

    def get_queryset(self, **kwargs):
        return Category.objects.defer('created_at')


class AlbumDetailView(DetailView):
    model=Album
    template_name="albums/album_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(*args, **kwargs)
        context['novels'] =  Novel.objects.get_published().filter(album=context['album']).defer('info','created_at','updated_at')[:200]
        return context


class DeBugAlbumDetailView(LoginRequiredMixin,AlbumDetailView):
    pass
