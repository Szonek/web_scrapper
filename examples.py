from html_getter import HtmlGetter
from bs4 import BeautifulSoup

# https://realpython.com/python-web-scraping-practical-introduction/

raw_html = HtmlGetter.simple_get('https://realpython.com/blog/')
print(len(raw_html))
print(raw_html)

raw_html = open("test_content\contrived.html").read()
html = BeautifulSoup(raw_html, 'html.parser')
for p in html.select('p'):
    if p['id'] == "walrus":
        print(p.text)

raw_html = HtmlGetter.simple_get("http://kwejk.pl")
html = BeautifulSoup(raw_html, 'html.parser')
for i, li, in enumerate(html.select("li")):
    print(str(i) + str(li.text))

raw_html = HtmlGetter.simple_get("http://fabpedigree.com/james/mathmen.htm")
html = BeautifulSoup(raw_html, 'html.parser')
for i, li, in enumerate(html.select("li")):
    print(str(i) + str(li.text))
