from django import forms
from .models import Text,Csv

class liveTweetForm(forms.Form):
    live_tweet = forms.CharField(max_length=280, label="",widget=forms.TextInput(attrs={'placeholder': 'Enter any search query, #hashtag or @user_tag'}))
# class uploadFileForm(forms.Form):
#     uploaded_file = forms.FileField(max_length=100, label="")
# class typedTweetForm(forms.Form):
#     typed_tweet = forms.CharField(max_length=280, label="",widget=forms.TextInput(attrs={'placeholder': 'Type the text of your tweet here'}))

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
# class CsvForm(forms.ModelForm):
#     class Meta:
#         model = Csv
#         fields = ['tweets']
#         labels = {
#             'tweets': '',
#         }
    