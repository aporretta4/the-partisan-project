from django.db import models
from partisan.models import pie_chart_sentiment_stat
from partisan.models import search_term
from random import randrange
import json

class sentiment_retriever:

  sentimentable_model = None

  def __init__(self, sentimentable_model: models.Model):
    self.sentimentable_model = sentimentable_model

  def getFullExampleDict(self, search_term: str, example_count: int = 1):
    pos_list = []
    neg_list = []
    neut_list = []
    pos_items = self.getExtremeSentimentExamples(searched_term=search_term, sentiment='positive', count=example_count)
    neg_items = self.getExtremeSentimentExamples(searched_term=search_term, sentiment='negative', count=example_count)
    neut_items = self.getExtremeSentimentExamples(searched_term=search_term, sentiment='neutral', count=example_count)
    if len(pos_items) != 0:
      for item in pos_items:
        pos_list.append(item.text)
    if len(neg_items) != 0:
      for item in neg_items:
        neg_list.append(item.text)
    if len(neut_items) != 0:
      for item in neut_items:
        neut_list.append(item.text)
    return {
      'positive': pos_list,
      'negative': neg_list,
      'neutral': neut_list,
    }

  def getExtremeSentimentExamples(self, searched_term: str, sentiment: str, count: int = 1):
    term = search_term.objects.filter(term=searched_term)
    if term.count() != 0:
      if sentiment == 'positive':
        positive_example = self.sentimentable_model.objects.filter(term_id=term[0].id, nlp_positive_sentiment__gt=0.9).order_by('-created_at')
        if positive_example.count() > 0:
          if count != 1 and count <= positive_example.count():
            return positive_example[0:count]
          else:
            return [positive_example[randrange(positive_example.count())]]
        else:
          return []
      elif sentiment == 'negative':
        negative_example = self.sentimentable_model.objects.filter(term_id=term[0].id, nlp_negative_sentiment__gt=0.9).order_by('-created_at')
        if negative_example.count() > 0:
          if count != 1 and count <= negative_example.count():
            return negative_example[0:count]
          else:
            return [negative_example[randrange(negative_example.count())]]
        else:
          return []
      elif sentiment == 'neutral':
        neutral_example = self.sentimentable_model.objects.filter(term_id=term[0].id, nlp_neutral_sentiment__gt=0.9).order_by('-created_at')
        if neutral_example.count() > 0:
          if count != 1 and count <= neutral_example.count():
            return neutral_example[0:count]
          else:
            return [neutral_example[randrange(neutral_example.count())]]
        else:
          return []
      else:
        return []
    else:
      return []

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