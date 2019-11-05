from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from django.views.generic import TemplateView

from articles import views

app_name = 'bigdbs'

if settings.DEBUG:
    urlpatterns = [
        #path('', views.ArticlesListView.as_view(), name='list'),
        path('<str:slug>-<int:id>/', TemplateView.as_view(template_name="pages/home.html"), name='bigdb'),
    ]
else:
    urlpatterns = [

        path('<str:slug>-<int:id>/'
             , cache_page(60 * 240)(TemplateView.as_view(template_name="pages/home.html"))
             , name='bigdb'),

    ]

urlpatterns +=[
    path('debug/<str:slug>-<int:id>/'
         , TemplateView.as_view(template_name="pages/home.html")
         , name='debug-bigdb')
]
