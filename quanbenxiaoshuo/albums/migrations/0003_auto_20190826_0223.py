# Generated by Django 2.2.2 on 2019-08-26 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_auto_20190825_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, unique=True, verbose_name='(URL)别名'),
        ),
    ]
