from django.core.management.base import BaseCommand, CommandError
from partisan.p_classes.nlp.aws_comprehend import comprehender
from partisan.p_classes.processors.twitter import twitter_processor

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--batchsize', type=int, help='The amount of records you want to run through AWS comprehend.', default=100, required=False)


    def handle(self, *args, **kwargs):
        processor = twitter_processor()
        processor.processTweets(process_number=kwargs['batchsize'])