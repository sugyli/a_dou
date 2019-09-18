# Generated by Django 2.2.2 on 2019-09-18 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
        ('articles', '0007_auto_20190918_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='album',
        ),
        migrations.AddField(
            model_name='article',
            name='compose',
            field=models.ManyToManyField(blank=True, related_name='article_compose', to='operation.Compose', verbose_name='聚合'),
        ),
    ]
