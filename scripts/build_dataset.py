from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard_utils import ARTICLES_PATH, ENTITIES_PATH, KEYWORDS_PATH, SUMMARY_PATH
from src.nlp_pipeline import analyze_articles
from src.scraper import records_to_dicts, scrape_articles


def main() -> None:
    records = scrape_articles(max_per_theme=12)
    articles_df = pd.DataFrame(records_to_dicts(records))
    artifacts = analyze_articles(articles_df)

    ARTICLES_PATH.parent.mkdir(parents=True, exist_ok=True)
    artifacts.articles.to_csv(ARTICLES_PATH, index=False)
    artifacts.entities.to_csv(ENTITIES_PATH, index=False)
    artifacts.keywords.to_csv(KEYWORDS_PATH, index=False)
    SUMMARY_PATH.write_text(json.dumps(artifacts.metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Articles saved to: {ARTICLES_PATH}")
    print(f"Entities saved to: {ENTITIES_PATH}")
    print(f"Keywords saved to: {KEYWORDS_PATH}")
    print(f"Summary saved to: {SUMMARY_PATH}")
    print(f"Articles collected: {artifacts.metadata['article_count']}")
    print(f"Entities extracted: {artifacts.metadata['entity_count']}")
    print(f"NLP status: {artifacts.metadata['nlp_status']}")


if __name__ == "__main__":
    main()
