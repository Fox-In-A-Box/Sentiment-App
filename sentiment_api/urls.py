from django.urls import path
from . import views

urlpatterns = [
    path('type/', views.textTest.as_view(), name='sentiment-type'),
    path('live/', views.liveTweetTest.as_view(), name='sentiment-live'),
    path('csv/', views.uploadTest.as_view(), name='sentiment-csv'),
]