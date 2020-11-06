import boto3
import json

class comprehender:
    def __init__(self):
        super().__init__()

    def comprehendText(self, text: list):
      comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')
      return comprehend.batch_detect_sentiment(TextList=text, LanguageCode='en')