from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from partisan.models import tweet

def index(request):
  tpl = loader.get_template('main.html')
  context = {
    'positive_tweet': tweet.getSentimentTweet(searched_term='election', sentiment='positive'),
    'negative_tweet': tweet.getSentimentTweet(searched_term='election', sentiment='negative'),
    'neutral_tweet': tweet.getSentimentTweet(searched_term='election', sentiment='neutral')
  }
  return HttpResponse(tpl.render(context, request))
