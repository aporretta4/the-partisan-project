import json
import logging
import requests
from requests.exceptions import HTTPError
from datetime import datetime
from urllib.parse import quote_plus
from django_project.settings import TW_BEARER_TOKEN
from partisan.models import tweet
from partisan.p_classes.nlp.aws_comprehend import comprehender

class twitter_processor:

    def __init__(self):
        super().__init__()

    def processTweets(self,process_number: int = 100):
      tweet_comprehender = comprehender()
      tweets = tweet.objects.filter(nlp_processed=False).order_by('id')[:process_number]
      tweet_list = list(tweets)
      text_list = [None] * tweets.count()
      processed_sentiment_list = []
      for i in range(tweets.count()):
        text_list[i] = tweet_list[i].text
      text_list = list(self.__chunk(text_list=text_list, n=25))
      for i in range(len(text_list)):
        sentiment_list = tweet_comprehender.comprehendText(text=text_list[i])
        for j in range(len(sentiment_list['ResultList'])):
          processed_sentiment_list.append(sentiment_list['ResultList'][j])
      for i in range(tweets.count()):
        tweets[i].nlp_processed = True
        if processed_sentiment_list[i]['SentimentScore']['Mixed'] < 0.25:
          tweet_list[i].nlp_neutral_sentiment = processed_sentiment_list[i]['SentimentScore']['Neutral']
          tweet_list[i].nlp_mixed_sentiment = processed_sentiment_list[i]['SentimentScore']['Mixed']
          tweet_list[i].nlp_negative_sentiment = processed_sentiment_list[i]['SentimentScore']['Negative']
          tweet_list[i].nlp_positive_sentiment = processed_sentiment_list[i]['SentimentScore']['Positive']
        tweet_list[i].save()

    def __chunk(self, text_list: list, n: int):
      for i in range(0, len(text_list), n):
        yield text_list[i:i + n]