from django.contrib import admin
from .models import CsvTweets, Text, Csv

admin.site.register(Text)
admin.site.register(Csv)
admin.site.register(CsvTweets)
