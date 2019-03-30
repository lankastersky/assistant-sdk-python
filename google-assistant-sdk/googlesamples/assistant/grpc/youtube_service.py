"""Helper for the youtube search

  See
  https://developers.google.com/api-client-library/python/apis/youtube/v3
  https://developers.google.com/youtube/v3/quickstart/python
"""

from googleapiclient.discovery import build # declared in google-api-python-client


class YouTubeSearchService(object):
  """The Youtube search service to use.

    Functionalities to include:
    - Search for videos given a keyword.
  """

  API_SERVICE_NAME = 'youtube'
  API_VERSION = 'v3'
  MAX_WIDTH = 1920

  def __init__(self, api_key=None, app_name=None):
    self.app_name = app_name or self.API_SERVICE_NAME
    self.service = build(self.app_name, self.API_VERSION, developerKey=api_key)

  def _get_video_stats(self, video_id):
    """Fetches video statistics for the specified video ID.
      Args:
        video_id: A video ID or command-delimited list of video IDs as a string.
    """
    kwargs = {}
    kwargs['part'] = 'statistics,snippet,player'
    kwargs['id'] = video_id
    kwargs['maxWidth'] = YouTubeSearchService.MAX_WIDTH

    response = self.service.videos().list(**kwargs).execute()
    results = response.get('items', [])
    return results

  def search(self, query, **kwargs):
    """Fetches YouTube video IDs.

      Args:
        query: The YouTube search query.
        kwargs: additional parameters to the API. See
                    https://developers.google.com/youtube/v3/docs/search/list
    """
    # Setup default parameters for this query
    kwargs['q'] = query
    kwargs['part'] = kwargs.get('part', 'id')
    kwargs['type'] = 'video'
    kwargs['videoEmbeddable'] = 'true'
    kwargs['videoSyndicated'] = 'true'

    search_response = self.service.search().list(**kwargs).execute()
    results = search_response.get('items', [])
    videoIds = ','.join([res['id']['videoId'] for res in results])
    stats = self._get_video_stats(videoIds)

    ret = []
    for vid in stats:
      ret.append({
        'videoId': vid['id'],
        'title': vid['snippet']['title'],
        'views': vid['statistics'].get('viewCount', 0),
      })

    return ret
