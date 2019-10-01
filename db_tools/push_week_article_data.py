import sys
import os
import django


APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APPS_DIR)
sys.path.insert(0, os.path.join(APPS_DIR, 'quanbenxiaoshuo'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from articles.models import Article



data_file = \
    os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/week_article_urls.txt')

host = 'https://www.51xunyue.com'


#判断文件是否存在

if os.path.exists(data_file):
    print(f'{data_file} 文件存在可能没有提交请检查')
else:

    articles = \
        Article.objects.get_published_no_user().filter(push=False).only('slug')[:2000]

    if articles.count():
        with open(data_file, 'w+') as f:
            for article in articles:
                url=f'{host}{article.get_article_url()}\n'
                f.write(url)
                print(f"写入{url}")
                article.push=True
                article.save()
    else:
        print('数据库中没有可PUSH的数据不生成week_article_urls.txt文件')



