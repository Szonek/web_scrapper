from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from html_getter import HtmlGetter
from error_logger import Logger
from meme_info import MemeInfo
import inspect
import sys
import importlib


class ParsersInterface:
    """
    Base class (interface) of all meme parsers.
    All derived classes have to implement abstract methods, which raises error: "NotImplementedError".
    """
    __metaclass__ = ABCMeta

    def __init__(self, name, url):
        self._web_page_name = name
        self._web_page_url = url
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
        self._raw_html = HtmlGetter.simple_get(self._web_page_url)
        Logger.CHECK_IF_NONE(self._raw_html)
        self._pretty_html = BeautifulSoup(self._raw_html, 'html.parser')
        Logger.CHECK_IF_NONE(self._pretty_html)

    def _get_by_tag_and_class(self, tag, class_):
        """
        Extract texts from pretty html (BeatiuflSoup object)based on tag and class of this tag.
        Example: <div class="user-bar"> abc </div> -> tag: "div", class: "user-bar" -> texts: "abc"
        :param tag: HTML tag (string)
        :param class_: HTML class (string)
        :return: Array of values matching tag and class_. (Value is text between tags: <..> ... </..>)
        """
        out = []
        for value in self._pretty_html.find_all(tag, class_=class_):
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
        for attr in self._pretty_html.find_all(tag):
            if attr[attribute] != 0:
                out.append(attr[attribute])
        return out

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
    Available methods:
    1. Set_page() -> sets page, which will be parsed (if not used: newest page is used)
    2. download_memes() -> download memes from sat page.
    """
    def __init__(self):
        self._web_page_name = "Kwejk"
        self._web_page_url = "http://kwejk.pl"

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

    def __make_array_from_toolbar(self, tags):
        """
        Process tags so they are useful.
        :param tags: Tags parsed from the kwejk.
        """
        for i in range(len(tags)):
            tags[i] = tags[i].split("\n")
            del tags[i][0]
            del tags[i][-1]

    def __get_gifs_idx(self, categories):
        """
        Currently detecting GIF is based on category.
        :param categories: Array of categories.
        :return: array of idxs of gifs
        """
        gifs_idxs = []
        for idx, cat in enumerate(categories):
            if cat == "GIF":
                gifs_idxs.append(idx)
        return gifs_idxs

    def set_page(self, page_number=0):
        """
        If user wants to download history of Kwejk he should set number of the page. (default is 0 -> newest)
        :param page_number: Number of the page of kwejk web site.
        """
        base_url = "http://kwejk.pl"
        if page_number == 0:
            self._web_page_url = base_url
        else:
            strona_str = "/strona/"
            self._web_page_url = base_url + strona_str + str(page_number)

    def download_memes(self):
        super(KwejkParser, self)._raw_and_pretty_html_setter()
        toolbars = self._get_by_tag_and_class("div", "toolbar")
        self.__make_array_from_toolbar(toolbars)
        categories = []
        tags = []
        for toolbar in toolbars:
            categories.append(toolbar[0])
            tags.append(toolbar[2:-1])
        gifs_idxs = self.__get_gifs_idx(categories)

        authors = self._get_by_tag_and_class("span", "name")
        if len(authors) != len(categories):  # some pages have one additional author (its best comment author)
            del authors[-1]
        for gif_idx in gifs_idxs:  # we need to delete info about gif
            del tags[gif_idx]
            del authors[gif_idx]
            del categories[gif_idx]

        urls_to_imgs = self.__extract_links_only_to_memes(self._get_attribute_from_tag("img", "src"))
        splited_urls = self._split_url(urls_to_imgs, "/")
        ids = []
        for splited in splited_urls:
            ids.append(splited[-1][:-4])  # [:-4] means we dont want to have ".jpg" in id of meme
        memes_count = len(ids)
        for i in range(memes_count):
            meme_info = MemeInfo(
                title="title",
                id=ids[i],
                web_page_name=self._web_page_name,
                url_to_img=urls_to_imgs[i],
                author=authors[i],
                category=[categories[i]],
                tags=tags[i]
            )
            meme_info.save_on_disk()





class TestParser(ParsersInterface):
    """
    Just for tests!
    """
    def __init__(self):
        self._web_page_name = "TestName"
        self._web_page_url = "test_url"

    def download_memes(self):
        print("downloading meme for TestParser")


class AllParsers:
    """
    It create all parsers, which are given in the constructor argument.
    No need to update this class, when adding new parser.
    !!! All parsers need to implement download_memes() method and have name <WebPageName>Parser !!!
    """
    def __init__(self, parsers_names=[]):
        self.parsers_names = [name + "Parser" for name in parsers_names]
        self.parser_objs = []
        self.__create_parser()

    def __create_parser(self):
        """
        Creates instances of parsers, based on the given names in the constructor.
        """
        is_class_member = lambda member: inspect.isclass(member) and member.__module__ == __name__
        classes = inspect.getmembers(sys.modules[__name__], is_class_member)

        get_class = lambda x: globals()[x]
        for parser, _ in classes:
            if any(parser in p_name for p_name in self.parsers_names):
                c = get_class(parser)
                inst = c()
                self.parser_objs.append(inst)

    def download_memes(self):
        """
        Download memes from all created parsers.
        """
        for parser in self.parser_objs:
            parser.download_memes()
