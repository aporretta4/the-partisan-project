from django.db import models
from random import randrange
from django.core.exceptions import ObjectDoesNotExist

class search_term(models.Model):
    id = models.AutoField(primary_key=True,editable=False,unique=True)
    term = models.CharField(editable=False,unique=False,max_length=255)

    @staticmethod
    def getSearchTerm(term_name: str):
        try:
            return search_term.objects.get(term=term_name)
        except search_term.DoesNotExist:
            return False

class tweet(models.Model):
    id = models.BigIntegerField(primary_key=True,editable=False,unique=True)
    text = models.CharField(max_length=2048, )
    text_hash = models.CharField(max_length=128,null=True,unique=True)
    author_id = models.BigIntegerField(editable=False)
    created_at = models.DateTimeField(default='1970-01-01 00:00:00+00:00')
    pie_stat_processed = models.BooleanField(default=False)
    nlp_processed = models.BooleanField(default=False)
    nlp_neutral_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_positive_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_negative_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_mixed_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    term = models.ForeignKey(search_term,null=False,on_delete=models.RESTRICT)

    @staticmethod
    def searchTermTweets(searched_term: str):
        term = search_term.objects.filter(term=searched_term)
        if term.count() != 0:
            return tweet.objects.filter(term_id=term[0].id).all()
        else:
            return []

class tw_retriever_metadata(models.Model):
    id = models.CharField(primary_key=True,editable=False,unique=True,max_length=255)
    val = models.TextField(blank=False,null=False)

class reddit_submission(models.Model):
    submission_id = models.CharField(max_length=32, null=False, editable=False, unique=True)
    term = models.ForeignKey(to=search_term, on_delete=models.RESTRICT, null=False)
    text = models.CharField(max_length=4750, null=True)
    nlp_processed = models.BooleanField(default=False)
    nlp_neutral_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_positive_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_negative_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_mixed_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    pie_stat_processed = models.BooleanField(default=False)

    @staticmethod
    def getSubmission(submission_id: str):
        try:
            return reddit_submission.objects.get(submission_id=submission_id)
        except reddit_submission.DoesNotExist:
            return False

    def save(self):
        if self.text is not None:
            self.text = (self.text[:4750] + '...') if len(self.text) > 4750 else self.text
        super().save()

class reddit_comment(models.Model):
    comment_id = models.CharField(max_length=32, null=False, editable=False)
    term = models.ForeignKey(to=search_term, on_delete=models.RESTRICT, null=False)
    text = models.CharField(max_length=4750, null=False)
    text_hash = models.CharField(max_length=128,null=True,unique=True)
    nlp_processed = models.BooleanField(default=False)
    nlp_neutral_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_positive_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_negative_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_mixed_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    pie_stat_processed = models.BooleanField(default=False)

    @staticmethod
    def getComment(hash: str):
        try:
            return reddit_comment.objects.get(text_hash=hash)
        except reddit_comment.DoesNotExist:
            return False

    def save(self):
        if self.text is not None:
            self.text = (self.text[:4750] + '...') if len(self.text) > 4750 else self.text
        super().save()

class pie_chart_sentiment_stat(models.Model):
    id = models.AutoField(primary_key=True,editable=False,unique=True)
    term = models.OneToOneField(search_term,null=False,on_delete=models.RESTRICT,related_name='statistic_of')
    neutral_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    mixed_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    positive_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    negative_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    processed_records_count = models.BigIntegerField(editable=True,null=True)

    @staticmethod
    def getStat(searched_term: str, sentiment: str):
        try:
            term = pie_chart_sentiment_stat.objects.get(term_id__term=searched_term)
            if sentiment == 'positive':
                return term.positive_sentiment_aggregate
            elif sentiment == 'negative':
                return term.negative_sentiment_aggregate
            elif sentiment == 'neutral':
                return term.neutral_sentiment_aggregate
            elif sentiment == 'mixed':
                return term.mixed_sentiment_aggregate
            else:
                return -1
        except ObjectDoesNotExist as ex:
            return -1
