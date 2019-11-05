from django.views.generic import DetailView

from categorys.models import Category




class CategorysDetailView(DetailView):
    model = Category
    paginate_by=20
    #context_object_name="categorys"
    template_name="categorys/category_detail.html"
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super(CategorysDetailView, self).get_context_data(*args, **kwargs)


        return context

    # def get_queryset(self, **kwargs):
    #     return Category.objects.get_published()
