import sys
import os
import django



APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APPS_DIR)
sys.path.insert(0, os.path.join(APPS_DIR, 'quanbenxiaoshuo'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()


from bigdbs.models import BigDb

bigdbs = BigDb.objects.all().order_by('id')
for bigdb in bigdbs:
    print(bigdb.id,' ',bigdb.name)
    bigdb.slug = str(bigdb.slug) + '-' + str(bigdb.id)
    bigdb.save()


