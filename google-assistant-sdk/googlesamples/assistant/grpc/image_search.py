"""
  Helper for the image search
"""
import logging
from googleapiclient.discovery import build # declared in google-api-python-client


class ImageSearch(object):
  """Queries Google Custom Search for images"""

  def __init__(self, api_key, custom_search):
    self.__search = build('customsearch', 'v1', developerKey=api_key)
    self.custom_search = custom_search

  def search(self, query, num=10):
    """searches for images by a query"""
    res = []
    try:
        response = self.__search.cse().list(
            q=query,
            cx=self.custom_search,
            num=num,
            searchType='image',
            safe='high',
            start=0).execute()
        if response and 'items' in response:
          res.extend([item['link'] for item in response['items'] if 'link' in item])
    except Exception:
      logging.exception('Generic exception')
    return res
