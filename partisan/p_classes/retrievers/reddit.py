import praw
from praw.models import Submission
from markdown import markdown
from bs4 import BeautifulSoup
import logging
from django_project.settings import REDDIT_APP_SECRET
from partisan.models import reddit_submission, reddit_comment, search_term
from partisan.p_classes.util.text import hashText

class reddit_retriever:

  reddit_interactor = {}

  def __init__(self):
    super().__init__()
    self.reddit_interactor = praw.Reddit(
      client_id="s1hHWMH_ekUzrQ",
      client_secret=REDDIT_APP_SECRET,
      redirect_uri="http://127.0.0.1:8000",
      user_agent="PartisanProject"
    )
    self.reddit_interactor.read_only = True

  def saveRedditSubmissions(self, subreddit_name: str, post_count: int, submission_type: str):
    gathered_submissions = []
    if submission_type not in ['gilded', 'hot', 'new', 'rising']:
      raise ValueError(submission_type + ' is not a valid submission type in Reddit. Please choose "gilded", "hot", "new", or "rising"')
    try:
      sub_interactor = self.reddit_interactor.subreddit(display_name=subreddit_name)
      submissions = getattr(sub_interactor, submission_type)(limit=post_count)
      existing_subreddit = search_term.getSearchTerm(term_name='r/' + subreddit_name)
      if existing_subreddit == False:
        new_subreddit = search_term(term='r/' + subreddit_name)
        new_subreddit.save()
        existing_subreddit = new_subreddit
      for submission in submissions:
        if not reddit_submission.getSubmission(submission_id=submission.id):
          if submission.selftext == '':
            new_submission = reddit_submission(
              submission_id=submission.id,
              term_id=existing_subreddit.id,
              nlp_processed=True,
              pie_stat_processed=True
            )
          else:
            submission.selftext = ''.join(BeautifulSoup(markdown(submission.selftext), features='html.parser').get_text())
            new_submission = reddit_submission(
              submission_id=submission.id,
              text=submission.selftext,
              term_id=existing_subreddit.id
            )
          new_submission.save()
          gathered_submissions.append(submission)
        else:
          gathered_submissions.append(submission)
      return gathered_submissions
    except Exception as ex:
      logging.error(str(ex))
      print(str(ex))
      return gathered_submissions

  def saveRedditComments(self, submission: Submission, comment_count: int):
    gathered_comments = []
    try:
      remote_comments = submission.comments
      if len(remote_comments) < comment_count:
        comment_count = len(remote_comments)
      existing_subreddit = search_term.getSearchTerm(term_name='r/' + submission.subreddit.display_name)
      if existing_subreddit == False:
        new_subreddit = search_term(term='r/' + submission.subreddit.display_name)
        new_subreddit.save()
        existing_subreddit = new_subreddit
      remote_comments.replace_more(limit=5)
      for i in range(comment_count):
        comment_text = BeautifulSoup(remote_comments[i].body_html, features='html.parser').get_text()
        hashed_text = hashText(comment_text)
        existing_comment = reddit_comment.getComment(hash=hashed_text)
        if existing_comment == False and len(comment_text) > 200:
          new_comment = reddit_comment(
            comment_id=remote_comments[i].id,
            text=comment_text,
            text_hash=hashed_text,
            term_id=existing_subreddit.id
          )
          new_comment.save()
          gathered_comments.append(new_comment)
        else:
          gathered_comments.append(existing_comment)
      return gathered_comments
    except Exception as ex:
      logging.error(str(ex))
      print(str(ex))
      return gathered_comments
