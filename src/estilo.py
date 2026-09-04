"""
Módulo de estilo visual "espacial" para o NEO Monitor.

Uso: chame aplicar_tema_espacial() logo após o st.set_page_config() em
cada página, e opcionalmente renderizar_hero(titulo, subtitulo) para
exibir uma seção de capa com a Imagem Astronômica do Dia da NASA (APOD).

Você não precisa entender nem editar o CSS abaixo — é só importar e chamar
as duas funções. Tudo é gerado em Python.
"""
import os
import random

import requests
import streamlit as st


def _gerar_estrelas(quantidade=200, seed=42):
    """
    Gera posições aleatórias de 'estrelas' como camadas de radial-gradient CSS.
    seed fixo garante que o padrão de estrelas não mude a cada rerun da página
    (senão elas "pulariam" de lugar toda vez que você interagisse com algo).
    """
    random.seed(seed)
    camadas = []
    for _ in range(quantidade):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        tamanho = random.choice([1, 1, 1, 2])  # maioria pequena, algumas maiores
        opacidade = random.uniform(0.3, 1.0)
        camadas.append(
            f"radial-gradient({tamanho}px {tamanho}px at {x:.2f}% {y:.2f}%, "
            f"rgba(255,255,255,{opacidade:.2f}), transparent)"
        )
    return ",\n            ".join(camadas)


def aplicar_tema_espacial():
    """Injeta CSS: fundo escuro com estrelas, leve 'parallax' ao rolar,
    tipografia monospace estilo terminal, e visual de painel técnico (HUD)."""
    estrelas_css = _gerar_estrelas()

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

        /* Fundo escuro com estrelas geradas via CSS puro (sem imagens externas) */
        .stApp {{
            background-color: #05070D;
            background-image: {estrelas_css};
            background-attachment: fixed;  /* dá sensação de profundidade ao rolar */
        }}

        /* Fade + leve subida ao carregar cada bloco de conteúdo */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(15px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        [data-testid="stVerticalBlock"] > div {{
            animation: fadeInUp 0.6s ease-out;
        }}

        /* Mais espaço entre seções, pra dar ritmo de "capítulos" ao rolar */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            margin-bottom: 1.5rem;
        }}

        /* Sidebar em "vidro": semi-transparente, deixa as estrelas do fundo
           levemente visíveis por trás, com borda ciano sutil na direita */
        [data-testid="stSidebar"] {{
            background-color: rgba(20, 27, 46, 0.75);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(0, 240, 255, 0.2);
        }}

        /* Tabelas (st.dataframe) com o mesmo tratamento de vidro + leve
           brilho ciano ao redor, reforçando a leitura de "painel técnico" */
        [data-testid="stDataFrame"] {{
            background-color: rgba(20, 27, 46, 0.55);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(0, 240, 255, 0.2);
            border-radius: 0.75rem;
            padding: 0.5rem;
            box-shadow: 0 0 16px rgba(0, 240, 255, 0.06);
        }}

        /* Cards de métrica: mesmo glow sutil ciano */
        [data-testid="stMetric"] {{
            box-shadow: 0 0 16px rgba(0, 240, 255, 0.06);
        }}

        /* Gráficos Plotly: remove qualquer fundo próprio que sobre, deixando
           só o que for definido no update_layout() do próprio gráfico */
        [data-testid="stPlotlyChart"] {{
            background-color: transparent !important;
        }}

        /* Estrelas "piscando" bem sutilmente por cima do fundo */
        @keyframes piscar {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: {estrelas_css};
            opacity: 0.5;
            animation: piscar 4s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }}

        /* Tipografia "terminal de dados": números e rótulos em monospace,
           títulos em caixa alta e espaçada — tira o ar de UI web genérica */
        [data-testid="stMetricValue"] {{
            font-family: 'JetBrains Mono', monospace !important;
        }}
        [data-testid="stMetricLabel"] {{
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.8rem !important;
        }}
        [data-testid="stHeadingWithActionElements"] h1,
        [data-testid="stHeadingWithActionElements"] h2,
        [data-testid="stHeadingWithActionElements"] h3 {{
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        /* Botões estilo "ghost" (contorno ciano, sem preenchimento) —
           menos chamativo que o botão azul sólido padrão do Streamlit */
        [data-testid="stSidebar"] button {{
            background-color: transparent !important;
            border: 1px solid rgba(0, 240, 255, 0.4) !important;
            color: #00F0FF !important;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            font-size: 0.8rem !important;
        }}
        [data-testid="stSidebar"] button:hover {{
            background-color: rgba(0, 240, 255, 0.08) !important;
            border-color: #00F0FF !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def hud_tag(texto: str, cor: str = "#00F0FF") -> str:
    """
    Retorna um HTML de tag estilo terminal/HUD, ex: [ SEGURO ] ou [ PERIGOSO ].
    Use com st.markdown(hud_tag(...), unsafe_allow_html=True).
    """
    return (
        "<span style=\""
        "font-family: 'JetBrains Mono', monospace; "
        f"color: {cor}; "
        f"border: 1px solid {cor}66; "
        "padding: 0.1rem 0.5rem; "
        "border-radius: 0.25rem; "
        "font-size: 0.78rem; "
        "letter-spacing: 0.05em; "
        "white-space: nowrap;"
        f"\">[ {texto.upper()} ]</span>"
    )


@st.cache_data(ttl=60 * 60 * 24)  # busca a imagem só 1x por dia
def _buscar_imagem_apod():
    """
    Busca a Imagem Astronômica do Dia da NASA (APOD).
    Usa a mesma NASA_API_KEY que o etl_completo.py já usa.
    Retorna (url_imagem, titulo) ou None se falhar / não for imagem (às vezes é vídeo).
    """
    api_key = os.getenv('NASA_API_KEY')
    if not api_key:
        return None
    try:
        resp = requests.get(
            "https://api.nasa.gov/planetary/apod",
            params={"api_key": api_key},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("media_type") == "image":
            url = data.get("hdurl") or data.get("url")
            return url, data.get("title")
    except Exception:
        return None
    return None


def renderizar_hero(titulo: str, subtitulo: str):
    """Renderiza uma seção de capa em tela cheia com a imagem real do dia da NASA."""
    resultado = _buscar_imagem_apod()
    imagem_url = resultado[0] if resultado else None
    fundo = f"url('{imagem_url}')" if imagem_url else "none"

    st.markdown(f"""
        <div style="
            background-image: linear-gradient(rgba(5,7,13,0.55), rgba(5,7,13,0.88)), {fundo};
            background-size: cover;
            background-position: center;
            border-radius: 1rem;
            padding: 4.5rem 2rem;
            text-align: center;
            margin-bottom: 2rem;
        ">
            <h1 style="color: white; font-size: 2.8rem; margin-bottom: 0.5rem;">{titulo}</h1>
            <p style="color: #cfd3dc; font-size: 1.15rem;">{subtitulo}</p>
        </div>
    """, unsafe_allow_html=True)

    if resultado and resultado[1]:
        st.caption(f"📷 Imagem Astronômica do Dia (NASA APOD): {resultado[1]}")