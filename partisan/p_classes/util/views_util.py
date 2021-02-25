from django.db import models
from partisan.models import pie_chart_sentiment_stat, data_sources, search_term, historical_sentiment_stat
from random import randrange
from datetime import datetime
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
  def getAggregateSentimentStatsByMonth(searched_term: str, sentiment_type: str, source: str):
    aggregate_stats = {}
    term = search_term.objects.filter(term=searched_term)
    if term.count() != 0:
      stats = historical_sentiment_stat.objects.filter(term_id=term[0].id, data_source=source).order_by('month_dt')
      if stats.count() != 0:
        for stat in stats:
          aggregate_stats[stat.month_dt.strftime('%b %Y')] = {
            'stat': getattr(stat, sentiment_type),
            'source': stat.data_source
          }
    return aggregate_stats

  @staticmethod
  def getHistoricalSMComparisonLineChartDict(sentiment_type: str, *term_names: str):
    stats = []
    datasets = []
    labels = []
    for term_name in term_names:
      stat_datapoints = sentiment_retriever.getAggregateSentimentStatsByMonth(
        term_name,
        sentiment_type
      )
      if stat_datapoints != False:
        stats.append(
          stat_datapoints
        )
        datasets.append({
          'label': data_sources.getSource(list(stat_datapoints)[0].source),
          'data': [data_point.stat for data_point in stat_datapoints]
        })
    biggest_len_index = 0
    for stat in stats:
      if len(stat) > biggest_len_index:
        biggest_len_index = len(stat)
    for month, stat in stats[biggest_len_index]:
      labels.append(month)
    return {
      'labels': labels,
      'datasets': datasets
    }


  @staticmethod
  def getSentimentPieChartDict(*term_names: str):
    stats = []
    for term_name in term_names:
      for stat in pie_chart_sentiment_stat.objects.filter(term__term=term_name):
        stats.append(stat)
    merged_stats = pie_chart_sentiment_stat.mergePieStats(*stats)
    return json.dumps([
      {
        'label': 'Positive',
        'value': str(merged_stats['positive'] * 100)
      },
      {
        'label': 'Negative',
        'value': str(merged_stats['negative'] * 100)
      },
            {
        'label': 'Neutral',
        'value': str(merged_stats['neutral'] * 100)
      },
      {
        'label': 'Mixed',
        'value': str(merged_stats['mixed'] * 100)
      }
    ])

  @staticmethod
  def getSentimentSocialMediaComparisonDict(*sentiment_stat_collection: pie_chart_sentiment_stat):
    data_sets = {}
    data_set_list = []
    for stat_collection in sentiment_stat_collection:
      if data_sources.getSource(stat_collection.data_source) != '':
        data_source = data_sources.getSource(stat_collection.data_source)
        data_sets[stat_collection.data_source] = {
          'label': data_source + ' Sentiment',
          'social_media_source': data_source,
          'data': [
            str(stat_collection.positive_sentiment_aggregate * 100),
            str(stat_collection.negative_sentiment_aggregate * 100),
            str(stat_collection.neutral_sentiment_aggregate * 100),
          ]
        }
    for data_set in data_sets.items():
      data_set_list.append(data_set[1])
    return json.dumps({
      'labels': ['Positive', 'Negative', 'Neutral'],
      'datasets': data_set_list
    })
