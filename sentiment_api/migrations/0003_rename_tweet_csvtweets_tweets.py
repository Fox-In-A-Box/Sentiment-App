# Generated by Django 3.2.5 on 2021-12-31 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment_api', '0002_alter_livetweet_sentiment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvtweets',
            old_name='tweet',
            new_name='tweets',
        ),
    ]
