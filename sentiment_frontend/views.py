from django.shortcuts import render
from django.views.generic import ListView, CreateView, View, TemplateView
import rest_framework
from rest_framework import serializers

# from sentiment_api.serializers import TextSerializer
# from .models import LiveTweet, Text, Csv, CsvTweets
# from .analyse_text import AnalysisText
# from .analyse_csv import AnalysisCsv
# from .analyse_live_tweet import AnalysisLiveTweet
# from .forms import liveTweetForm, CsvModelForm, TextForm
from sentiment_api.serializers import TextSerializer,LiveTweetSerializer,CsvSerializer,CsvTweetsSerializer 
from django.http import JsonResponse
import csv, pandas as pd

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status


def sentiment_api(request):
    return render(request, './home.html')

def about(request):
    return render(request, './about.html', {'title': 'About'})


# class text(APIView):
#         # renderer_classes = [textTemplateHTMLRender]
#         renderer_classes = [TemplateHTMLRenderer]
#         template_name = './sentiment_type.html'
#         style={'base_template': 'input.html', 'placeholder': 'Enter any search query, #hashtag or @user_tag', 'hide_label': True}

#     #     # def get(self, request):
#     #     #     tweets = Text.objects.all()
#     #     #     serializer = TextSerializer(tweets, many=True)
#     #     #     return Response(serializer.data)

#         def get(self, request, *args, **kwargs):
#             serializer = TextSerializer()
#             return Response({'serializer': serializer, 'style': self.style})


class SentimentAnalysisPage(APIView):
        renderer_classes = [TemplateHTMLRenderer]
        template_name = './sentiment_all_types.html'
        # intialise styles for each form input
        style={'base_template': 'input.html', 'placeholder': 'Enter your text here...', 'hide_label': True}
        style2={'base_template': 'input.html', 'placeholder': 'Enter any search query, #hashtag or @user_tag', 'hide_label': True}
        style3={'hide_label': True}

        def get(self, request, *args, **kwargs):
            # get serializers and pass them along with their corresponding style to the html to be rendered
            serializer = TextSerializer()
            serializer2 = LiveTweetSerializer()
            serializer3 = CsvSerializer()
            return Response({
                'serializer': serializer, 
                'serializer2': serializer2, 
                'serializer3': serializer3, 
                'style': self.style, 
                'style2': self.style2,
                'style3': self.style3,
                })
        
        # post request is handled by AJAX in main.js