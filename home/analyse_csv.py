import numpy as np
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
import re

class AnalysisCsv():
    def preprocess_tweets(self, tweet, custom_stopwords):
    #   Remove @user and links
        preprocessed_tweet = re.sub("(?:\@|https?\://)\S+|#|\n"," ",tweet).split()
        preprocessed_tweet = [word for word in preprocessed_tweet if word not in custom_stopwords]
        return(' '.join(preprocessed_tweet))

    def results(self, dataframe):
            if dataframe['Polarity'].iloc[0]<-0.05:
                return "Negative"
            elif dataframe['Polarity'].iloc[0]>0.05:
                return "Positive"
            else:
                return "Neutral"
    def rowResults(self, polarity):
            if polarity<-0.05:
                return "Negative"
            elif polarity>0.05:
                return "Positive"
            else:
                return "Neutral"
    def analyseRow(self, df):
        #Mia (MIA) discovered to have negative polarity score due to Vader lack of Name Recognition. Hence, included in stopwards
        custom_stopwords = ['RT', 'Mia']

        df['Processed Tweet'] = df['tweets'].apply(lambda x: self.preprocess_tweets(self, x, custom_stopwords))

        # calculate the mean of the polarity scores of each sentence in a tweet
        # polarity tested to be slightly more accurate when sentence is tokenised

        df['Polarity'] = df['Processed Tweet'].apply(lambda x: np.mean([analyzer.polarity_scores(x)['compound'] for sent in sent_tokenize(x)]))
        df['Sentiment'] = df['Polarity'].apply(lambda x: self.rowResults(self, x))
        
        sentiment =  df['Sentiment'].tolist()
        polarity = df['Polarity'].tolist()
        return {'sentiment': sentiment, 'polarity':polarity}

    def analyse(self, df):
        #Mia (MIA) discovered to have negative polarity score due to Vader lack of Name Recognition. Hence, included in stopwards
        custom_stopwords = ['RT', 'Mia']

        df['Processed Tweet'] = df['tweets'].apply(lambda x: self.preprocess_tweets(self, x, custom_stopwords))

        # calculate the mean of the polarity scores of each sentence in a tweet
        # polarity tested to be slightly more accurate when sentence is tokenised

        df['Polarity'] = df['Processed Tweet'].apply(lambda x: np.mean([analyzer.polarity_scores(x)['compound'] for sent in sent_tokenize(x)]))
        df['Neutral'] = df['Processed Tweet'].apply(lambda x: 1 if -0.05<=np.mean([analyzer.polarity_scores(x)['compound'] for sent in sent_tokenize(x)])<=0.05 else 0)
        df['Negative'] = df['Processed Tweet'].apply(lambda x: 1 if np.mean([analyzer.polarity_scores(x)['compound'] for sent in sent_tokenize(x)])<-0.05 else 0)
        df['Positive'] = df['Processed Tweet'].apply(lambda x: 1 if np.mean([analyzer.polarity_scores(x)['compound'] for sent in sent_tokenize(x)])>0.05 else 0)

        df2 = df[['Polarity', 'Neutral','Negative','Positive']].agg([np.mean])

        res = self.results(self, df2)
        polarity = df2['Polarity'].iloc[0]
        dataArray = [df2['Positive'].iloc[0], df2['Neutral'].iloc[0],df2['Negative'].iloc[0]]

        return {'sentiment': res, 'polarity':polarity, 'dataArray': dataArray}