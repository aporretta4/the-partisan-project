import logging
from django.db import models
from partisan.p_classes.nlp.aws_comprehend import comprehender

class sentimentable():

  @staticmethod
  def saveTextSentiment(sentimentable_classes: models.QuerySet):
    sentiment_comprehender = comprehender()
    sentimentable_list = list(sentimentable_classes)
    text_list = [None] * sentimentable_classes.count()
    processed_sentiment_list = []
    processed_index = 0
    for i in range(sentimentable_classes.count()):
      text_list[i] = sentimentable.__shrinkLongText(sentimentable_list[i].text)
    text_list = list(sentimentable.__chunk(text_list=text_list, n=25))
    for i in range(len(text_list)):
      sentiment_list = sentiment_comprehender.comprehendText(text=text_list[i])
      for j in range(len(sentiment_list['ResultList'])):
        processed_sentiment_list.append(sentiment_list['ResultList'][j])
    for i in range(sentimentable_classes.count()):
      try:
        sentimentable_classes[i].nlp_processed = True
        if processed_sentiment_list[i]['SentimentScore']['Mixed'] < 0.25:
          sentimentable_list[i].nlp_neutral_sentiment = processed_sentiment_list[i]['SentimentScore']['Neutral']
          sentimentable_list[i].nlp_mixed_sentiment = processed_sentiment_list[i]['SentimentScore']['Mixed']
          sentimentable_list[i].nlp_negative_sentiment = processed_sentiment_list[i]['SentimentScore']['Negative']
          sentimentable_list[i].nlp_positive_sentiment = processed_sentiment_list[i]['SentimentScore']['Positive']
        if sentimentable_list[i].nlp_neutral_sentiment == None or sentimentable_list[i].nlp_mixed_sentiment == None or sentimentable_list[i].nlp_negative_sentiment == None or sentimentable_list[i].nlp_positive_sentiment == None:
          sentimentable_list[i].delete()
        else:
          sentimentable_list[i].save()
        processed_index += 1
      except Exception as ex:
        logging.error(str(ex))
        print(str(ex))
        sentimentable_classes[processed_index].delete()
        processed_index += 1

  @staticmethod
  def __chunk(text_list: list, n: int):
    for i in range(0, len(text_list), n):
      yield text_list[i:i + n]

  @staticmethod
  def __shrinkLongText(text: str):
    if len(text) > 4750:
      return text[0:4750]
    else:
      return text
