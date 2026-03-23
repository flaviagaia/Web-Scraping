from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

from .source_config import STOPWORDS_PT


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
ARTICLES_PATH = DATA_DIR / "articles.csv"
ENTITIES_PATH = DATA_DIR / "entities.csv"
KEYWORDS_PATH = DATA_DIR / "keywords.csv"
SUMMARY_PATH = DATA_DIR / "summary.json"
TOKEN_PATTERN = re.compile(r"\b[a-zA-ZÀ-ÿ]{4,}\b")


def load_outputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    articles = pd.read_csv(ARTICLES_PATH)
    entities = pd.read_csv(ENTITIES_PATH) if ENTITIES_PATH.exists() else pd.DataFrame(columns=["entity", "label"])
    keywords = pd.read_csv(KEYWORDS_PATH) if KEYWORDS_PATH.exists() else pd.DataFrame(columns=["keyword", "count"])
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8")) if SUMMARY_PATH.exists() else {}
    return articles, entities, keywords, summary


def render_wordcloud(text: str):
    wordcloud = WordCloud(width=1400, height=700, background_color="white", colormap="viridis").generate(text)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig


def keywords_from_texts(texts: list[str], limit: int = 30) -> pd.DataFrame:
    counts: dict[str, int] = {}
    for text in texts:
        for token in TOKEN_PATTERN.findall(text.lower()):
            if token in STOPWORDS_PT:
                continue
            counts[token] = counts.get(token, 0) + 1

    rows = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:limit]
    return pd.DataFrame(rows, columns=["keyword", "count"])
