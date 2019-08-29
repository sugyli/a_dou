from django import template
from albums.models import Category
from quanbenxiaoshuo import helpers


register = template.Library()

@register.filter
def navigations(f):
    return Category.objects.all().defer('created_at')



@register.simple_tag
def description(n):
    return helpers.descriptionreplace(n)

