# Generated by Django 2.2.2 on 2019-08-31 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0004_auto_20190831_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='push',
            field=models.BooleanField(default=False, help_text='是否已经推送给熊掌', verbose_name='推送'),
        ),
    ]