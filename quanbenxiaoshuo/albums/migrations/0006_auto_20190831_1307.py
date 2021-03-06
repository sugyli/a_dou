# Generated by Django 2.2.2 on 2019-08-31 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0005_auto_20190831_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='push',
            field=models.BooleanField(default=False, help_text='是否已经推送给熊掌', verbose_name='推送'),
        ),
        migrations.AlterField(
            model_name='category',
            name='push',
            field=models.BooleanField(default=False, help_text='是否已经推送给熊掌', verbose_name='推送'),
        ),
    ]
