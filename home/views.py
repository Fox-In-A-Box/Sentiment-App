from django.shortcuts import render
from django.views.generic import ListView, CreateView, View, TemplateView
import rest_framework
from rest_framework import serializers

from home.serializers import TextSerializer
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
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html', {'title': 'About'})

# class textTestTemplateHTMLRender(TemplateHTMLRenderer):
#     def get_template_context(self, data, renderer_context):
#         data = super().get_template_context(data, renderer_context)
#         if not data:
#             return {}
#         else:
#             return data

class textTest(APIView):
    # renderer_classes = [textTestTemplateHTMLRender]
    # template_name = 'home/sentiment_type.html'
    # style={'base_template': 'input.html', 'placeholder': 'Enter any search query, #hashtag or @user_tag', 'hide_label': True}

    # def get(self, request):
    #     tweets = Text.objects.all()
    #     serializer = TextSerializer(tweets, many=True)
    #     return Response(serializer.data)

    # def get(self, request):
    #     serializer = TextSerializer()
    #     return Response({'serializer': serializer, 'style': self.style})

    def post(self, request):
    # print(request.POST)
        data = request.data
        input = data['text']
        analysisData = AnalysisText.analyse(input)
        data['sentiment'] = analysisData['sentiment']
        data['polarity'] = analysisData['polarity']

        serializer = TextSerializer(data=request.data)
        # if request.is_ajax():
        #     form = TextForm(request.POST)
        if serializer.is_valid():
            # input = serializer.validated_data['text']
            # data = AnalysisText.analyse(input)
            
            # print('got here')
            
            # serializer.validated_data['sentiment'] =  data['sentiment']
            # serializer.validated_data['polarity'] =  data['polarity']
            serializer.save()

            # print(data['sentiment'])
            # print(data['polarity'])
            print(serializer.data)
            newdict={"dataArray": analysisData['dataArray']}
            newdict.update(serializer.data)

            return Response(newdict, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    # context = {
    #     'serializer':serializer,
    #     'title':'Sentiment'
    # }
    
    # return render(request, 'home/sentiment_type.html', context)

    # Page with HTML
    # class textTest(APIView):
    #     # renderer_classes = [textTestTemplateHTMLRender]
    #     renderer_classes = [TemplateHTMLRenderer]
    #     template_name = 'home/sentiment_type.html'
    #     style={'base_template': 'input.html', 'placeholder': 'Enter any search query, #hashtag or @user_tag', 'hide_label': True}

    #     # def get(self, request):
    #     #     tweets = Text.objects.all()
    #     #     serializer = TextSerializer(tweets, many=True)
    #     #     return Response(serializer.data)

    #     def get(self, request, *args, **kwargs):
    #         serializer = TextSerializer()
    #         return Response({'serializer': serializer, 'style': self.style})

    #     def post(self, request, *args, **kwargs):
    #     # print(request.POST)
        
    #         data = request.data# remember old state
    #         _mutable = data._mutable

    #         # set to mutable
    #         data._mutable = True

    #         # сhange the values you want
    #         data['param_name'] = 'new value'

            
    #         input = data['text']
    #         analysisData = AnalysisText.analyse(input)
    #         data['sentiment'] = analysisData['sentiment']
    #         data['polarity'] = analysisData['polarity']
    #         # data['dataArray'] = analysisData['dataArray']

    #         # set mutable flag back
    #         data._mutable = _mutable

    #         serializer = TextSerializer(data=request.data)
    #         if request.is_ajax():
    #             if serializer.is_valid():
    #                 # input = serializer.validated_data['text']
    #                 # data = AnalysisText.analyse(input)
                    
    #                 # print('got here')
                    
    #                 # serializer.validated_data['sentiment'] =  data['sentiment']
    #                 # serializer.validated_data['polarity'] =  data['polarity']
    #                 serializer.save()

    #                 # print(data['sentiment'])
    #                 # print(data['polarity'])
    #                 print(serializer.data)
    #                 newdict={"dataArray": analysisData['dataArray']}
    #                 newdict.update(serializer.data)

    #                 # return Response(newdict, status=status.HTTP_201_CREATED)    
    #                 return JsonResponse(newdict, status=status.HTTP_201_CREATED)    
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class liveTweetTest(APIView):
    def post(self, request):
        data = request.data
        input = data['live_tweet']
        analysisData = AnalysisLiveTweet.analyse(AnalysisLiveTweet, input)
        data['sentiment'] = analysisData['sentiment']
        data['polarity'] = analysisData['polarity']

        serializer = LiveTweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            newdict={
                'dataArray': analysisData['dataArray'], 
                'MA':analysisData['MA'],
                'MA_polarity':analysisData['MA_polarity'], 
                'MA_timestamps': analysisData['MA_timestamps']
                }
            newdict.update(serializer.data)

            return Response(newdict, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        # form = liveTweetForm(request.POST or None)
        # if request.method == "POST":
        #     print(request.POST)
        #     if form.is_valid():
        #         live_tweet = form.cleaned_data['live_tweet']
        #         print(AnalysisLiveTweet.analyse(AnalysisLiveTweet, live_tweet)['sentiment'])
        #         print(AnalysisLiveTweet.analyse(AnalysisLiveTweet, live_tweet)['polarity'])


        #         data = AnalysisLiveTweet.analyse(AnalysisLiveTweet,live_tweet)
        #         # data['type']="live_tweet" 
        #         return JsonResponse(data, status=200)       
        # print(request.POST)
        # context = {
        #     'form':form,
        #     'title':'Sentiment'
        # }
        # return render(request, 'home/sentiment_type.html', context)


# def liveTweetTest(request):
#     form = liveTweetForm(request.POST or None)
#     if request.method == "POST":
#         print(request.POST)
#         if form.is_valid():
#             live_tweet = form.cleaned_data['live_tweet']
#             print(AnalysisLiveTweet.analyse(AnalysisLiveTweet, live_tweet)['sentiment'])
#             print(AnalysisLiveTweet.analyse(AnalysisLiveTweet, live_tweet)['polarity'])


#             data = AnalysisLiveTweet.analyse(AnalysisLiveTweet,live_tweet)
#             # data['type']="live_tweet" 
#             return JsonResponse(data, status=200)       
#     print(request.POST)
#     context = {
#         'form':form,
#         'title':'Sentiment'
#     }
#     return render(request, 'home/sentiment_type.html', context)

class uploadTest(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = CsvSerializer
    queryset = Csv.objects.all()


    def perform_create(self, serializer):
        instance = serializer.save()
        with open(instance.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i != 0:
                    CsvTweets.objects.create(
                        tweets = "".join(row),
                        tweetnum=i,
                        csv=instance
                        )

        tweetObjs = CsvTweets.objects.filter(processed=False).values("tweets")
        dataframe = pd.DataFrame(tweetObjs)
        # print(dataframe)
        

        CsvTweets.objects.filter(processed=False).update(processed=True)
        analysisData = AnalysisCsv.analyse(AnalysisCsv, dataframe)
        serializer.save(activated=True,sentiment=analysisData['sentiment'], polarity=analysisData['polarity'])
        # newdict={
        #     'dataArray': analysisData['dataArray'],
        #     }
        # newdict.update(serializer.data)
    def post(self, request):
        
        

        #     return Response(newdict, status=status.HTTP_201_CREATED)    
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return self.create(request)






# def uploadTest(request):
#     form = CsvModelForm(request.POST or None, request.FILES or None)
#     if request.is_ajax():
#         print('started')
#         if form.is_valid():
#             form.save()
#             obj = Csv.objects.get(activated=False)
#             with open(obj.file_name.path, 'r') as f:
#                 reader = csv.reader(f)

#                 for i, row in enumerate(reader):
#                     if i != 0:
#                         print(row)
#                         print(type(row))
#                         CsvTweets.objects.create(
#                             tweets="".join(row)
#                         )
#                 tweetObjs = CsvTweets.objects.filter(processed=False).values("tweets")
#                 dataframe = pd.DataFrame(tweetObjs)
#                 print(dataframe)

#                 CsvTweets.objects.filter(processed=False).update(processed=True)
#                 obj.activated = True
#                 obj.save()
                
#                 data = AnalysisCsv.analyse(AnalysisCsv, dataframe)
#                 print(AnalysisCsv.analyse(AnalysisCsv, dataframe)['sentiment'])
#                 print(AnalysisCsv.analyse(AnalysisCsv, dataframe)['polarity'])
#                 # data['type']="text"
#                 return JsonResponse(data, status=200)
#             print('form not valid')
#     else:
#         print('nothing happened')        
#     context = {
#         'form':form,
#         'title':'Sentiment'
#     }
#     return render(request, 'home/sentiment_type.html', context)


class textSentimentAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = CsvSerializer
    queryset = Csv.objects.all()
    def perform_create(self, serializer):
        data = request.data
        input = data['text']
        analysisData = AnalysisText.analyse(input)
        data['sentiment'] = analysisData['sentiment']
        data['polarity'] = analysisData['polarity']
        serializer.save()
    def post(self, request):
    # print(request.POST)
        

        serializer = TextSerializer(data=request.data)
        # if request.is_ajax():
        #     form = TextForm(request.POST)
        if serializer.is_valid():
            # input = serializer.validated_data['text']
            # data = AnalysisText.analyse(input)
            
            # print('got here')
            
            # serializer.validated_data['sentiment'] =  data['sentiment']
            # serializer.validated_data['polarity'] =  data['polarity']
            serializer.save()

            # print(data['sentiment'])
            # print(data['polarity'])
            print(serializer.data)
            newdict={"dataArray": analysisData['dataArray']}
            newdict.update(serializer.data)

            return Response(newdict, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class SentimentAnalysisPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home/sentiment_live_tweet.html'

    def get(self, request):
        # type = get_object_or_404(Text, pk=pk)
        # live = get_object_or_404(LiveTweet, pk=pk)
        # upload = get_object_or_404(Csv, pk=pk)
        typeSerializer = TextSerializer()
        livetweetSerializer = LiveTweetSerializer()
        uploadSerializer= CsvSerializer()

        return Response({'typeSerialiser':typeSerializer, 'livetweetSerializer': livetweetSerializer, 'uploadSerializer': uploadSerializer})
        
    def post(self, request):
        serializer = TextSerializer(request.data or None)
        # if request.method == "POST":
        # print(request.POST)
        if "text" in request.data:
            serializer = TextSerializer(request.data)   
            if request.is_ajax():
                # form = TextForm(request.POST)
                if serializer.is_valid():
                    input = serializer.validated_data['text']
                    data = AnalysisText.analyse(input)
                    text = serializer.save(commit=False)
                    
                    text.sentiment = data['sentiment'] #for model sheet, displays on admin page
                    text.polarity = data['polarity'] 
                    text.dataArray = data['dataArray']
                    serializer.save()

                    print(data['sentiment'])
                    print(data['polarity'])

                    return Response(data, status=status.HTTP_201_CREATED)
        elif 'live_tweet' in request.data:
            print('live_tweet')
            serializer = LiveTweetSerializer(request.data)
            # form = liveTweetForm(request.POST)
            if serializer.is_valid():
                # print(form)
                input = serializer.validated_data['live_tweet']
                data = AnalysisLiveTweet.analyse(AnalysisLiveTweet,input)
                live_tweet = serializer.save(commit=False)

                live_tweet.sentiment = data['sentiment'] #for model sheet, displays on admin page
                live_tweet.polarity = data['polarity'] 
                live_tweet.dataArray = data['dataArray'] 
                live_tweet.MA = data['MA'] 
                live_tweet.MA_window = data['MA_window'] 
                live_tweet.MA_polarity = data['MA_polarity'] 
                live_tweet.MA_timestamps = data['MA_timestamps'] 

                serializer.save() 

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = CsvSerializer(request.data or None)
            if request.is_ajax():
                print('started')
                if serializer.is_valid():
                    serializer.save()
                    # obj = Csv.objects.get(activated=False)
                    # with open(obj.file_name.path, 'r') as f:
                    #     reader = csv.reader(f)

                    #     for i, row in enumerate(reader):
                    #         if i != 0:
                    #             print(row)
                    #             print(type(row))
                    #             CsvTweets.objects.create(
                    #                 tweets="".join(row),
                    #                 tweetnum=i
                    #             )
                    print('works up to here')
                    tweetObjs = CsvTweets.objects.filter(processed=False).values("tweets")
                    dataframe = pd.DataFrame(tweetObjs)
                    print(dataframe)

                    CsvTweets.objects.filter(processed=False).update(processed=True)
                    # obj.activated = True
                    # obj.save()
                    
                    data = AnalysisCsv.analyse(AnalysisCsv, dataframe)
                    upload = serializer.save(commit=False)
                    upload.sentiment = data['sentiment'] #for model sheet, displays on admin page
                    upload.polarity = data['polarity'] 
                    upload.dataArray = data['dataArray']
                    serializer.save()

                    print(data['sentiment'])
                    print(data['polarity'])
                    # data['type']="text"
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                #     return JsonResponse({'message': 'hell yeah'}, status=200)
                # else:
                #     print('form not valid')
        # else:
        #     print('nothing happened')        
        # context = {
        #     'serializer':serializer,
        #     'title':'Sentiment'
        # }
        # return render(request, 'home/sentiment_live_tweet.html', context)