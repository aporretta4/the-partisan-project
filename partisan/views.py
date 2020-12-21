from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from partisan.models import tweet
from partisan.p_classes.util.views_util import sentiment_retriever

def index(request):
  tpl = loader.get_template('main.html')
  context = {
    'election': {},
    'us_politics': {},
    'uk_politics': {},
    'covid': {}
  }
  context['election']['examples'] = sentiment_retriever(sentimentable_model=tweet).getFullExampleDict(search_term='election', example_count=10)
  context['election']['sentiment_pie'] = sentiment_retriever.getSentimentPieChartDict(term_name='election')
  context['us_politics']['examples'] = sentiment_retriever(sentimentable_model=tweet).getFullExampleDict(search_term='us politics', example_count=10)
  context['us_politics']['sentiment_pie'] = sentiment_retriever.getSentimentPieChartDict(term_name='us politics')
  context['uk_politics']['examples'] = sentiment_retriever(sentimentable_model=tweet).getFullExampleDict(search_term='uk politics', example_count=10)
  context['uk_politics']['sentiment_pie'] = sentiment_retriever.getSentimentPieChartDict(term_name='uk politics')
  context['covid']['examples'] = sentiment_retriever(sentimentable_model=tweet).getFullExampleDict(search_term='covid', example_count=10)
  context['covid']['sentiment_pie'] = sentiment_retriever.getSentimentPieChartDict(term_name='covid')
  return HttpResponse(tpl.render(context, request))
