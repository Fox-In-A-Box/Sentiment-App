from rest_framework import serializers
from django.db import models
from .models import Text,LiveTweet, Csv, CsvTweets

from .analyse_text import AnalysisText
import csv

# data = {}

class TextSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=280, style={'base_template': 'input.html', 'placeholder': 'Enter any search query, #hashtag or @user_tag', 'hide_label': True})
    sentiment = serializers.CharField(max_length=10)
    polarity = serializers.FloatField()
    # dataArray = serializers.ListField()
    class Meta:
        model = Text
        fields = ['text','date_submitted','sentiment','polarity']

class LiveTweetSerializer(serializers.ModelSerializer):
    live_tweet = serializers.CharField(max_length=280, style={'base_template': 'input.html', 'placeholder': 'Enter any search query, #hashtag or @user_tag', 'hide_label': True})
    # sentiment = serializers.CharField(max_length=10)
    # polarity = serializers.FloatField()
    # dataArray = serializers.ListField()
    # MA = serializers.ListField()
    # MA_window = serializers.IntegerField()
    # MA_polarity = serializers.ListField()
    # MA_timestamps = serializers.ListField()

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
    csv_tweets= CsvTweetsforCsvSerializer(many=True, read_only=True)

    class Meta:
        model = Csv
        fields = ['id', 'file_name', 'uploaded','sentiment','polarity','csv_tweets']
        depth = 1