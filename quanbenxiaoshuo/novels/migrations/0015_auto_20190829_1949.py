# Generated by Django 2.2.2 on 2019-08-29 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0014_auto_20190828_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='content',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='content_chapter', to='novels.Content', verbose_name='内容'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, verbose_name='(URL)别名'),
        ),
        migrations.AlterIndexTogether(
            name='content',
            index_together=set(),
        ),
        migrations.RemoveField(
            model_name='content',
            name='chapter',
        ),
    ]
