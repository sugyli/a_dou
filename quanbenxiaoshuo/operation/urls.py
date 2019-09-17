from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from operation import views

app_name = 'operation'


if settings.DEBUG:
    urlpatterns = [
        path('<str:slug>/', views.ComposeDetailView.as_view(), name='compose')

    ]
else:
    urlpatterns=[
        path('<str:slug>/'
             , cache_page(60 * 120)(views.ComposeDetailView.as_view())
             , name='compose')

    ]


urlpatterns +=[
    path('debug/<str:slug>/', views.DeBugComposeDetailView.as_view(), name='debugcompose')
]

