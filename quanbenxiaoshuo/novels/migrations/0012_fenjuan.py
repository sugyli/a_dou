# Generated by Django 2.2.2 on 2019-09-14 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0011_auto_20190910_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='FenJuan',
            fields=[
            ],
            options={
                'verbose_name': '分卷名',
                'verbose_name_plural': '分卷名',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('novels.chapter',),
        ),
    ]
