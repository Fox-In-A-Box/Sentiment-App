from django import forms
from .models import Text, LiveTweet, Csv

class liveTweetForm(forms.ModelForm):
    class Meta:
        model = LiveTweet
        fields = ['live_tweet']
        labels = {
            'live_tweet': '',
        }
        widgets = {
            'live_tweet': forms.TextInput(attrs={'placeholder': 'Enter any search query, #hashtag or @user_tag'})
        }

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['text']
        labels = {
            'text': '',
        }
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Enter your text here...'})
        }
        
class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ['file_name']
        labels = {
            'file_name': '',
        }
    