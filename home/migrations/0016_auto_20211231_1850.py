# Generated by Django 3.2.5 on 2021-12-31 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20211231_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvtweets',
            name='polarity',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='csvtweets',
            name='sentiment',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
