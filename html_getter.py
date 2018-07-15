from error_logger import Logger
from requests import get
from requests.exceptions import RequestException
from contextlib import closing


class HtmlGetter:
    """
    Functions for getting html content.
    """

    @staticmethod
    def simple_get(url):
        """
        Attempts to get the content of the url (url should be www page).
        It does HTTP GET request action.
        :param url: Path to the web page.
        :return: Returns text content if the respone of the HTTP GET is some kind of HTML/XML, otherwise returns None.
        """
        try:
            with closing(get(url, stream=True)) as resp:
                if HtmlGetter.__is_good_response(resp):
                    return resp.content
                else:
                    return None
        except RequestException as e:
            Logger.log_error("Error during requests to {0} : {1}".format(url, str(e)))
            return None

    @staticmethod
    def __is_good_response(resp):
        """
        :param resp: Response from the HTTP GET action.
        :return: True if the response seems to be HTML, false otherwise.
        """
        content_type = resp.headers["Content-Type"].lower()
        return (resp.status_code == 200
                and content_type is not None
                and (content_type.find('html') > -1 or content_type.find("jpeg") > -1))



