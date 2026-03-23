from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Iterable

from newspaper import Article, build

from .source_config import AGENCIA_BRASIL_ROOT, INVALID_URL_SNIPPETS, THEME_PATTERNS


@dataclass
class ArticleRecord:
    source: str
    theme: str
    url: str
    title: str
    publish_date: str
    authors: str
    text: str
    summary: str
    word_count: int


def discover_article_urls(max_per_theme: int = 12) -> dict[str, list[str]]:
    paper = build(AGENCIA_BRASIL_ROOT, memoize_articles=False, fetch_images=False, language="pt")
    urls = [article.url for article in paper.articles]

    discovered: dict[str, list[str]] = {}
    for theme, pattern in THEME_PATTERNS.items():
        filtered = []
        for url in urls:
            if pattern not in url:
                continue
            if any(snippet in url for snippet in INVALID_URL_SNIPPETS):
                continue
            if url not in filtered:
                filtered.append(url)
            if len(filtered) >= max_per_theme:
                break
        discovered[theme] = filtered
    return discovered


def parse_article(url: str, theme: str, source: str = "Agência Brasil") -> ArticleRecord | None:
    article = Article(url, language="pt")
    article.download()
    article.parse()

    text = (article.text or "").strip()
    title = (article.title or "").strip()
    if not text or not title:
        return None

    publish_date = ""
    if isinstance(article.publish_date, datetime):
        publish_date = article.publish_date.isoformat()

    authors = ", ".join(article.authors) if article.authors else ""
    summary = text[:400].replace("\n", " ").strip()

    return ArticleRecord(
        source=source,
        theme=theme,
        url=url,
        title=title,
        publish_date=publish_date,
        authors=authors,
        text=text,
        summary=summary,
        word_count=len(text.split()),
    )


def scrape_articles(max_per_theme: int = 12) -> list[ArticleRecord]:
    discovered = discover_article_urls(max_per_theme=max_per_theme)
    records: list[ArticleRecord] = []
    for theme, urls in discovered.items():
        for url in urls:
            try:
                record = parse_article(url=url, theme=theme)
            except Exception:
                continue
            if record is not None:
                records.append(record)
    return records


def records_to_dicts(records: Iterable[ArticleRecord]) -> list[dict]:
    return [asdict(record) for record in records]

