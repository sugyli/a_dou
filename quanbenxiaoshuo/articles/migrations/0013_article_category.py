# Generated by Django 2.2.2 on 2019-09-29 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0010_auto_20190929_0836'),
        ('articles', '0012_remove_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='category_article', to='albums.Category', verbose_name='类别'),
        ),
    ]
