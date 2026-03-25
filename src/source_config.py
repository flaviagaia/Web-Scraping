from __future__ import annotations

AGENCIA_BRASIL_ROOT = "https://agenciabrasil.ebc.com.br/"

THEME_PATTERNS = {
    "politica": "/politica/noticia/",
    "economia": "/economia/noticia/",
}

INVALID_URL_SNIPPETS = [
    "/en/",
    "/es/",
    "noticiahttps://",
]

EXCLUDED_REFERENCE_TERMS: set[str] = set()

STOPWORDS_PT = {
    "a", "ao", "aos", "aquela", "aquele", "aqueles", "as", "até", "com", "como", "da", "das",
    "de", "dela", "dele", "deles", "depois", "do", "dos", "e", "ela", "ele", "eles", "em", "entre",
    "era", "essa", "esse", "esta", "está", "estao", "estas", "este", "estes", "foi", "foram",
    "há", "isso", "isto", "já", "la", "lhe", "mais", "mas", "na", "nas", "nem", "no", "nos", "o",
    "os", "ou", "para", "pela", "pelas", "pelo", "pelos", "por", "qual", "que", "quem", "se",
    "sem", "ser", "seu", "seus", "sua", "suas", "sobre", "tambem", "também", "tem", "ter", "um",
    "uma", "uns", "umas", "vai", "vão", "dos", "das", "ainda", "após", "contra", "durante", "entre",
    "disse", "afirmou", "informou", "declarou", "segundo", "sobre", "nesta", "neste", "nestas",
    "nestes", "dessa", "desse", "desses", "dessas", "apenas", "todo", "toda", "todos", "todas",
    "durante", "entrevista", "reportagem", "agora", "ontem", "hoje", "amanhã", "pode", "podem",
    "deve", "devem", "sido", "estão", "estava", "força", "feira", "anos", "ano", "dia", "dias",
    "mesmo", "mesma", "mesmos", "mesmas", "além", "apresentou", "destacou", "explicou", "discurso",
    "governo", "presidente", "ministro", "prefeito", "cidade", "federal", "nacional", "brasileiro",
    "brasileira", "brasileiros", "brasileiras", "país", "países",
}

RULE_BASED_ENTITIES = {
    "PERSON": [
        "Lula",
        "Luiz Inácio Lula da Silva",
        "Fernando Haddad",
        "Jair Bolsonaro",
        "Alexandre de Moraes",
        "Geraldo Alckmin",
        "Gabriel Galípolo",
    ],
    "ORG": [
        "Banco Central",
        "Receita Federal",
        "Congresso Nacional",
        "Supremo Tribunal Federal",
        "STF",
        "Câmara dos Deputados",
        "Senado Federal",
        "IBGE",
        "Copom",
        "B3",
        "Caixa Econômica Federal",
    ],
    "GPE": [
        "Brasil",
        "Brasília",
        "Rio de Janeiro",
        "São Paulo",
        "Bogotá",
        "América do Sul",
        "Estados Unidos",
        "China",
    ],
    "ECONOMIC_TERM": [
        "Selic",
        "IPCA",
        "PIB",
        "inflação",
        "juros",
        "imposto de renda",
        "combustíveis",
        "mercado",
        "orçamento",
        "receita",
    ],
}
