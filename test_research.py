from research_helper import Article, Reference, Researcher


def test_article_creation():
    article = Article(
        title="Test title",
        published="2021-01-01",
        authors=["Test Author"],
        summary="Test summary",
    )
    assert article.title == "Test title"
    assert article.published == "2021-01-01"
    assert article.authors == ["Test Author"]
    assert article.summary == "Test summary"


def test_article_translation():
    article = Article(
        title="Test title",
        published="2021-01-01",
        authors=["Test Author"],
        summary="Test summary",
    )
    article.translate()
    assert article.title != "Test title"
    assert article.summary != "Test summary"
    assert article.original_title == "Test title"


def test_reference_creation():
    article = Article(
        title="Test title",
        published="2021-01-01",
        authors=["Test Author"],
        summary="Test summary",
    )
    reference = Reference(article, "Test source")
    assert reference.article == article
    assert reference.source == "Test source"


def test_reference_authors_formatting():
    article = Article(
        title="Test title",
        published="2021-01-01",
        authors=["Test Author", "Test Author2"],
        summary="Test summary",
    )
    reference = Reference(article, "Test source")
    assert reference.format_authors_name() == ["Author, T.", "Author2, T."]


def test_reference_publish_year_formatting():
    article = Article(
        title="Test title",
        published="2021-01-01",
        authors=["Test Author", "Test Author 2"],
        summary="Test summary",
    )
    reference = Reference(article, "Test source")
    assert reference.format_publish_year() == "(2021)"


def test_reference_citing():
    article = Article(
        title="Test title",
        published="2021-01-01",
        authors=["Test Author", "Test Author2"],
        summary="Test summary",
    )
    reference = Reference(article, "Test source")
    assert (
        reference.build_citing() == "Author, T. ,& Author2, T. (2021). Test title. Test source."
    )


def test_researcher_creation():
    researcher = Researcher("Test query", False)
    assert researcher.search_query == "Test query"
    assert not researcher.is_clean_query
    assert not researcher.translate


def test_researcher_clean_query():
    researcher = Researcher("Test query", False)
    researcher.clean_query()
    assert researcher.search_query == "Test+query"
    assert researcher.is_clean_query
    assert not researcher.translate


def test_researcher_translate():
    researcher = Researcher("testando", True)
    assert researcher.translate_query() == "testing"
