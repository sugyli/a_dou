from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
import xadmin
#from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.views.decorators.cache import cache_page

from operation import views


if settings.DEBUG:
    urlpatterns = [
        #path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
        # path(
        #     "about/", TemplateView.as_view(template_name="403_csrf.html"), name="about"
        # ),
        # Django Admin, use {% url 'admin:index' %}
        #path(settings.ADMIN_URL, admin.site.urls),
        # User management
        # path("users/", include("quanbenxiaoshuo.users.urls", namespace="users")),
        # path("accounts/", include("allauth.urls")),

        # 开发的应用
        path('',views.IndexListView.as_view(), name='home'),#首页
        path('articles/', include('articles.urls', namespace='articles')),
        path('albums/', include('albums.urls', namespace='albums')),
        path('novels/', include('novels.urls', namespace='novels')),
        path('operation/', include('operation.urls', namespace='operation')),
        path('bigdbs/',include('bigdbs.urls', namespace='bigdbs')),
        path('categorys/',include('categorys.urls', namespace='categorys')),
        #富文本相关url
        path('ueditor/',include(('DjangoUeditor.urls', 'ueditor'), namespace="ueditor")),
        #后台
        path(settings.ADMIN_URL, xadmin.site.urls),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns=[
        # 开发的应用
        path('', cache_page(60 * 120)(views.IndexListView.as_view()), name='home'),
        # 首页
        path('articles/',
             include('articles.urls', namespace='articles')),

        path('albums/',
             include('albums.urls', namespace='albums')),

        path('novels/',
             include('novels.urls', namespace='novels')),

        path('operation/',
             include('operation.urls', namespace='operation')),

        path('bigdbs/',
             include('bigdbs.urls', namespace='bigdbs')),

        path('categorys/',
             include('categorys.urls', namespace='categorys')),

        # 富文本相关url
        path('ueditor/',
             include(('DjangoUeditor.urls', 'ueditor'), namespace="ueditor")),

        # 后台
        path(settings.ADMIN_URL, xadmin.site.urls),

    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
