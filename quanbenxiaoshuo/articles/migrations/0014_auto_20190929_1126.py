# Generated by Django 2.2.2 on 2019-09-29 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0010_auto_20190929_0836'),
        ('articles', '0013_article_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='category_article', to='albums.Category', verbose_name='类别'),
        ),
    ]
