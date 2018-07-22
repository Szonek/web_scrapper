from abc import ABCMeta, abstractmethod
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from meme_info import MemeInfo
import json
import datetime
import os



class RequestParserInterface:
    """
    Base interface for parsers using HTML request to get memes data.
    """
    __metaclass__ = ABCMeta

    def __init__(self, name, url, url_hot):
        self._web_page_name = name
        self._web_page_url = url
        self._request_url_hot = url_hot

    @abstractmethod
    def download_memes(self):
        """
        Virtual function. All parsers have to implement own download_function.
        It should download memes from whole (if possible) page.
        """
        raise NotImplementedError


class NineGagParser(RequestParserInterface):

    def __init__(self):
        self._web_page_name = "9gag"
        self._web_page_url = "https://9gag.com"
        self._request_url_hot = "https://9gag.com/v1/group-posts/group/default/type/hot"

    def download_memes(self):
        try:
            response = urlopen(self._request_url_hot).read()
            response_json = json.loads(response)
            if response_json['meta']['status'] != 'Success':
                print('Error (9gag)')
                return
            for post in response_json['data']['posts']:
                # skip gifs and nsfw
                if post['type'] != 'Photo' or post['nsfw'] == 1:
                    continue
                # skip if there is no image url
                if 'image700' not in post['images']:
                    continue
                meme_info = MemeInfo(
                    title=post['title'],
                    id=post['id'],
                    web_page_name=self._web_page_name,
                    url_to_img=post['images']['image700']['url'],
                    author='',
                    category=post['sections'],
                    tags=list(map((lambda tag_data: tag_data['key']), post['tags']))
                )
                meme_info.save_on_disk()
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        except Exception as e:
            print('Error: ', str(e))
