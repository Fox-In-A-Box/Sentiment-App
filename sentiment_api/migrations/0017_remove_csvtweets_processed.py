# Generated by Django 3.2.5 on 2022-01-01 00:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment_api', '0016_auto_20211231_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csvtweets',
            name='processed',
        ),
    ]
