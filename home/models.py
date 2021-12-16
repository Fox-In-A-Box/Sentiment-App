from django.db import models
from django.utils import timezone
from .analyse_text import AnalysisText

class Text(models.Model):
    text = models.TextField(max_length=280)
    sentiment = models.CharField(max_length=10)
    date_submitted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Csv(models.Model):
    file_name = models.FileField(max_length=200,upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"

class CsvTweets(models.Model):
    tweets = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Tweet: {self.id}"
    
   