from io import StringIO
from html.parser import HTMLParser

class Stripper(HTMLParser):
  def __init__(self):
    super().__init__()
    self.reset()
    self.strict = False
    self.convert_charrefs = True
    self.text = StringIO()
  def handle_data(self, d):
    self.text.write(d)
  def get_data(self):
    return self.text.getvalue()

def stripTags(html):
  s = Stripper()
  s.feed(html)
  return s.get_data()