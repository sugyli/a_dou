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
    os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/day_bigdb_urls.txt')

host = 'https://www.51xunyue.com'






#判断文件是否存在

if os.path.exists(data_file):
    print(f'{data_file} 文件存在可能没有提交请检查')
else:

    chapters= \
        Chapter.objects.exclude(is_tab=True).filter(push=False).defer(
            'name')[:1999]

    if chapters.count():
        with open(data_file, 'w+') as f:
            for chapter in chapters:
                url=f'{host}{chapter.get_chapter_url()}\n'
                f.write(url)
                print(f"写入{url}")
                chapter.push=True
                chapter.save()
    else:
        print('数据库中没有可PUSH的数据不生成urls.txt文件')



