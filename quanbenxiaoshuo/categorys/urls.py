from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from django.views.generic import TemplateView

#from articles import views

app_name = 'categorys'

if settings.DEBUG:
    urlpatterns = [
        path('<str:slug>/', TemplateView.as_view(template_name="pages/home.html"), name='category'),
    ]
else:
    urlpatterns = [

        path('<str:slug>/'
             , cache_page(60 * 240)(TemplateView.as_view(template_name="pages/home.html"))
             , name='category'),

    ]

urlpatterns +=[
    path('debug/<str:slug>/'
         , TemplateView.as_view(template_name="pages/home.html")
         , name='debug-category')
]
