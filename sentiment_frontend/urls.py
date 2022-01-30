from django.urls import path
from . import views

urlpatterns = [
    path('', views.sentiment_api, name='home'),
    path('about/', views.about, name='about'),
    path('emotion/', views.emotion, name='emotion'),
    path('sentiment/', views.SentimentAnalysisPage.as_view(), name='sentiment-all'),
]