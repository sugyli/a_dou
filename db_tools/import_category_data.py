import sys
import os
import django



thispath = os.path.dirname(os.path.realpath(__file__))
parent_thispath = os.path.dirname(thispath)
sys.path.insert(0, parent_thispath)
sys.path.insert(0, os.path.join(parent_thispath, 'quanbenxiaoshuo'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from albums.models import Category
from db_tools.data.category_data import row_data

for lev1_cat in row_data:
    lev1_intance = Category()
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.title=lev1_cat["title"]
    lev1_intance.keywords=lev1_cat["keywords"]
    lev1_intance.description=lev1_cat["description"]
    lev1_intance.save()



#
# # #/Users/sugyil/quanbenxiaoshuo
# # #DJANGO_SETTINGS_MODULE = 'config.settings.production'
# sys.path.insert(0, DJANGO_PROJECT_PATH)
# #
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
# # #os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
# django.setup()
# #
# # from albums.models import Category
# # from db_tools.data.category_data import row_data
# # #
# # # for lev1_cat in row_data:
# # #     lev1_intance = Category()
# # #     lev1_intance.name = lev1_cat["name"]
# # #     lev1_intance.title=lev1_cat["title"]
# # #     lev1_intance.keywords=lev1_cat["keywords"]
# # #     lev1_intance.description=lev1_cat["description"]
# # #     lev1_intance.save()
# #
#


