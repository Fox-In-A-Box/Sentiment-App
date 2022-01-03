from django.urls import path
from . import views

urlpatterns = [
    path('', views.sentiment_api, name='home'),
    path('about/', views.about, name='about'),
    path('sentiment/', views.SentimentAnalysisPage.as_view(), name='sentiment-all'),
    # path('sentiment_type/', views.textTest.as_view(), name='sentiment-type'),
]