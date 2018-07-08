from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from html_getter import HtmlGetter
from error_logger import Logger

class ParsersInterface:
    """
    Base class (interface) of all meme parsers.
    All derived classes have to implement abstract methods, which raises error: "NotImplementedError".
    """
    __metaclass__ = ABCMeta

    def __init__(self, name, url):
        self.web_page_name = name
        self.web_page_url = url
        self.raw_html = None
        self.pretty_html = None

    @abstractmethod
    def download_memes(self): raise NotImplementedError

    def _raw_and_pretty_html_setter(self):
        """
        Set raw_html and pretty_html from processed web page.
        Raw_html is raw string.
        Pretty_html is BeautifulSoup object.
        """
        self.raw_html = HtmlGetter.simple_get(self.web_page_url)
        Logger.CHECK_IF_NONE(self.raw_html)
        self.pretty_html = BeautifulSoup(self.raw_html, 'html.parser')
        Logger.CHECK_IF_NONE(self.pretty_html)


class KwejkParser(ParsersInterface):
    """
    Kwejk parser.
    """
    def __init__(self):
        self.web_page_name = "Kwejk"
        self.web_page_url = "http://kwejk.pl"

    def download_memes(self):
        super(KwejkParser, self)._raw_and_pretty_html_setter()

        #for i, li, in enumerate(kp.pretty_html.find_all("div", {"class": ["tag-list", "content"]})):
            #print(str(i) + str(li.text))