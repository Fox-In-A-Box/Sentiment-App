# Generated by Django 3.2.5 on 2021-12-15 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_rename_csvtweet_csvtweets'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvtweets',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
