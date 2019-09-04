import sys
import os
import django


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APPS_DIR)
sys.path.insert(0, os.path.join(APPS_DIR, 'quanbenxiaoshuo'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from novels.models import Novel


data_file = \
    os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/novelurls.txt')

host = 'https://www.51xunyue.com'


#判断文件是否存在

if os.path.exists(data_file):
    print(f'{data_file} 文件存在可能没有提交请检查')
else:

    novels= \
        Novel.objects.get_published().filter(push=False).defer('name','info')[:10]

    if novels.count():
        with open(data_file, 'w+') as f:
            for novel in novels:
                url=f'{host}{novel.get_novel_url()}\n'
                f.write(url)
                print(f"写入{url}")
                novel.push=True
                novel.save()
    else:
        print('数据库中没有可PUSH的数据不生成urls.txt文件')



