import sys
import os
import django


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APPS_DIR)
sys.path.insert(0, os.path.join(APPS_DIR, 'quanbenxiaoshuo'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()




data_file = \
    os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/urls.txt')



with open(data_file,'w+') as f:


    f.write('sss')



