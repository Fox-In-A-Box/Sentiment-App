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

class CsvSerializer(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField()

    # file_name = serializers.FileField(max_length=200,use_url=False)

    class Meta:
        model = Csv
        fields = ['id', 'file_name','activated', 'uploaded','sentiment','polarity']
        
class CsvTweetsSerializer(serializers.ModelSerializer):
    # csv_id = serializers.Field(source='csv.id')
    class Meta:
        model = Csv
        fields = ['tweets','created','processed','csv','tweetnum']
            # for i, row in enumerate(reader):
            #     if i != 0:
            #         print(row)
            #         print(type(row))
            #         CsvTweets.objects.create(
            #             tweets="".join(row),
            #             tweetnum=i
            #         )