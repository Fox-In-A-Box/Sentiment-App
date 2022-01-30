from django.shortcuts import render
from django.views.generic import ListView, CreateView, View, TemplateView
import rest_framework
from rest_framework import serializers

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

def emotion(request):
    return render(request, './coming_soon.html', {'title': 'Emotion'})


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