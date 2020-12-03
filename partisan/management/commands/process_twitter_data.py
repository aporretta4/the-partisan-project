from django.core.management.base import BaseCommand
from partisan.models import tweet
from partisan.p_classes.nlp.sentimentable import sentimentable

class Command(BaseCommand):

  def add_arguments(self, parser):
    parser.add_argument('--batchsize', type=int, help='The amount of records you want to run through AWS comprehend.', default=100, required=False)

  def handle(self, *args, **kwargs):
    tweets = tweet.objects.filter(nlp_processed=False, ).order_by('id')[:kwargs['batchsize']]
    sentimentable.saveTextSentiment(sentimentable_classes=tweets)
