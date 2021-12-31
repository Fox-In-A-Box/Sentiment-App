from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='sentiment-home'),
    path('about/', views.about, name='sentiment-about'),
    # path('sentiment_type3/', views.uploadTest, name='sentiment-type'),
    path('sentiment_type3/', views.uploadTest.as_view(), name='sentiment-type'),
    # path('sentiment_type2/', views.textHistory, name='sentiment-type'),
    path('sentiment_type2/', views.textTest.as_view(), name='sentiment-type'),
    # path('sentiment_type/', views.liveTweetTest, name='sentiment-type'),
    path('sentiment_type/', views.liveTweetTest.as_view(), name='sentiment-live'),
    path('sentiment_live_tweet/', views.SentimentAnalysisPage.as_view(), name='sentiment-all'),
    # path('api/chart/data/', views.textHistory, name='api_chart_data'),
]