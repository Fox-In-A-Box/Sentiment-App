
# Twitter Sentiment Analyser

## Demo

![](demo.gif)


## About


This application analyses input text and returns its overall sentiment (whether the text is positive, negative, or neutral) with the use of NLTK.

Your text input can be in the form of a .csv file, a search query, or text you can manually enter yourself.

Live tweets are obtained from the Twitter API for use in finding the sentiment of 100 of the most recent tweets under the entered #hashtags, @user_handles or regular search query.

## Features

- Sentiment analysis of any manually typed tweets, live tweets or .csv file data
- Polarity charts showing how positive, negative, or neutral the input is
- Pie charts showing the distribution of the different sentiments throughout the input text as a percentage
- Wordcloud generation from list of 200 most common words for live tweets
- Written list of the top 5 most common words for live tweets
- Line charts of 10 tweet moving average of the most recent 100 tweets obtained from Twitter's feed


## Requirements

- Python 3.8.11+
- NLTK
- Pandas
- Django
- NumPy
- TweePy
- Python-DateUtils
