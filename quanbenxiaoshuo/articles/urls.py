from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from articles import views

app_name = 'articles'

if settings.DEBUG:
    urlpatterns = [
        #path('', views.ArticlesListView.as_view(), name='list'),
        # path('write-new-article/', views.CreateArticleView.as_view(), name='write_new'),
        # path('drafts/', views.DraftsListView.as_view(), name='drafts'),
        path('<str:slug>/', views.DetailArticleView.as_view(), name='article'),
        # path('edit/<int:pk>/', views.EditArticleView.as_view(), name='edit_article'),
    ]
else:
    urlpatterns = [

        path('<str:slug>/'
             , cache_page(60 * 240)(views.DetailArticleView.as_view())
             , name='article'),

    ]
