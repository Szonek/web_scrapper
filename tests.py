import unittest
from html_getter import HtmlGetter
from bs4 import BeautifulSoup
import parsers


class WebScrapperTester(unittest.TestCase):
    """
    Unit tests for scrapping and manipulating htmls from the web.
    Every test name have to start with "test_"
    """

    def test_basic_web_scrapper(self):
        raw_html = HtmlGetter.simple_get('https://wikipedia.org')
        self.assertIsNotNone(raw_html)  # if not None then we got html

    def test_simple_html_page(self):
        raw_html = open("test_content\contrived.html").read()
        parsed_html = BeautifulSoup(raw_html, 'html.parser')
        reference_outputs = ["eggman", "walrus"]
        real_outputs = []
        for p in parsed_html.select('p'):
            real_outputs.append(p['id'])
        self.assertEqual(real_outputs, reference_outputs)

    def test_basic_kwejk(self):
        kwejk_parser = parsers.KwejkParser()  # we will not download memes so we give dummy path
        name = kwejk_parser.web_page_name
        url = kwejk_parser.web_page_url
        self.assertEqual(name, "Kwejk")
        self.assertEqual(url, "http://kwejk.pl")

    def test_basic_kwejk(self):
        kwejk_parser = parsers.KwejkParser()  # we will not download memes so we give dummy path
        kwejk_parser.download_memes()
        run_complete = True
        self.assertTrue(run_complete)


if __name__ == '__main__':
    unittest.main(verbosity=2)
