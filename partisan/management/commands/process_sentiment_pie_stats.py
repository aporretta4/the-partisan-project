from django.core.management.base import BaseCommand, CommandError
from partisan.p_classes.processors.pie_chart_sentiment_stat import stat_processor
from partisan.models import tweet, reddit_comment, reddit_submission, search_term

class Command(BaseCommand):

  def handle(self, *args, **kwargs):
    search_terms = search_term.objects.all()
    for term in search_terms:
      if stat_processor.processStats(searched_term=term.term, sentimentable_model=tweet, batch=10000):
        self.stdout.write(self.style.SUCCESS('Successfully processed Twitter pie stats for term ' + term.term + '.'))
      else:
        self.stdout.write(self.style.ERROR('DID NOT SUCCESSFULLY PROCESS TWITTER PIE STATS FOR TERM ' + term.term + '.'))
      if stat_processor.processStats(searched_term=term.term, sentimentable_model=reddit_comment, batch=10000):
        self.stdout.write(self.style.SUCCESS('Successfully processed Reddit submission pie stats for term ' + term.term + '.'))
      else:
        self.stdout.write(self.style.ERROR('DID NOT SUCCESSFULLY PROCESS REDDIT SUBMISSION PIE STATS FOR TERM ' + term.term + '.'))
      if stat_processor.processStats(searched_term=term.term, sentimentable_model=reddit_submission, batch=10000):
        self.stdout.write(self.style.SUCCESS('Successfully processed Reddit comment pie stats for term ' + term.term + '.'))
      else:
        self.stdout.write(self.style.ERROR('DID NOT SUCCESSFULLY PROCESS REDDIT COMMENT PIE STATS FOR TERM ' + term.term + '.'))
