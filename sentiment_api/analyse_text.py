import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
import re

class AnalysisText():
    def analyse(text):
        #Mia (MIA) discovered to have negative polarity score due to Vader lack of Name Recognition. Hence, included in stopwards
        custom_stopwords = ['RT', 'Mia']

        # Remove  @user, links, hashtags and  new lines from text
        preprocessed_tweet = re.sub("(?:\@|https?\://)\S+|#|\n"," ",text).split()
        # Remove stopwards
        preprocessed_tweet = [word for word in preprocessed_tweet if word not in custom_stopwords]
        # Turn list back into string
        newText = ' '.join(preprocessed_tweet)

        # calculate the mean of the polarity scores of each sentence in a tweet

        polarity = analyzer.polarity_scores(newText)['compound']
        dataArray = [analyzer.polarity_scores(newText)['pos'], 
                     analyzer.polarity_scores(newText)['neu'], 
                     analyzer.polarity_scores(newText)['neg']]
        
        # Determin sentiment based on polarity number
        if polarity<-0.05:
            res = "Negative"
        elif polarity>0.05:
            res = "Positive"
        else:
            res = "Neutral"
        
        return { 
            'sentiment': res, 
            'polarity':polarity, 
            'dataArray': dataArray
            }