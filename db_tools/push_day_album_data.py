import sys
import os
import django


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APPS_DIR)
sys.path.insert(0, os.path.join(APPS_DIR, 'quanbenxiaoshuo'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from albums.models import Album


data_file = \
    os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/day_album_urls.txt')

host = 'https://www.51xunyue.com'


#判断文件是否存在

if os.path.exists(data_file):
    print(f'{data_file} 文件存在可能没有提交请检查')
else:

    albums = \
        Album.objects.filter(push=False).defer('name','info')[:10]

    if albums.count():
        with open(data_file, 'w+') as f:
            for album in albums:
                url=f'{host}{album.get_album_url()}\n'
                f.write(url)
                print(f"写入{url}")
                album.push=True
                album.save()
    else:
        print('数据库中没有可PUSH的数据不生成day_album_urls.txt文件')



