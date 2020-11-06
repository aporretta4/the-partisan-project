from django.core.management.base import BaseCommand, CommandError
from partisan.p_classes.nlp.aws_comprehend import comprehender
from partisan.p_classes.processors.twitter import twitter_processor

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        processor = twitter_processor()
        processor.processTweets()