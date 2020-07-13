import requests
import bs4
import json


class GathererTemplate:
    @classmethod
    def get_html(cls, url):
        response = requests.get(url)
        if response.status_code == 200:
            document = bs4.BeautifulSoup(response.text, features="html.parser")
            return document

    @classmethod
    def get_json(cls, url):
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return json.loads(response.text)
            except:
                pass

    @classmethod
    def next(cls, element: bs4.PageElement):
        children = list(element.parent.children)
        index = children.index(element)
        delta = 1
        while index + delta < len(children) and isinstance(children[index + delta], bs4.NavigableString):
            delta += 1

        if index + delta < len(children):
            return children[index + delta]
