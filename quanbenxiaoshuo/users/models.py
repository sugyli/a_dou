# from django.contrib.auth.models import AbstractUser
# from django.db.models import CharField
# from django.urls import reverse
# from django.utils.translation import ugettext_lazy as _


from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.urls import reverse


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    nickname = models.CharField(max_length=255,null=True, blank=True,verbose_name='昵称')


    def get_nickname(self):
        if self.nickname:
            return self.nickname
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
