from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from django.views.generic import TemplateView

from categorys import views

app_name = 'categorys'

if settings.DEBUG:
    urlpatterns = [
        path('<str:slug>/', views.CategorysDetailView.as_view(), name='category'),
    ]
else:
    urlpatterns = [

        path('<str:slug>/'
             , cache_page(60 * 240)(views.CategorysDetailView.as_view())
             , name='category'),

    ]

urlpatterns +=[
    path('debug/<str:slug>/'
         , views.CategorysDetailView.as_view()
         , name='debug-category')
]
