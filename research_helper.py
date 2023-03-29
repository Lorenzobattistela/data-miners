import urllib.request
import xml.etree.ElementTree as ET
from typing import List

class Article:
    def __init__(self, title: str, published: str, authors: List, summary: str) -> None:
        self.title = title
        self.published = published
        self.authors = authors
        self.summary = summary

class Reference:
    def __init__(self, article: Article, source: str) -> None:
        self.article = article
        self.source = source
    
    def format_authors_name(self) -> str:
        formated_authors = []
        for author in self.article.authors:
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
        return f"{authors_str} {publish_year}. {self.article.title}. {self.source}."

class ArxivArticle(Article):
    def __init__(self, title: str, published: str, authors: List, summary: str, arxiv_id: str) -> None:
        self.title = title
        self.published = published
        self.authors = authors
        self.summary = summary
        self.arxiv_id = arxiv_id

class ArxivReference(Reference):
    def __init__(self, article: Article) -> None:
        self.article = article
        self.source = f"arXiv"
    
    def format_arxiv_id(self):
        splitted = self.article.arxiv_id.split("abs/")
        return splitted[1]

    def build_citing(self) -> str:
        authors_name = self.format_authors_name()
        authors_str = " ,& ".join(authors_name)
        publish_year = self.format_publish_year()
        formated_id = self.format_arxiv_id() 
        return f"{authors_str} {publish_year}. {self.article.title}. {self.source}:{formated_id}"

search_query = input("Enter a search query: ")
search_query = search_query.replace(" ", "+")

url = f"http://export.arxiv.org/api/query?search_query=all:{search_query}&start=0&max_results=5"
response = urllib.request.urlopen(url)
xml_data = response.read()

root = ET.fromstring(xml_data)


for entry in root.iter(f"{{http://www.w3.org/2005/Atom}}entry"):
    title = entry.find(f"{{http://www.w3.org/2005/Atom}}title").text
    published = entry.find(f"{{http://www.w3.org/2005/Atom}}published").text
    authors = [author.find(f"{{http://www.w3.org/2005/Atom}}name").text for author in entry.findall(f"{{http://www.w3.org/2005/Atom}}author")]
    summary = entry.find(f"{{http://www.w3.org/2005/Atom}}summary").text
    id_element = entry.find(f"{{http://www.w3.org/2005/Atom}}id").text
    
    art = ArxivArticle(title, published, authors, summary, id_element)
    art_ref = ArxivReference(art)
    print(art_ref.build_citing())