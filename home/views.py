from django.shortcuts import render
from django.views.generic import ListView, CreateView, View, TemplateView
from .models import Csv, CsvTweets
from .analyse_text import AnalysisText
from .analyse_csv import AnalysisCsv
from .analyse_live_tweet import AnalysisLiveTweet
from .forms import liveTweetForm, CsvModelForm, TextForm
from django.http import JsonResponse
import csv, pandas as pd


def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html', {'title': 'About'})
    
def textHistory(request):
    form = TextForm(request.POST or None)   
    if request.is_ajax():
        # form = TextForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data['text']
            text = form.save(commit=False)
            text.sentiment = AnalysisText.analyse(input)['sentiment']
            form.save()
            print(AnalysisText.analyse(input)['sentiment'])
            print(AnalysisText.analyse(input)['polarity'])

            # {'text': text, 'sentiment': res, 'polarity':polarity, 'dataArray': dataArray}


            # data['text']=input
            # data['sentiment']=res[0]
            # data['polarity']=res[1]
            return JsonResponse(AnalysisText.analyse(input), status=200)        
    context = {
        'form':form,
        'title':'Sentiment'
    }
    return render(request, 'home/sentiment_type.html', context)


def liveTweetTest(request):
    form = liveTweetForm(request.POST or None)
    if request.method == "POST":
        print(request.POST)
        if form.is_valid():
            live_tweet = form.cleaned_data['live_tweet']
            print(AnalysisLiveTweet.analyse(AnalysisLiveTweet, live_tweet)['sentiment'])
            print(AnalysisLiveTweet.analyse(AnalysisLiveTweet, live_tweet)['polarity'])


            data = AnalysisLiveTweet.analyse(AnalysisLiveTweet,live_tweet)
            # data['type']="live_tweet" 
            return JsonResponse(data, status=200)       
    print(request.POST)
    context = {
        'form':form,
        'title':'Sentiment'
    }
    return render(request, 'home/sentiment_type.html', context)

def uploadTest(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if request.is_ajax():
        print('started')
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'hell yeah'}, status=200)
        else:
            print('form not valid')
    else:
        print('nothing happened')        
    context = {
        'form':form,
        'title':'Sentiment'
    }
    return render(request, 'home/sentiment_type.html', context)

class SentimentAnalysisPage(TemplateView):
    template_name = 'home/sentiment_live_tweet.html'

    def get(self, request, *args, **kwargs):
        typeForm = TextForm()
        liveForm = liveTweetForm()
        uploadForm = CsvModelForm()

        return self.render_to_response({'typeForm':typeForm, 'liveForm': liveForm, 'uploadForm': uploadForm})
        
    def post(self, request, *args, **kwargs):
        # form = TextForm(request.POST or None)
        # if request.method == "POST":
        print(request.POST)
        if 'live_tweet' in request.POST:
            print('live_tweet')
            form = liveTweetForm(request.POST)
            if form.is_valid():
                # print(form)
                live_tweet = form.cleaned_data['live_tweet']
                print(AnalysisLiveTweet.analyse(AnalysisLiveTweet, live_tweet)['sentiment'])
                print(AnalysisLiveTweet.analyse(AnalysisLiveTweet, live_tweet)['polarity'])


                data = AnalysisLiveTweet.analyse(AnalysisLiveTweet,live_tweet)
                # data['type']="live_tweet" 
                return JsonResponse(data, status=200)
        elif "text" in request.POST:
            form = TextForm(request.POST)   
            if request.is_ajax():
                # form = TextForm(request.POST)
                if form.is_valid():
                    input = form.cleaned_data['text']
                    text = form.save(commit=False)
                    text.sentiment = AnalysisText.analyse(input)['sentiment'] #for model sheet
                    form.save()
                    print(AnalysisText.analyse(input)['sentiment'])
                    print(AnalysisText.analyse(input)['polarity'])

                    # {'text': text, 'sentiment': res, 'polarity':polarity, 'dataArray': dataArray}


                    # data['text']=input
                    # data['sentiment']=res[0]
                    # data['polarity']=res[1]

                    data = AnalysisText.analyse(input)
                    # data['type']="text"
                    return JsonResponse(data, status=200)
        elif 'file_name' in request.POST:
            form = CsvModelForm(request.POST, request.FILES)
            if request.is_ajax():
                print('started')
                if form.is_valid():
                    form.save()
                    # form = CsvModelForm()
                    # obj = Csv.objects.get(activated=False)
                    # with open(obj.file_name.path, 'r') as f:
                    #     reader = csv.reader(f)

                    #     for i, row in enumerate(reader):
                    #         if i != 0:
                    #             print(row)
                    #             print(type(row))
                    #             CsvTweets.objects.create(
                    #                 tweets="".join(row)
                    #             )
                    #     tweetObjs = CsvTweets.objects.filter(processed=False).values("tweets")
                    #     dataframe = pd.DataFrame(tweetObjs)
                    #     print(dataframe)

                    #     CsvTweets.objects.filter(processed=False).update(processed=True)
                    #     obj.activated = True
                    #     obj.save()
                        
                    #     data = AnalysisCsv.analyse(AnalysisCsv, dataframe)
                    #     print(AnalysisCsv.analyse(AnalysisCsv, dataframe)['sentiment'])
                    #     print(AnalysisCsv.analyse(AnalysisCsv, dataframe)['polarity'])
                    #     # data['type']="text"
                    #     return JsonResponse(data, status=200)
                    return JsonResponse({'message': 'hell yeah'}, status=200)
                else:
                    print('form not valid')
        else:
            print('nothing happened')        
        context = {
            'form':form,
            'title':'Sentiment'
        }
        return render(request, 'home/sentiment_live_tweet.html', context)