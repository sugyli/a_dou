from django import template
from albums.models import Category
#from categorys.models import Category
from quanbenxiaoshuo import helpers


register = template.Library()

@register.filter
def navigations(f):
    return Category.objects.get_published().defer('created_at')


# @register.filter
# def newnavigations(f):
#     return Category.objects.get_published().defer('created_at')



@register.simple_tag
def description(n):
    n=str(helpers.descriptionreplace(n))
    n=n[0:150]
    return n

