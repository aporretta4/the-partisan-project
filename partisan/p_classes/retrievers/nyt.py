from django_project.settings import NYT_API_SECRET
from django.utils import timezone, dateparse
from urllib import request, parse
from partisan.models import nyt_retriever_metadata, search_term, news
from datetime import timedelta
import json

class nyt_retriever():

  nyt_endpoint = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
  next_page_meta = nyt_retriever_metadata()
  api_throttle_meta = nyt_retriever_metadata()

  def __init__(self):
    try:
      self.next_page_meta = nyt_retriever_metadata.objects.get(id="next_page_meta")
    except nyt_retriever_metadata.DoesNotExist:
      new_pager_meta = nyt_retriever_metadata(id='next_page_meta', val='0')
      new_pager_meta.save()
      self.next_page_meta = new_pager_meta
    try:
      self.api_throttle_meta = nyt_retriever_metadata.objects.get(id='api_throttle_meta')
    except nyt_retriever_metadata.DoesNotExist:
      dt = timezone.now()
      dt = dt + timedelta(0, -6)
      new_throttle_meta = nyt_retriever_metadata(id='api_throttle_meta', val=dt.strftime('%Y-%m-%d %H:%M:%S%z'))
      new_throttle_meta.save()
      self.api_throttle_meta = new_throttle_meta

  def initiatePull(self, term: str, count: int):
    throttle = dateparse.parse_datetime(self.api_throttle_meta.val)
    if timezone.now() > throttle:
      new_dt = timezone.now()
      new_dt = new_dt + timedelta(0, 6)
      self.api_throttle_meta.val = new_dt.strftime('%Y-%m-%d %H:%M:%S%z')
      self.api_throttle_meta.save()
      return self.saveNews(term, count)

  def saveNews(self, term: str, count: int):
    pulled_count = 0
    yesterday = timezone.now() - timedelta(1)
    if count > 10:
      count = 10
    term = self.__createTerm(term=term)
    query = self.nyt_endpoint + '?q=' + parse.quote(term.term) \
      + '&page=' + self.next_page_meta.val \
      + '&api-key=' + NYT_API_SECRET \
      + '&sort=newest&facet=true&facet_fields=source&begin_date=' + yesterday.strftime('%Y%m%d') \
      + '&fl=lead_paragraph,headline,web_url'
    resp = request.urlopen(url=query)
    resp = json.loads(resp.read().decode('utf-8'))
    if resp['status'] == 'OK':
      for news_article in resp['response']['docs']:
        if len(news.objects.filter(source=news_article['web_url'])) == 0:
          new_article = news(
            source=news_article['web_url'],
            text=news_article['headline']['main'] + '. ' + news_article['lead_paragraph'],
            term_id=term.id,
            created_at=timezone.now().strftime('%Y-%m-%d %H:%M:%S%z')
          )
          new_article.save()
          pulled_count = pulled_count + 1
      self.__updatePager(resp)
    else:
      raise SystemError('A 200 was not retuned by the NYT API. The response status is: ' + resp['status'])
    return pulled_count


  def __createTerm(self, term: str):
    term = search_term.getSearchTerm(term_name=term)
    if term:
      return term
    else:
      term = search_term(term_name=term)
      term.save()
      return term

  def __updatePager(self, resp: dict):
    if len(resp['response']['docs']) < 10:
      self.next_page_meta.val = '0'
      self.next_page_meta.save()
    else:
      self.next_page_meta.val = str(int(self.next_page_meta.val) + 1)
      self.next_page_meta.save()

