from django.core.management.base import BaseCommand
from partisan.models import sentiment_process_configuration, tweet, reddit_comment, reddit_submission
from partisan.p_classes.nlp.sentimentable import sentimentable

class Command(BaseCommand):

  def handle(self, *args, **kwargs):
    tw_sentiment_configs = sentiment_process_configuration.objects.filter(data_source='tw')
    for tw_sentimentiment_conf in tw_sentiment_configs:
      tweets = tweet.objects.filter(nlp_processed=False, ).order_by('id')[:tw_sentimentiment_conf.items_per_run]
      sentimentable.saveTextSentiment(sentimentable_classes=tweets)
    self.stdout.write(self.style.SUCCESS('Processed Twitter sentiment data.'))
    re_sentiment_configs = sentiment_process_configuration.objects.filter(data_source='re')
    for re_sentimentiment_conf in re_sentiment_configs:
      reddit_comments = reddit_comment.objects.filter(nlp_processed=False).order_by('id')[:re_sentimentiment_conf.items_per_run]
      sentimentable.saveTextSentiment(sentimentable_classes=reddit_comments)
      reddit_submissions = reddit_submission.objects.filter(nlp_processed=False).exclude(text='').order_by('id')[:re_sentimentiment_conf.items_per_run]
      sentimentable.saveTextSentiment(sentimentable_classes=reddit_submissions)
    self.stdout.write(self.style.SUCCESS('Processed Reddit sentiment data.'))