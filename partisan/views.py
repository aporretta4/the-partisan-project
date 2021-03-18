from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from partisan.models import tweet, pie_chart_sentiment_stat, reddit_comment
from partisan.p_classes.util.views_util import sentiment_retriever

def index(request):
  tpl = loader.get_template('main.html')
  context = {
    'election': {},
    'us_politics': {},
    'uk_politics': {},
    'covid': {}
  }

  # Election
  context['election']['tw_examples'] = sentiment_retriever(sentimentable_model=tweet).getFullExampleDict(search_term='election', example_count=10)
  context['election']['sentiment_pie'] = sentiment_retriever.getSentimentPieChartDict('election')

  # US Politics
  context['us_politics']['tw_examples'] = sentiment_retriever(sentimentable_model=tweet).getFullExampleDict(search_term='us politics', example_count=10)
  context['us_politics']['re_examples'] = sentiment_retriever(sentimentable_model=reddit_comment).getFullExampleDict(search_term='r/politics', example_count=10)
  context['us_politics']['sentiment_pie'] = sentiment_retriever.getSentimentPieChartDict('r/politics', 'us politics')
  context['us_politics']['sm_comparison'] = sentiment_retriever.getSentimentSocialMediaComparisonDict(
    pie_chart_sentiment_stat.objects.get(term__term='r/politics'),
    pie_chart_sentiment_stat.objects.filter(term__term='us politics', data_source='tw')[0]
  )
    ### Historical Sentiment.
  context['us_politics']['historical_positive_comparison'] = sentiment_retriever.getHistoricalSentimentComparisonLineChartDict(
    [
      ('r/politics', 're'),
      ('us politics', 'tw')
    ],
    sentiment_type='positive_sentiment_aggregate'
  )
  context['us_politics']['historical_negative_comparison'] = sentiment_retriever.getHistoricalSentimentComparisonLineChartDict(
    [
      ('r/politics', 're'),
      ('us politics', 'tw')
    ],
    sentiment_type='negative_sentiment_aggregate'
  )

  # UK Politics
  context['uk_politics']['tw_examples'] = sentiment_retriever(sentimentable_model=tweet).getFullExampleDict(search_term='uk politics', example_count=10)
  context['uk_politics']['re_examples'] = sentiment_retriever(sentimentable_model=reddit_comment).getFullExampleDict(search_term='r/ukpolitics', example_count=10)
  context['uk_politics']['sentiment_pie'] = sentiment_retriever.getSentimentPieChartDict('r/ukpolitics', 'uk politics')
  context['uk_politics']['sm_comparison'] = sentiment_retriever.getSentimentSocialMediaComparisonDict(
    pie_chart_sentiment_stat.objects.get(term__term='r/ukpolitics'),
    pie_chart_sentiment_stat.objects.filter(term__term='uk politics', data_source='tw')[0]
  )

  ### Historical Sentiment.
  context['uk_politics']['historical_positive_comparison'] = sentiment_retriever.getHistoricalSentimentComparisonLineChartDict(
    [
      ('r/ukpolitics', 're'),
      ('uk politics', 'tw')
    ],
    sentiment_type='positive_sentiment_aggregate'
  )
  context['uk_politics']['historical_negative_comparison'] = sentiment_retriever.getHistoricalSentimentComparisonLineChartDict(
    [
      ('r/ukpolitics', 're'),
      ('uk politics', 'tw')
    ],
    sentiment_type='negative_sentiment_aggregate'
  )

  # Covid
  context['covid']['tw_examples'] = sentiment_retriever(sentimentable_model=tweet).getFullExampleDict(search_term='covid', example_count=10)
  context['covid']['re_examples'] = sentiment_retriever(sentimentable_model=reddit_comment).getFullExampleDict(search_term='r/Coronavirus', example_count=10)
  context['covid']['sentiment_pie'] = sentiment_retriever.getSentimentPieChartDict('r/Coronavirus', 'covid')
  context['covid']['sm_comparison'] = sentiment_retriever.getSentimentSocialMediaComparisonDict(
    pie_chart_sentiment_stat.objects.get(term__term='r/Coronavirus'),
    pie_chart_sentiment_stat.objects.filter(term__term='covid', data_source='tw')[0]
  )

  ### Historical Sentiment.
  context['covid']['historical_positive_comparison'] = sentiment_retriever.getHistoricalSentimentComparisonLineChartDict(
    [
      ('r/Coronavirus', 're'),
      ('covid', 'tw')
    ],
    sentiment_type='positive_sentiment_aggregate'
  )
  context['covid']['historical_negative_comparison'] = sentiment_retriever.getHistoricalSentimentComparisonLineChartDict(
    [
      ('r/Coronavirus', 're'),
      ('covid', 'tw')
    ],
    sentiment_type='negative_sentiment_aggregate'
  )

  return HttpResponse(tpl.render(context, request))