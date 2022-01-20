import tweepy as tw
import numpy as np
import pandas as pd
import math
import nltk
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
import re
from datetime import datetime, timedelta
from dateutil.parser import parse

from nltk.corpus import stopwords
import string
from nltk import FreqDist
import contractions

from wordcloud import WordCloud, STOPWORDS
from collections import defaultdict

from PIL import Image
import os.path

# Keys necessary for twitter api to run
consumer_key = 'hllT6aKS7S6T0Qbw5uRzVdEBF'
consumer_secret = 'xcp1cz02UyGhZGLRPED1JSrKfTfjQKvoJ7JzTtnila64WUpCQ4'
access_token = '1259743528986517504-GVCAOVeK1L7PJtPrr7u8DqF7fReyD2'
access_token_secret = 'jfPtqGTdXBBXkJihJeyIN2hebN0fxTznIi43wXfM11T63'


class AnalysisLiveTweet():
    def preprocess_tweets(self, tweet):
        custom_stopwords = ['RT', 'Mia']
        #Mia (MIA) discovered to have negative polarity score due to Vader lack of Name Recognition. Hence, included in stopwards

        # Remove  @user, links, hashtags and  new lines from text
        preprocessed_tweet = re.sub("(?:\@|https?\://)\S+|#|\n"," ",tweet).split()
        # Remove stopwards
        preprocessed_tweet = [word for word in preprocessed_tweet if word not in custom_stopwords]
        # Turn list back into string
        return(' '.join(preprocessed_tweet))

    def wordcloud_tweets(self, tweet):
        custom_stopwords = ['rt','amp','&amp;']
        new_stopwords = ' '.join(list(STOPWORDS)).translate(str.maketrans('', '', string.punctuation)).split()
        stop_words = set(stopwords.words('english') + custom_stopwords + new_stopwords + list(string.ascii_lowercase))

 
        preprocessed_tweet = contractions.fix(tweet)
        preprocessed_tweet = re.sub("(?:\@|https?\://)\S+|www.\S+|#\S+|[^\x00-\x7f\xe9]+|\d+\S+|\d+"," ",tweet.lower())
        preprocessed_tweet = re.sub("\n"," ",preprocessed_tweet)

        preprocessed_tweet = preprocessed_tweet.translate(str.maketrans('', '', string.punctuation)).split()

        preprocessed_tweet = [word for word in preprocessed_tweet if not word.isdigit() if word not in stop_words]


        return(' '.join(preprocessed_tweet))

    def results(self, dataframe):
        # take polarity column from mean calculated dataframe and return the sentiment based on the polarity number
            if dataframe['Polarity'].iloc[0]<-0.05:
                return "Negative"
            elif dataframe['Polarity'].iloc[0]>0.05:
                return "Positive"
            else:
                return "Neutral"

    def analyse(self, text):
    # Necessary for twitter api functionality
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tw.API(auth, wait_on_rate_limit=True)

        searchTerm = text
        itemcount = 100;
        if searchTerm[0]=='@':
            query = tw.Cursor(api.user_timeline, screen_name=searchTerm[1:], include_rts = False, tweet_mode = 'extended').items(itemcount)
            tweets = [{'Tweets':tweet.full_text, 'Timestamp':parse(tweet.created_at.strftime('%H:%M:%S'))} for tweet in query]
        else:    
            query = tw.Cursor(api.search_tweets, q=searchTerm, lang='en', tweet_mode = 'extended').items(itemcount)
            tweets = [{'Tweets':tweet.full_text, 'Timestamp':parse(tweet.created_at.strftime('%H:%M:%S'))} for tweet in query]

    # Add milliseconds to any tweets that have the same timestamp so that they can be spaced better on moving average line graph
        add = 0
        tracker = {}
        for i,v in enumerate(tweets):
            if i>=1:
                # check if tweet timestamp is in tracker dict
                timestamp = str(tweets[i]['Timestamp'])
                if timestamp in tracker:
                    # if there is more than 1 entry in tweets dict with the same timestamp
                    if tracker[timestamp]>=1:
                        add += 40
                        tracker[timestamp]+=1
                        # add 40 milliseconds each time
                        tweets[i]['Timestamp'] = (tweets[i]['Timestamp'] + timedelta(milliseconds=add)).time()
                        
                else:
                    # reset addition amount
                    add=0
                    # add timestamp as key
                    tracker[timestamp]=1

# convert anytime that didn't have milliseconds added to it to a datetime.time()
        for i in range(len(tweets)):
            try:
                tweets[i]['Timestamp'] = (tweets[i]['Timestamp']).time()
            except:
                pass
        df = pd.DataFrame.from_dict(tweets)

        
        df['Processed Tweet'] = df['Tweets'].apply(lambda x: self.preprocess_tweets(self, x))
        df['Wordcloud Tweet'] = df['Tweets'].apply(lambda x: self.wordcloud_tweets(self, x))


        frequency = FreqDist(' '.join(df['Wordcloud Tweet'].tolist()).split())
        
        word_frequency = frequency.most_common(10)
        word_frequency_list = list(word_frequency)
        for word in word_frequency_list:
            if word[-1]=='s' and word.rstrip('s') in word_frequency:
                word_frequency[word.rstrip('s')]+=word_frequency[word]
                del word_frequency[word]

        script_dir = os.path.dirname(os.path.abspath(__file__))
        mask = np.array(Image.open(os.path.join(script_dir,'../static/images', 'twitter_mask.png')))
        
        wordcloud = WordCloud(
            width=800,
            mode="RGBA",
            height=400,
            max_words=200,
            background_color=None,
        ).generate(' '.join(df['Wordcloud Tweet'].tolist()))

        if os.path.exists(os.path.join(script_dir,'../static/images', 'wordcloud.png')):
            os.remove(os.path.join(script_dir,'../static/images', 'wordcloud.png'))
        wordcloud.to_file("static/images/wordcloud.png")

        wordcloud_mask = WordCloud(
            mask = mask,
            max_words=200,
            background_color="white",
        ).generate(' '.join(df['Wordcloud Tweet'].tolist()))

        wordcloud_mask.to_file("static/images/wordcloud_mask.png")
        


        # calculate the mean of the polarity scores of each sentence in a tweet
        # polarity tested to be slightly more accurate when sentence is tokenised

        df['Polarity'] = df['Processed Tweet'].apply(lambda x: np.mean([analyzer.polarity_scores(x)['compound'] for sent in sent_tokenize(x)]))
        df['Neutral'] = df['Processed Tweet'].apply(lambda x: 1 if -0.05<=np.mean([analyzer.polarity_scores(x)['compound'] for sent in sent_tokenize(x)])<=0.05 else 0)
        df['Negative'] = df['Processed Tweet'].apply(lambda x: 1 if np.mean([analyzer.polarity_scores(x)['compound'] for sent in sent_tokenize(x)])<-0.05 else 0)
        df['Positive'] = df['Processed Tweet'].apply(lambda x: 1 if np.mean([analyzer.polarity_scores(x)['compound'] for sent in sent_tokenize(x)])>0.05 else 0)

        df2 = df[['Polarity', 'Neutral','Negative','Positive']].agg([np.mean])


        # For Moving Average graph
        df['Polarity'] = df['Polarity'].fillna(0.0)
        visualMA = df[['Timestamp', 'Polarity']]
        visualMA = visualMA.sort_values(by='Timestamp', ascending=True)
        val=10
        visualMA['MA Polarity'] = visualMA.Polarity.rolling(val, min_periods=1).mean()

        # pos, neg or neu
        res = self.results(self, df2)
        # number
        polarity = df2['Polarity'].iloc[0]
        dataArray = [df2['Positive'].iloc[0], df2['Neutral'].iloc[0],df2['Negative'].iloc[0]]
        MA = visualMA['MA Polarity'].tolist()
        MA_timestamps = visualMA['Timestamp'].tolist()
        # print(MA)
        MA_original_polarity = visualMA['Polarity'].tolist()
        # print(MA_original_polarity)

        return { 
            'sentiment': res, 
            'polarity':polarity, 
            'dataArray': dataArray, 
            'MA':MA, 
            'MA_window': val, 
            'MA_polarity':MA_original_polarity, 
            'MA_timestamps': MA_timestamps,
            'word_frequency': word_frequency_list,
            }


        