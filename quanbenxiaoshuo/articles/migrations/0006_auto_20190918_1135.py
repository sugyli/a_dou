# Generated by Django 2.2.2 on 2019-09-18 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_article_is_old'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='is_notice',
        ),
        migrations.RemoveField(
            model_name='article',
            name='is_old',
        ),
        migrations.AddField(
            model_name='article',
            name='datatype',
            field=models.CharField(choices=[('A', '老文章'), ('B', '公告'), ('C', '普通文章')], default='A', max_length=1, verbose_name='数据类型'),
        ),
        migrations.AlterField(
            model_name='article',
            name='keywords',
            field=models.CharField(blank=True, default='', help_text='keywords', max_length=255, null=True, verbose_name='关键字(seo)'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(blank=True, default='', help_text='title', max_length=255, null=True, verbose_name='标题(seo)'),
        ),
    ]