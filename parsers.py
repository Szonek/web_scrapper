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

    def __init__(self, name, url, path_on_disk):
        self._web_page_name = name
        self._web_page_url = url
        self._path_on_disk = path_on_disk
        self._raw_html = None
        self._pretty_html = None

    @abstractmethod
    def download_memes(self):
        """
        Virtual function. All parsers have to implement own download_function.
        It should download memes from whole (if possible) page.
        """
        raise NotImplementedError

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

    def _get_by_tag_and_class(self, tag, class_):
        """
        Extract texts from pretty html (BeatiuflSoup object)based on tag and class of this tag.
        Example: <div class="user-bar"> abc </div> -> tag: "div", class: "user-bar" -> texts: "abc"
        :param tag: HTML tag (string)
        :param class_: HTML class (string)
        :return: Array of values matching tag and class_. (Value is text between tags: <..> ... </..>)
        """
        out = []
        for value in self.pretty_html.find_all(tag, class_=class_):
            out.append(value.text)
        return out

    def _get_attribute_from_tag(self, tag, attribute):
        """
        Extract attribute value from pretty html (BeatiuflSoup object) based on tag.
        Example: <div class="user-bar"> -> tag: "div", attribute="class" -> attribute value: "user-bar"
        :param tag: HTML tag (string)
        :param attribute: HTML attribute
        :return: Array of attribute values of matching tag.
        """
        out = []
        for attr in self.pretty_html.find_all(tag):
            if attr[attribute] != 0:
                out.append(attr[attribute])
        return out

    def _save_image_from_url(self, web_url, file_name):
        image_raw = HtmlGetter.simple_get(web_url)
        with open(self.path_on_disk + "\\" + file_name, 'wb') as f:
            f.write(image_raw)

    def _split_url(self, memes_urls, character):
        """
        Split url by "/" character.
        Example: "http://kwejk.pl"   -> ["http", "", "kwejk.pl"]
        :param memes_urls: 1D array of urls.
        :return: Splitted array of urls. Returns 2D array.
        """
        splited_urls = []
        for i in range(len(memes_urls)):
            splited_urls.append(memes_urls[i].split(character))
        return splited_urls


class KwejkParser(ParsersInterface):
    """
    Kwejk parser.
    """
    def __init__(self, path_on_disk):
        self.web_page_name = "Kwejk"
        self.web_page_url = "http://kwejk.pl"
        self.path_on_disk = path_on_disk

    def __extract_links_only_to_memes(self, urls):
        """
        Kwejk specific function.
        Helper functions which from the all urls choose only theese, which contains memes.
        :param urls: Array of urls
        :return: Array of urls to memes.
        """
        requirements = ["kwejk", "obrazki", ".jpg"]  # if all of these are in the url, we can be sure we are dealing with meme
        forbidden = ["_mobile"]
        ret = []
        for url in urls:
            if all(x in url for x in requirements) and all(x not in url for x in forbidden):
                ret.append(url)
        return ret

    def download_memes(self):
        super(KwejkParser, self)._raw_and_pretty_html_setter()
        categories = self._get_by_tag_and_class("a", "category")
        tags = self._get_by_tag_and_class("div", "tag-list")
        authors = self._get_by_tag_and_class("span", "name")
        urls_to_memes = self.__extract_links_only_to_memes(self._get_attribute_from_tag("img", "src"))
        splited_urls = self._split_url(urls_to_memes, "/")
        ids = []
        for splited in splited_urls:
            ids.append(splited[-1][:-4])  # [:-4] means we dont want to have ".jpg" in id of meme
        memes_count = len(ids)
        for i in range(memes_count):
            self._save_image_from_url(urls_to_memes[i], ids[i] + ".jpg")
