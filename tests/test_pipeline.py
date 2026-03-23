from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.nlp_pipeline import analyze_articles


class WebScrapingNlpPipelineTest(unittest.TestCase):
    def test_analyze_articles_returns_expected_outputs(self):
        articles = pd.DataFrame(
            [
                {
                    "source": "Agência Brasil",
                    "theme": "politica",
                    "url": "https://example.com/1",
                    "title": "Lula fala sobre orçamento",
                    "publish_date": "2026-03-22T00:00:00",
                    "authors": "Repórter Teste",
                    "text": "Lula discutiu o orçamento com o Congresso Nacional e o Banco Central em Brasília.",
                    "summary": "Resumo 1",
                    "word_count": 12,
                },
                {
                    "source": "Agência Brasil",
                    "theme": "economia",
                    "url": "https://example.com/2",
                    "title": "Petrobras fala sobre combustíveis",
                    "publish_date": "2026-03-22T00:00:00",
                    "authors": "Repórter Teste",
                    "text": "A Petrobras comentou preços dos combustíveis e o impacto da inflação no Brasil.",
                    "summary": "Resumo 2",
                    "word_count": 13,
                },
            ]
        )

        artifacts = analyze_articles(articles)
        self.assertEqual(len(artifacts.articles), 2)
        self.assertGreaterEqual(len(artifacts.entities), 2)
        self.assertGreater(len(artifacts.keywords), 0)
        self.assertIn("entity_count", artifacts.articles.columns)


if __name__ == "__main__":
    unittest.main()

