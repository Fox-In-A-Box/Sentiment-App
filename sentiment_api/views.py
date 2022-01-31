from django.shortcuts import render
from django.views.generic import ListView, CreateView, View, TemplateView
import rest_framework
from rest_framework import serializers

from sentiment_api.serializers import TextSerializer
from .models import LiveTweet, Text, Csv, CsvTweets
from .analyse_text import AnalysisText
from .analyse_csv import AnalysisCsv
from .analyse_live_tweet import AnalysisLiveTweet
from .forms import liveTweetForm, CsvModelForm, TextForm
from .serializers import TextSerializer,LiveTweetSerializer,CsvSerializer,CsvTweetsSerializer 
from django.http import JsonResponse
import csv, pandas as pd

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status


class text(APIView):
    def post(self, request):
        data = request.data
        input = data['text']
        analysisData = AnalysisText.analyse(input)
        data['sentiment'] = analysisData['sentiment']
        data['polarity'] = analysisData['polarity']
        serializer = TextSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            newdict = serializer.data
            newdict.update({"dataArray": analysisData['dataArray']})

            return Response(newdict, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class liveTweet(APIView):
    def post(self, request):
        data = request.data
        input = data['live_tweet']
        analysisData = AnalysisLiveTweet.analyse(AnalysisLiveTweet, input)
        data['sentiment'] = analysisData['sentiment']
        data['polarity'] = analysisData['polarity']

        serializer = LiveTweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            newdict = serializer.data
            newdict.update({
                'dataArray': analysisData['dataArray'], 
                'MA':analysisData['MA'],
                'MA_polarity':analysisData['MA_polarity'], 
                'MA_timestamps': analysisData['MA_timestamps'],
                'word_frequency': analysisData['word_frequency'],
                'wordcloud_b64': analysisData['wordcloud_b64'],
                'wordcloud_mask_b64':analysisData['wordcloud_mask_b64'],
                })

            return Response(newdict, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class upload(generics.GenericAPIView, mixins.CreateModelMixin, mixins.RetrieveModelMixin ):
    serializer_class = CsvSerializer
    newdict = {}

    def get_object(self):
        try:
            return Csv.objects.latest('uploaded')
        except:
            pass

    def get(self, request):
        return self.retrieve(request)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        with open(instance.file_name.path, 'r', encoding='cp1252') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i != 0:
                    CsvTweets.objects.create(
                        tweets = "".join(row),
                        tweetnum=i,
                        csv=instance
                        )

        tweetObjs = CsvTweets.objects.filter(csv=instance).values("tweets")
        dataframe = pd.DataFrame(tweetObjs)

        rowData = AnalysisCsv.analyseRow(AnalysisCsv, dataframe)
        analysisData = AnalysisCsv.analyse(AnalysisCsv, dataframe)

        for i in range(CsvTweets.objects.filter(csv=instance).count()):
            CsvTweets.objects.filter(tweetnum=i+1).update(
                sentiment = rowData['sentiment'][i],
                polarity = rowData['polarity'][i]
                )
        serializer.save(sentiment=analysisData['sentiment'], polarity=analysisData['polarity'])
        self.newdict = serializer.data
        self.newdict.update({'dataArray': analysisData['dataArray']})

    def post(self, request):
        self.create(request)
        
        return Response(self.newdict, status=status.HTTP_201_CREATED)