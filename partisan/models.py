from django.db import models
from random import randrange
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator

class search_term(models.Model):
    id = models.AutoField(primary_key=True,editable=False,unique=True)
    term = models.CharField(editable=False,unique=False,max_length=255)

    def __str__(self):
        return self.term

    @staticmethod
    def getSearchTerm(term_name: str):
        try:
            return search_term.objects.get(term=term_name)
        except search_term.DoesNotExist:
            return False

class news(models.Model):
    id = models.BigIntegerField(primary_key=True,editable=False,unique=True)
    source = models.CharField(max_length=256,null=True,unique=True)
    outlet = models.CharField(max_length=256,null=True,unique=True)
    text = models.TextField(blank=False,null=False)
    created_at = models.DateTimeField(default='1970-01-01 00:00:00+00:00')
    pie_stat_processed = models.BooleanField(default=False)
    nlp_processed = models.BooleanField(default=False)
    nlp_neutral_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_positive_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_negative_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    nlp_mixed_sentiment = models.DecimalField(max_digits=30,decimal_places=20,null=True)
    term = models.ForeignKey(search_term,null=False,on_delete=models.RESTRICT)

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
            self.text = (self.text[:4740] + '...') if len(self.text) > 4740 else self.text
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
            self.text = (self.text[:4740] + '...') if len(self.text) > 4740 else self.text
        super().save()

class data_sources(models.TextChoices):
    REDDIT = 're', ('Reddit')
    TWITTER = 'tw', ('Twitter')

    @staticmethod
    def getSource(key: str):
        choices = {v: k for v, k in data_sources.choices}
        if key in choices:
            return choices[key]
        else:
            return ''

class pull_configuration(models.Model):
    id = models.AutoField(primary_key=True,editable=False,unique=True)
    term_name = models.CharField(unique=True,max_length=255,editable=True,help_text='If searching a subreddit, DO NOT prefix with "r/".')
    data_source = models.CharField(
        max_length=2,
        choices=data_sources.choices,
        default=data_sources.REDDIT,
        editable=True,
        null=False
    )
    items_per_run = models.IntegerField(null=False,editable=True,validators=[MinValueValidator(1),MaxValueValidator(10000)])

    def __str__(self):
        return self.term_name + ' (from ' + data_sources.getSource(key=self.data_source) + ')'

class sentiment_process_configuration(models.Model):
    id = models.AutoField(primary_key=True,editable=False,unique=True)
    term = models.OneToOneField(search_term,null=False,on_delete=models.CASCADE,related_name='pull_config_of',unique=True)
    data_source = models.CharField(
        max_length=2,
        choices=data_sources.choices,
        default=data_sources.REDDIT,
        editable=True,
        null=False
    )
    items_per_run = models.IntegerField(null=False,editable=True,validators=[MinValueValidator(1),MaxValueValidator(10000)])

    def __str__(self):
        return str(self.term) + ' (from ' + data_sources.getSource(key=self.data_source) + ')'

class pie_chart_sentiment_stat(models.Model):
    id = models.AutoField(primary_key=True,editable=False,unique=True)
    term = models.OneToOneField(search_term,null=False,on_delete=models.RESTRICT,related_name='statistic_of')
    neutral_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    mixed_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    positive_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    negative_sentiment_aggregate = models.DecimalField(max_digits=6,decimal_places=5,null=True)
    processed_records_count = models.BigIntegerField(editable=True,null=True)
    data_source = models.CharField(
        max_length=2,
        choices=data_sources.choices,
        editable=True,
        null=False
    )

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

    @staticmethod
    def mergePieStats(*pie_stats):
        total_records = 0
        merged_pie_stats = {
        'positive': 0,
        'negative': 0,
        'neutral': 0,
        'mixed': 0,
        }
        for pie_stat in pie_stats:
            total_records = total_records + pie_stat.processed_records_count
        for pie_stat in pie_stats:
            merged_pie_stats['positive'] = merged_pie_stats['positive'] + float(pie_stat.positive_sentiment_aggregate) * (pie_stat.processed_records_count / total_records)
            merged_pie_stats['negative'] = merged_pie_stats['negative'] + float(pie_stat.negative_sentiment_aggregate) * (pie_stat.processed_records_count / total_records)
            merged_pie_stats['neutral'] = merged_pie_stats['neutral'] + float(pie_stat.neutral_sentiment_aggregate) * (pie_stat.processed_records_count / total_records)
            merged_pie_stats['mixed'] = merged_pie_stats['mixed'] + float(pie_stat.mixed_sentiment_aggregate) * (pie_stat.processed_records_count / total_records)
        return merged_pie_stats
