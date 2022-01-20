from django.urls import path
from . import views

urlpatterns = [
    path('type/', views.text.as_view(), name='sentiment-type'),
    path('live/', views.liveTweet.as_view(), name='sentiment-live'),
    path('csv/', views.upload.as_view(), name='sentiment-csv'),
]