from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from partisan.models import tweet, pie_chart_sentiment_stat
import json

def index(request):
  tpl = loader.get_template('main.html')
  context = {
    # Election stuff.
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
    ]),
    # US politics stuff.
    'positive_us_tweet': tweet.getSentimentTweet(searched_term='us politics', sentiment='positive'),
    'negative_us_tweet': tweet.getSentimentTweet(searched_term='us politics', sentiment='negative'),
    'neutral_us_tweet': tweet.getSentimentTweet(searched_term='us politics', sentiment='neutral'),
    'us_politics_pie_stats': json.dumps([
      {
        'label': 'Positive',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='us politics', sentiment='positive') * 100)
      },
      {
        'label': 'Negative',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='us politics', sentiment='negative') * 100)
      },
            {
        'label': 'Neutral',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='us politics', sentiment='neutral') * 100)
      },
      {
        'label': 'Mixed',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='us politics', sentiment='mixed') * 100)
      }
    ]),
    # UK politics stuff
    'positive_uk_tweet': tweet.getSentimentTweet(searched_term='uk politics', sentiment='positive'),
    'negative_uk_tweet': tweet.getSentimentTweet(searched_term='uk politics', sentiment='negative'),
    'neutral_uk_tweet': tweet.getSentimentTweet(searched_term='uk politics', sentiment='neutral'),
    'uk_politics_pie_stats': json.dumps([
      {
        'label': 'Positive',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='uk politics', sentiment='positive') * 100)
      },
      {
        'label': 'Negative',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='uk politics', sentiment='negative') * 100)
      },
            {
        'label': 'Neutral',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='uk politics', sentiment='neutral') * 100)
      },
      {
        'label': 'Mixed',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='uk politics', sentiment='mixed') * 100)
      }
    ]),
    # Covid stuff
    'positive_covid_tweet': tweet.getSentimentTweet(searched_term='covid', sentiment='positive'),
    'negative_covid_tweet': tweet.getSentimentTweet(searched_term='covid', sentiment='negative'),
    'neutral_covid_tweet': tweet.getSentimentTweet(searched_term='covid', sentiment='neutral'),
    'covid_pie_stats': json.dumps([
      {
        'label': 'Positive',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='covid', sentiment='positive') * 100)
      },
      {
        'label': 'Negative',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='covid', sentiment='negative') * 100)
      },
            {
        'label': 'Neutral',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='covid', sentiment='neutral') * 100)
      },
      {
        'label': 'Mixed',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term='covid', sentiment='mixed') * 100)
      }
    ]),
  }
  return HttpResponse(tpl.render(context, request))
