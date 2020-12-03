from re import sub
import praw
from praw.models import Submission
import logging
from django_project.settings import REDDIT_APP_SECRET
from partisan.models import subreddit, reddit_submission, reddit_comment
from partisan.p_classes.util.html import stripTags
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
      for submission in submissions:
        existing_subreddit = subreddit.getSubreddit(sub_name=subreddit_name)
        if existing_subreddit == False:
          new_subreddit = subreddit(subreddit_name=subreddit_name)
          new_subreddit.save()
          existing_subreddit = new_subreddit
        if not reddit_submission.getSubmission(submission_id=submission.id):
          new_submission = reddit_submission(
            submission_id=submission.id,
            text=submission.selftext,
            subreddit_id=existing_subreddit.id
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
      for i in range(comment_count):
        comment_text = stripTags(remote_comments[i].body_html)
        hashed_text = hashText(comment_text)
        existing_comment = reddit_comment.getComment(hash=hashed_text)
        if existing_comment == False and len(comment_text) > 200:
          new_comment = reddit_comment(
            comment_id=remote_comments[i].id,
            text=comment_text,
            text_hash=hashed_text,
            submission_id=reddit_submission.getSubmission(submission_id=submission.id).id
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