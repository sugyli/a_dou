# Generated by Django 2.2.2 on 2019-09-16 22:05

from django.db import migrations, models
import quanbenxiaoshuo.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='标题')),
                ('image', models.ImageField(blank=True, null=True, storage=quanbenxiaoshuo.storage.ImageStorage(), upload_to='compose/%Y/%m', verbose_name='聚合封面')),
                ('info', models.TextField(verbose_name='简介')),
                ('slug', models.SlugField(blank=True, default='', max_length=255, unique=True, verbose_name='(URL)别名')),
                ('title', models.CharField(default='', help_text='title', max_length=255, verbose_name='标题(seo)')),
                ('keywords', models.CharField(default='', help_text='keywords', max_length=255, verbose_name='关键字(seo)')),
                ('description', models.CharField(blank=True, default='', help_text='description', max_length=255, null=True, verbose_name='描述(seo)')),
                ('push', models.BooleanField(default=False, help_text='是否已经推送给熊掌', verbose_name='推送')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '聚合',
                'verbose_name_plural': '聚合',
                'ordering': ('-updated_at',),
            },
        ),
    ]
