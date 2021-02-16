import logging
from django.core.management.base import BaseCommand, CommandError
from partisan.p_classes.processors.sentiment_processor import stat_processor
from partisan.models import tweet, reddit_comment, reddit_submission, search_term, news
from partisan.p_classes.exceptions.DataExceptions import DataSourceNotFoundException

class Command(BaseCommand):

  def handle(self, *args, **kwargs):
    search_terms = search_term.objects.all()
    for term in search_terms:
      try:
        if stat_processor.processModelStats(searched_term=term.term, sentimentable_model=tweet, batch=1000, type='historic_averages'):
          self.stdout.write(self.style.SUCCESS('Successfully processed Twitter historic stats for term ' + term.term + '.'))
        else:
          self.stdout.write(self.style.ERROR('DID NOT SUCCESSFULLY PROCESS TWITTER HISTORIC STATS FOR TERM ' + term.term + '.'))
      except DataSourceNotFoundException as ex:
        self.__handleDataSourceException(exception=ex)
      try:
        if stat_processor.processModelStats(searched_term=term.term, sentimentable_model=reddit_comment, batch=1000, type='historic_averages'):
          self.stdout.write(self.style.SUCCESS('Successfully processed Reddit submission historic stats for term ' + term.term + '.'))
        else:
          self.stdout.write(self.style.ERROR('DID NOT SUCCESSFULLY PROCESS REDDIT SUBMISSION HISTORIC STATS FOR TERM ' + term.term + '.'))
      except DataSourceNotFoundException as ex:
        self.__handleDataSourceException(exception=ex)
      try:
        if stat_processor.processModelStats(searched_term=term.term, sentimentable_model=reddit_submission, batch=1000, type='historic_averages'):
          self.stdout.write(self.style.SUCCESS('Successfully processed Reddit comment historic stats for term ' + term.term + '.'))
        else:
          self.stdout.write(self.style.ERROR('DID NOT SUCCESSFULLY PROCESS REDDIT COMMENT HISTORIC STATS FOR TERM ' + term.term + '.'))
      except DataSourceNotFoundException as ex:
        self.__handleDataSourceException(exception=ex)


  def __handleDataSourceException(self, exception: DataSourceNotFoundException):
    logging.error(str(exception))
    self.stdout.write(self.style.ERROR(str(exception)))