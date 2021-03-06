import sys
import os
import django


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APPS_DIR)
sys.path.insert(0, os.path.join(APPS_DIR, 'quanbenxiaoshuo'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()


from albums.models import Category,Album
from db_tools.data.album_data import row_data

for lev1_cat in row_data:
    lev1_intance = Album()
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.title=lev1_cat["title"]
    lev1_intance.keywords=lev1_cat["keywords"]
    lev1_intance.description=lev1_cat["description"]
    lev1_intance.info=lev1_cat["info"]
    lev1_intance.is_tab=lev1_cat["is_tab"]
    lev1_intance.category= Category.objects.filter(name=lev1_cat["category"])[0]
    lev1_intance.save()




