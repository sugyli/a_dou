from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from categorys import views

app_name = 'articles'

if settings.DEBUG:
    urlpatterns = [
        path('<str:slug>/'
             , views.CategoryDetailView.as_view()
             , name='category'),
    ]
else:
    urlpatterns = [
        path('<str:slug>/'
             , cache_page(60 * 240)(views.CategoryDetailView.as_view())
             , name='category'),

    ]

