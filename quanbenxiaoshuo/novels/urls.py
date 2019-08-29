from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from novels import views
app_name = 'novels'


if settings.DEBUG:
    urlpatterns = [
        path('<str:slug>/', views.NovelDetailView.as_view(), name='novel'),
        path('chapter/<int:pk>/', views.ChapterDetailView.as_view(), name='chapter')
    ]
else:
    urlpatterns = [
        path('<str:slug>/'
             , cache_page(60 * 240)(views.NovelDetailView.as_view())
             , name='novel'),

        path('chapter/<int:pk>/'
             , cache_page(60 * 240)(views.ChapterDetailView.as_view())
             , name='chapter')
    ]
