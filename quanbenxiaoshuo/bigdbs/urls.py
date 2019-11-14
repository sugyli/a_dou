from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from django.views.generic import TemplateView

from bigdbs import views

app_name = 'bigdbs'

if settings.DEBUG:
    urlpatterns = [
        #path('', views.BigDbListView.as_view(), name='list'),
        path('<str:slug>-<int:pk>/', views.BigDbDetailView.as_view(), name='bigdb'),
    ]
else:
    urlpatterns = [
        #path('', cache_page(60 * 240)(views.BigDbListView.as_view()), name='list'),

        path('<str:slug>-<int:pk>/'
             , cache_page(60 * 240)(views.BigDbDetailView.as_view())
             , name='bigdb'),

    ]

urlpatterns +=[
    path('debug/<str:slug>-<int:pk>/'
         , views.DeBugBigDbDetailView.as_view()
         , name='bigdb-debug')
]
