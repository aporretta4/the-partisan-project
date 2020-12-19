from django.db import models
from partisan.models import pie_chart_sentiment_stat
from partisan.models import search_term
from random import randrange
import json

class sentiment_retriever:

  sentimentable_model = None

  def __init__(self, sentimentable_model: models.Model):
    self.sentimentable_model = sentimentable_model

  def getFullExampleDict(self, search_term: str):
    return {
      'positive': self.getExtremeSentimentExample(searched_term=search_term, sentiment='positive'),
      'negative': self.getExtremeSentimentExample(searched_term=search_term, sentiment='negative'),
      'neutral': self.getExtremeSentimentExample(searched_term=search_term, sentiment='neutral')
    }

  def getExtremeSentimentExample(self, searched_term: str, sentiment: str):
    term = search_term.objects.filter(term=searched_term)
    if term.count() != 0:
      if sentiment == 'positive':
        positive_example= self.sentimentable_model.objects.filter(term_id=term[0].id, nlp_positive_sentiment__gt=0.95)
        if positive_example.count() > 0:
          return positive_example[randrange(positive_example.count())].text
        else:
          return ''
      elif sentiment == 'negative':
        negative_example = self.sentimentable_model.objects.filter(term_id=term[0].id, nlp_negative_sentiment__gt=0.95)
        if negative_example.count() > 0:
          return negative_example[randrange(negative_example.count())].text
        else:
          return ''
      elif sentiment == 'neutral':
        neutral_example = self.sentimentable_model.objects.filter(term_id=term[0].id, nlp_neutral_sentiment__gt=0.95)
        if neutral_example.count() > 0:
          return neutral_example[randrange(neutral_example.count())].text
        else:
          return ''
      else:
        return ''
    else:
      return ''

  @staticmethod
  def getSentimentPieChartDict(term_name: str):
    return json.dumps([
      {
        'label': 'Positive',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term=term_name, sentiment='positive') * 100)
      },
      {
        'label': 'Negative',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term=term_name, sentiment='negative') * 100)
      },
            {
        'label': 'Neutral',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term=term_name, sentiment='neutral') * 100)
      },
      {
        'label': 'Mixed',
        'value': str(pie_chart_sentiment_stat.getStat(searched_term=term_name, sentiment='mixed') * 100)
      }
    ])