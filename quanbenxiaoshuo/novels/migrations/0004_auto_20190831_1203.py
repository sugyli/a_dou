# Generated by Django 2.2.2 on 2019-08-31 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0003_auto_20190831_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='description',
            field=models.CharField(blank=True, default='', help_text='description', max_length=255, null=True, verbose_name='描述(seo)'),
        ),
    ]
