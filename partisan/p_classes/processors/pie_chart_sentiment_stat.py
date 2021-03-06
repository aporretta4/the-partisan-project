from django.db.models.query import QuerySet
from partisan.models import pie_chart_sentiment_stat, search_term, news
from partisan.p_classes.exceptions.DataExceptions import DataSourceNotFoundException
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Model
from django.db import transaction
import decimal
import logging

class stat_processor:

  @staticmethod
  def processModelStats(searched_term: str, sentimentable_model: Model, batch: int):
    success = False
    unprocessed_stats = sentimentable_model.objects.filter(pie_stat_processed=False, nlp_processed=True, term__term=searched_term)[:batch]
    if unprocessed_stats.count() > 0:
      success = stat_processor.calculateStats(
        searched_term=searched_term,
        unprocessed_stats=unprocessed_stats,
        source=stat_processor.getSentimentableDataSource(sentimentable_model=sentimentable_model),
        sentimentable_model=sentimentable_model
      )
      if success == False:
        return success
    else:
      success = True
    return success

  @staticmethod
  def processNewsStats(searched_term: str, batch: int):
    success = False
    unprocessed_news_outlets = news.objects.filter(pie_stat_processed=False, nlp_processed=True, term__term=searched_term).values('news_outlet__outlet_name').distinct()
    if unprocessed_news_outlets.count() == 0:
      success = True
    for unprocessed_news_outlet in unprocessed_news_outlets:
      outlet_name = unprocessed_news_outlet['news_outlet__outlet_name']
      unprocessed_news = news.objects.filter(pie_stat_processed=False, nlp_processed=True, news_outlet__outlet_name=outlet_name, term__term=searched_term)[:batch]
      if len(unprocessed_news) > 0:
        success = stat_processor.calculateStats(
          searched_term=searched_term,
          unprocessed_stats=unprocessed_news,
          source=stat_processor.getNewsSourceKey(news_source=outlet_name),
          sentimentable_model=news
        )
        if success == False:
          return success
      else:
        success = True
    return success

  @staticmethod
  def getSentimentableDataSource(sentimentable_model: Model):
    if sentimentable_model.__name__ == 'tweet':
      return 'tw'
    elif sentimentable_model.__name__ == 'reddit_submission' or sentimentable_model.__name__ == 'reddit_comment':
      return 're'
    else:
      DataSourceNotFoundException('A news source could not be determined when processing pie chart stats. The name of the model is is: ' + sentimentable_model.__name__)

  @staticmethod
  def getNewsSourceKey(news_source: str):
    if news_source == 'www.nytimes.com':
      return 'nt'
    else:
      DataSourceNotFoundException('A news source could not be determined when processing pie chart stats. The news source full name is: ' + news_source)

  @staticmethod
  def calculateStats(searched_term: str, unprocessed_stats: QuerySet, source: str, sentimentable_model: Model):
    try:
      term = search_term.objects.get(term=searched_term)
      if unprocessed_stats.count() == 0:
        return True
      processed_weight = stat_processor.processDataWeight(
        searched_term_id=term.id,
        data_source=source,
        new_record_count=unprocessed_stats.count(),
        new_data=False
      )
      unprocessed_weight = stat_processor.processDataWeight(
        searched_term_id=term.id,
        data_source=source,
        new_record_count=unprocessed_stats.count()
      )
      new_neutral_avg = round(unprocessed_stats.aggregate(Avg('nlp_neutral_sentiment'))['nlp_neutral_sentiment__avg'], 5)
      new_mixed_avg = round(unprocessed_stats.aggregate(Avg('nlp_mixed_sentiment'))['nlp_mixed_sentiment__avg'], 5)
      new_positive_avg = round(unprocessed_stats.aggregate(Avg('nlp_positive_sentiment'))['nlp_positive_sentiment__avg'], 5)
      new_negative_avg = round(unprocessed_stats.aggregate(Avg('nlp_negative_sentiment'))['nlp_negative_sentiment__avg'], 5)
      if processed_weight == 0:
        with transaction.atomic():
          sentiment_stat = pie_chart_sentiment_stat(
            neutral_sentiment_aggregate=new_neutral_avg,
            mixed_sentiment_aggregate=new_mixed_avg,
            positive_sentiment_aggregate=new_positive_avg,
            negative_sentiment_aggregate=new_negative_avg,
            processed_records_count=unprocessed_stats.count(),
            term_id=term.id,
            data_source=source
          )
          sentiment_stat.save()
          sentimentable_model.objects.filter(id__in=list(unprocessed_stats.values_list('id', flat=True))).update(pie_stat_processed=True)
          return True
      else:
        try:
          with transaction.atomic():
            old_stats = pie_chart_sentiment_stat.objects.get(term_id=term.id, data_source=source)
            old_stats.neutral_sentiment_aggregate = (processed_weight * old_stats.neutral_sentiment_aggregate) + (unprocessed_weight * new_neutral_avg)
            old_stats.mixed_sentiment_aggregate = (processed_weight * old_stats.mixed_sentiment_aggregate) + (unprocessed_weight * new_mixed_avg)
            old_stats.positive_sentiment_aggregate = (processed_weight * old_stats.positive_sentiment_aggregate) + (unprocessed_weight * new_positive_avg)
            old_stats.negative_sentiment_aggregate = (processed_weight * old_stats.negative_sentiment_aggregate) + (unprocessed_weight * new_negative_avg)
            old_stats.processed_records_count = old_stats.processed_records_count + unprocessed_stats.count()
            old_stats.save()
            sentimentable_model.objects.filter(id__in=list(unprocessed_stats.values_list('id', flat=True))).update(pie_stat_processed=True)
            return True
        except ObjectDoesNotExist as ex_stat:
          print('Error! The term ' + searched_term + ' does not exist when looking for existing aggregate stats! Exception: ' + str(ex_stat))
          logging.error('Error! The term ' + searched_term + ' does not exist when looking for existing aggregate stats! Exception: ' + str(ex_stat))
          return False
    except ObjectDoesNotExist as ex_term:
      print('Error! The term ' + searched_term + ' does not exist when searching for terms in the term table! Exception: ' + str(ex_term))
      logging.error('Error! The term ' + searched_term + ' does not exist when searching for terms in the term table! Exception: ' + str(ex_term))
      return False

  @staticmethod
  def processDataWeight(searched_term_id: int, data_source: str, new_record_count: int, new_data: bool = True):
    try:
      existing_stat = pie_chart_sentiment_stat.objects.get(term_id=searched_term_id, data_source=data_source)
      if new_data:
        return decimal.Decimal(new_record_count / (existing_stat.processed_records_count + new_record_count))
      else:
        return decimal.Decimal(1 - (new_record_count / (existing_stat.processed_records_count + new_record_count)))
    except ObjectDoesNotExist:
      if new_data:
        return decimal.Decimal(1.0)
      else:
        return decimal.Decimal(0.0)
