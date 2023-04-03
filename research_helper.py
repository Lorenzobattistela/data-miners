import urllib.request
import xml.etree.ElementTree as ET
from typing import List
from deep_translator import GoogleTranslator


class Article:
    def __init__(self, title: str, published: str, authors: List, summary: str) -> None:
        self.title = title
        self.published = published
        self.authors = authors
        self.summary = summary
        self.original_title = None

    def translate(self):
        translator = GoogleTranslator(source='en', target='pt')
        self.original_title = self.title
        self.title = translator.translate(self.title)
        self.summary = translator.translate(self.summary)


class Reference:
    def __init__(self, article: Article, source: str) -> None:
        self.article = article
        self.source = source

    def format_authors_name(self) -> str:
        formated_authors = []
        for author in self.article.authors:
            author = author.strip()
            splited_name = author.split(" ")
            first_letter = splited_name[0][0]
            last_name = splited_name[1]
            formated_authors.append(f"{last_name}, {first_letter}.")
        return formated_authors

    def format_publish_year(self) -> str:
        year = self.article.published.split("-")[0]
        return f"({year})"

    def build_citing(self) -> str:
        authors_name = self.format_authors_name()
        authors_str = " ,& ".join(authors_name)
        publish_year = self.format_publish_year()
        if self.article.original_title:
            title = self.article.original_title
        else:
            title = self.article.title
        self.citation = f"{authors_str} {publish_year}. {title}. {self.source}."
        return f"{authors_str} {publish_year}. {title}. {self.source}."


class ArxivArticle(Article):
    def __init__(self, title: str, published: str, authors: List, summary: str, arxiv_id: str) -> None:
        self.title = title
        self.published = published
        self.authors = authors
        self.summary = summary
        self.arxiv_id = arxiv_id
        self.original_title = None


class ArxivReference(Reference):
    def __init__(self, article: Article) -> None:
        self.article = article
        self.source = "arXiv"

    def format_arxiv_id(self):
        splitted = self.article.arxiv_id.split("abs/")
        return splitted[1]

    def build_citing(self) -> str:
        authors_name = self.format_authors_name()
        authors_str = " ,& ".join(authors_name)
        publish_year = self.format_publish_year()
        formated_id = self.format_arxiv_id()
        if self.article.original_title:
            title = self.article.original_title
        else:
            title = self.article.title

        self.citation = f"{authors_str} {publish_year}. {title}. {self.source}:{formated_id}"
        return f"{authors_str} {publish_year}. {title}. {self.source}:{formated_id}"


class Researcher:
    def __init__(self, search_query: str, translate: str) -> None:
        self.search_query = search_query
        self.is_clean_query = False
        self.translate = True if translate == "true" else False

    def clean_query(self):
        self.is_clean_query = True
        self.search_query = self.search_query.replace(" ", "+")

    def translate_query(self):
        translated = GoogleTranslator(source='auto', target='en').translate(self.search_query)
        return translated

    def search(self):
        self.search_query = self.translate_query()
        if not self.is_clean_query:
            self.clean_query()

        url = f"http://export.arxiv.org/api/query?search_query=all:{self.search_query}&start=0&max_results=5"

        root = self.fetch_xml(url=url)
        return self.parse_xml(root=root)

    def fetch_xml(self, url: str):
        response = urllib.request.urlopen(url)
        xml_data = response.read()
        return ET.fromstring(xml_data)

    def parse_xml(self, root):
        refs = []
        for entry in root.iter(f"{{http://www.w3.org/2005/Atom}}entry"):
            title = entry.find(f"{{http://www.w3.org/2005/Atom}}title").text
            published = entry.find(f"{{http://www.w3.org/2005/Atom}}published").text
            authors = [author.find(f"{{http://www.w3.org/2005/Atom}}name").text for author in entry.findall(f"{{http://www.w3.org/2005/Atom}}author")]
            summary = entry.find(f"{{http://www.w3.org/2005/Atom}}summary").text
            id_element = entry.find(f"{{http://www.w3.org/2005/Atom}}id").text

            art = ArxivArticle(title, published, authors, summary, id_element)
            if self.translate:
                art.translate()
            art_ref = ArxivReference(art)
            art_ref.build_citing()
            refs.append(art_ref)
        return refs
