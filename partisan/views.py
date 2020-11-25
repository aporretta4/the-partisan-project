from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from partisan.models import tweet, pie_chart_sentiment_stat
import json

def index(request):
  tpl = loader.get_template('main.html')
  context = {
    'positive_election_tweet': tweet.getSentimentTweet(searched_term='election', sentiment='positive'),
    'negative_election_tweet': tweet.getSentimentTweet(searched_term='election', sentiment='negative'),
    'neutral_election_tweet': tweet.getSentimentTweet(searched_term='election', sentiment='neutral'),
    'election_pie_stats': json.dumps([
      {
        'label': 'Positive',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='election', sentiment='positive') * 100)
      },
      {
        'label': 'Negative',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='election', sentiment='negative') * 100)
      },
            {
        'label': 'Neutral',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='election', sentiment='neutral') * 100)
      },
      {
        'label': 'Mixed',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='election', sentiment='mixed') * 100)
      }
    ])
  }
  return HttpResponse(tpl.render(context, request))
