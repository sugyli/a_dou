import sys
import os
import django


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APPS_DIR)
sys.path.insert(0, os.path.join(APPS_DIR, 'quanbenxiaoshuo'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from bigdbs.models import BigDb


data_file = \
    os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/week_bigdb_urls.txt')

host = 'https://www.home520.com'


#判断文件是否存在

if os.path.exists(data_file):
    print(f'{data_file} 文件存在可能没有提交请检查')
else:

    bigdbs = \
        BigDb.objects.get_published().filter(push=False).only('slug')[:2000]

    if bigdbs.count():
        with open(data_file, 'w+') as f:
            for bigdb in bigdbs:
                url=f'{host}{bigdb.get_url()}\n'
                f.write(url)
                print(f"写入{url}")
                bigdb.push=True
                bigdb.save()
    else:
        print('数据库中没有可PUSH的数据不生成week_bigdb_urls.txt文件')



