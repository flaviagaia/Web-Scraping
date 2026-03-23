from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard_utils import keywords_from_texts, load_outputs, render_wordcloud


st.set_page_config(page_title="Monitor de Noticias Politicas e Economicas", layout="wide")

st.title("Monitor de Noticias Politicas e Economicas")
st.caption("Web scraping com newspaper + NLP com spaCy/fallback + dashboard em Streamlit.")

try:
    articles, entities, keywords, summary = load_outputs()
except FileNotFoundError:
    st.warning(
        "Os arquivos de dados ainda não foram gerados. Execute `python3 scripts/build_dataset.py` para montar a base analítica."
    )
    st.stop()

theme_filter = st.sidebar.multiselect(
    "Tema",
    sorted(articles["theme"].dropna().unique().tolist()),
    default=sorted(articles["theme"].dropna().unique().tolist()),
)

source_filter = st.sidebar.multiselect(
    "Fonte",
    sorted(articles["source"].dropna().unique().tolist()),
    default=sorted(articles["source"].dropna().unique().tolist()),
)

filtered = articles[articles["theme"].isin(theme_filter) & articles["source"].isin(source_filter)].copy()
filtered_entities = entities[entities["url"].isin(filtered["url"])] if not entities.empty else entities
filtered["publish_date_dt"] = pd.to_datetime(filtered["publish_date"], errors="coerce")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Artigos", len(filtered))
col2.metric("Fontes", filtered["source"].nunique())
col3.metric("Entidades", len(filtered_entities))
col4.metric("Palavras media", int(filtered["word_count"].mean()) if len(filtered) else 0)

st.info(summary.get("nlp_status", "NLP status unavailable"))

left, right = st.columns([1, 1])
with left:
    st.subheader("Artigos por tema")
    st.bar_chart(filtered["theme"].value_counts())

with right:
    st.subheader("Artigos por fonte")
    st.bar_chart(filtered["source"].value_counts())

timeline = (
    filtered.dropna(subset=["publish_date_dt"])
    .assign(publish_day=lambda frame: frame["publish_date_dt"].dt.date)
    .groupby("publish_day")
    .size()
    .rename("artigos")
)
if not timeline.empty:
    st.subheader("Linha do tempo de publicações")
    st.line_chart(timeline)

if not filtered_entities.empty:
    st.subheader("Top entidades")
    entity_counts = (
        filtered_entities.groupby(["entity", "label"]).size().reset_index(name="count").sort_values("count", ascending=False).head(15)
    )
    st.dataframe(entity_counts, use_container_width=True)

st.subheader("Nuvem de palavras")
cloud_text = " ".join(filtered["text"].fillna("").tolist())
if cloud_text.strip():
    st.pyplot(render_wordcloud(cloud_text))

st.subheader("Top keywords")
filtered_keywords = keywords_from_texts(filtered["text"].fillna("").tolist(), limit=30)
st.dataframe(filtered_keywords, use_container_width=True)

st.subheader("Artigos coletados")
display_columns = ["publish_date", "theme", "source", "title", "authors", "word_count", "entity_count", "keyword_preview", "url"]
st.dataframe(filtered[display_columns], use_container_width=True, hide_index=True)

with st.expander("Como usar este dashboard"):
    st.markdown(
        """
        - Use os filtros laterais para separar política e economia.
        - Observe a distribuição por tema e fonte.
        - Explore as entidades nomeadas e a nuvem de palavras.
        - Use a tabela final para abrir artigos e revisar metadados.
        """
    )
