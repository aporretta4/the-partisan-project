from django.core.management.base import BaseCommand, CommandError
from partisan.p_classes.processors.pie_chart_sentiment_stat import stat_processor
from partisan.models import tweet, reddit_comment, reddit_submission

class Command(BaseCommand):

  def add_arguments(self, parser):
    parser.add_argument('search_term', type=str, help='The search term you want to process sentiment pie stats for.')

  def handle(self, *args, **kwargs):
    success = stat_processor.processStats(searched_term=kwargs['search_term'], sentimentable_model=tweet, batch=1000)
    success = stat_processor.processStats(searched_term=kwargs['search_term'], sentimentable_model=reddit_comment, batch=1000)
    success = stat_processor.processStats(searched_term=kwargs['search_term'], sentimentable_model=reddit_submission, batch=1000)
    if success:
      self.stdout.write(self.style.SUCCESS('Successfully processed pie stats for term ' + kwargs['search_term']) + '.')
    else:
      self.stdout.write(self.style.SUCCESS('DID NOT SUCCESSFULLY PROCESS PIE STATS FOR term ' + kwargs['search_term']) + '.')
