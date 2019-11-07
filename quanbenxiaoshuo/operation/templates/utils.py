from django import template
from django.conf import settings

from categorys.models import Category
from quanbenxiaoshuo import helpers

from sorl.thumbnail import get_thumbnail

register = template.Library()

@register.filter
def navigations(f):
    return Category.objects.get_published().defer('created_at')


@register.simple_tag
def description(n):
    n=str(helpers.descriptionreplace(n))
    n=n[0:150]
    return n

@register.simple_tag
def foramtThumbnail(image_url):
    image_url = image_url.replace(settings.MEDIA_URL, '')
    im=get_thumbnail(image_url, '200x200', crop='center', quality = 99)
    return im.url
