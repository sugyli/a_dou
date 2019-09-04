from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from albums import views

app_name = 'albums'


if settings.DEBUG:
    urlpatterns = [
        #path('', views.ArticlesListView.as_view(), name='list'),
        path('category/<str:slug>/', views.CategoryDetailView.as_view(), name='category'),
        path('<str:slug>/', views.AlbumDetailView.as_view(), name='album')

    ]
else:
    urlpatterns=[

        path('category/<str:slug>/'
             , cache_page(60 * 240)(views.CategoryDetailView.as_view())
             , name='category'),

        path('<str:slug>/'
             , cache_page(60 * 60)(views.AlbumDetailView.as_view())
             , name='album')

    ]


urlpatterns +=[
    path('debug/<str:slug>/', views.DeBugAlbumDetailView.as_view(), name='debugalbum')
]

