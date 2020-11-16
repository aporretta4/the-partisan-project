from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from partisan.models import tweet
from random import randrange

def index(request):
  tpl = loader.get_template('main.html')
  positive_tweet = tweet.objects.filter(nlp_positive_sentiment__gt=0.95)
  negative_tweet = tweet.objects.filter(nlp_negative_sentiment__gt=0.95)
  neutral_tweet = tweet.objects.filter(nlp_neutral_sentiment__gt=0.95)
  context = {
    'positive_tweet': positive_tweet[randrange(positive_tweet.count())].text,
    'negative_tweet': negative_tweet[randrange(negative_tweet.count())].text,
    'neutral_tweet': neutral_tweet[randrange(neutral_tweet.count())].text
  }
  return HttpResponse(tpl.render(context, request))
