# Generated by Django 2.2.2 on 2019-08-29 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0017_auto_20190829_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='content',
        ),
        migrations.AddField(
            model_name='content',
            name='chapter',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='chapter_content', to='novels.Chapter', verbose_name='小说章节'),
        ),
        migrations.AlterField(
            model_name='content',
            name='content',
            field=models.TextField(verbose_name='小说内容'),
        ),
    ]
