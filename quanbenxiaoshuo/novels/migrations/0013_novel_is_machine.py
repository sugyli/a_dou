# Generated by Django 2.2.2 on 2019-10-11 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0012_fenjuan'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='is_machine',
            field=models.BooleanField(default=False, help_text='是否采集提交', verbose_name='是否机器提交'),
        ),
    ]
