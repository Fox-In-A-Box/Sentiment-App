# Generated by Django 3.2.5 on 2021-12-15 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20211215_1337'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CsvTweet',
            new_name='CsvTweets',
        ),
    ]
