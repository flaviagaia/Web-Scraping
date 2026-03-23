from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

import pandas as pd

from .source_config import RULE_BASED_ENTITIES, STOPWORDS_PT


TOKEN_PATTERN = re.compile(r"\b[a-zA-ZÀ-ÿ]{4,}\b")


@dataclass
class NlpArtifacts:
    articles: pd.DataFrame
    entities: pd.DataFrame
    keywords: pd.DataFrame
    metadata: dict


def _load_spacy_model():
    try:
        import spacy
    except Exception as exc:
        return None, f"spaCy unavailable in this environment: {type(exc).__name__}"

    for model_name in ["pt_core_news_sm", "xx_ent_wiki_sm"]:
        try:
            return spacy.load(model_name), f"spaCy model loaded: {model_name}"
        except Exception:
            continue

    try:
        nlp = spacy.blank("pt")
        nlp.add_pipe("sentencizer")
        return nlp, "spaCy fallback pipeline loaded without pretrained NER model"
    except Exception as exc:
        return None, f"spaCy fallback unavailable: {type(exc).__name__}"


def _extract_entities_rule_based(text: str) -> list[dict]:
    entities: list[dict] = []
    lowered = text.lower()
    for label, terms in RULE_BASED_ENTITIES.items():
        for term in terms:
            if term.lower() in lowered:
                entities.append({"text": term, "label": label})
    return entities


def _extract_entities(text: str, nlp) -> list[dict]:
    if nlp is None:
        return _extract_entities_rule_based(text)

    try:
        doc = nlp(text)
    except Exception:
        return _extract_entities_rule_based(text)

    if getattr(doc, "ents", None):
        entities = [{"text": ent.text, "label": ent.label_ or "ENTITY"} for ent in doc.ents]
        if entities:
            return entities
    return _extract_entities_rule_based(text)


def _extract_keywords(text: str) -> list[str]:
    tokens = [token.lower() for token in TOKEN_PATTERN.findall(text)]
    return [token for token in tokens if token not in STOPWORDS_PT]


def analyze_articles(articles_df: pd.DataFrame) -> NlpArtifacts:
    nlp, nlp_status = _load_spacy_model()

    entity_rows: list[dict] = []
    keyword_counter: Counter[str] = Counter()
    enriched = articles_df.copy()

    entity_counts_per_article = []
    keyword_preview = []
    for _, row in enriched.iterrows():
        text = row["text"]
        entities = _extract_entities(text, nlp)
        keywords = _extract_keywords(text)

        for entity in entities:
            entity_rows.append(
                {
                    "url": row["url"],
                    "theme": row["theme"],
                    "source": row["source"],
                    "entity": entity["text"],
                    "label": entity["label"],
                }
            )

        keyword_counter.update(keywords)
        entity_counts_per_article.append(len(entities))
        keyword_preview.append(", ".join([kw for kw, _ in Counter(keywords).most_common(8)]))

    enriched["entity_count"] = entity_counts_per_article
    enriched["keyword_preview"] = keyword_preview

    entities_df = pd.DataFrame(entity_rows)
    keyword_df = pd.DataFrame(keyword_counter.most_common(200), columns=["keyword", "count"])

    metadata = {
        "article_count": int(len(enriched)),
        "entity_count": int(len(entities_df)),
        "nlp_status": nlp_status,
    }

    return NlpArtifacts(
        articles=enriched,
        entities=entities_df,
        keywords=keyword_df,
        metadata=metadata,
    )

