# Generated by Django 3.2.5 on 2021-12-27 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_csvtweets_csv'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvtweets',
            name='tweetnum',
            field=models.IntegerField(null=True),
        ),
    ]
