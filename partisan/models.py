from django.db import models

# Create your models here.

class tweet(models.Model):
    id = models.BigIntegerField(primary_key=True,editable=False,unique=True)
    text = models.CharField(max_length=280, )
    author_id = models.BigIntegerField(editable=False)
    created_at = models.DateTimeField(default='1970-01-01 00:00:00+00:00')

class tw_retriever_metadata(models.Model):
    id = models.CharField(primary_key=True,editable=False,unique=True,max_length=512)
    val = models.TextField(blank=False,null=False)