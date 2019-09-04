import sys
import os
import django


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APPS_DIR)
sys.path.insert(0, os.path.join(APPS_DIR, 'quanbenxiaoshuo'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from novels.models import Chapter


data_file = \
    os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/urls.txt')

host = 'https://www.51xunyue.com'


#判断文件是否存在

if os.path.exists(data_file):
    print(f'{data_file} 文件存在可能没有提交请检查')
else:
    with open(data_file, 'w+') as f:
        chapters= \
            Chapter.objects.exclude(is_tab=True).filter(push=False).defer(
                'name')[:1999]

        for chapter in chapters:
            url=f'{host}{chapter.get_chapter_url()}\n'
            f.write(url)
            print(f"写入{url}")
            chapter.push=True
            chapter.save()



