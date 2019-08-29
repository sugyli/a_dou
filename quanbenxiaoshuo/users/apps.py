from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "quanbenxiaoshuo.users"
    verbose_name = "用户管理"

    def ready(self):
        try:
            import quanbenxiaoshuo.users.signals  # noqa F401
        except ImportError:
            pass
