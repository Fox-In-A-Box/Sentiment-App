from rest_framework import serializers
from django.db import models
from .models import Text,LiveTweet, Csv, CsvTweets

from .analyse_text import AnalysisText
import csv

class TextSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=280, style={'base_template': 'input.html', 'placeholder': 'Enter your text here...', 'hide_label': True})
    sentiment = serializers.CharField(max_length=10)
    polarity = serializers.FloatField()
    class Meta:
        model = Text
        fields = ['text','date_submitted','sentiment','polarity']

class LiveTweetSerializer(serializers.ModelSerializer):
    live_tweet = serializers.CharField(max_length=280, style={'base_template': 'input.html', 'placeholder': 'Enter any search query, #hashtag or @user_tag', 'hide_label': True})

    class Meta:
        model = LiveTweet
        fields = ['live_tweet','date_submitted','sentiment','polarity', 'MA_window']

       
class CsvTweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvTweets
        fields = ['tweetnum','tweets','sentiment','polarity',]

class CsvTweetsforCsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvTweets
        fields = ['id','tweetnum','tweets','sentiment','polarity',]
        
class CsvSerializer(serializers.ModelSerializer):
    file_name = serializers.FileField(max_length=200, style={'hide_label': True})
    csv_tweets= CsvTweetsforCsvSerializer(many=True, read_only=True)

    class Meta:
        model = Csv
        fields = ['id', 'file_name', 'uploaded','sentiment','polarity','csv_tweets']
        depth = 1