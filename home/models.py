from django.db import models
from django.utils import timezone
from .analyse_text import AnalysisText

class Text(models.Model):
    text = models.CharField(max_length=280)
    date_submitted = models.DateTimeField(default=timezone.now)
    polarity = models.FloatField(null=True)
    sentiment = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.text
class LiveTweet(models.Model):
    live_tweet = models.CharField(max_length=280)
    sentiment = models.CharField(max_length=10,null=True)
    polarity = models.FloatField(null=True)
    MA_window = models.IntegerField(default=10)
    date_submitted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.live_tweet

class Csv(models.Model):
    file_name = models.FileField(max_length=200,upload_to='csvs')
    sentiment = models.CharField(max_length=10, null=True)
    polarity = models.FloatField(null=True)
    activated = models.BooleanField(default=False)
    uploaded = models.DateTimeField(auto_now_add=True)
    # activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File ID: {self.id}"

class CsvTweets(models.Model):
    tweets = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    csv = models.ForeignKey(Csv,on_delete=models.CASCADE,null=True)
    tweetnum = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.csv}, Tweet: {self.tweetnum}"
    
   