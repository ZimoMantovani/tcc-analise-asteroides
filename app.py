import streamlit as st
import plotly.express as px
from src.utils import carregar_asteroides, render_sidebar

from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container

from src.estilo import aplicar_tema_espacial, renderizar_hero, hud_tag
from PIL import Image
icone = Image.open("assets/logo.png")
# Configuração da página (deve ser a primeira chamada Streamlit)
st.set_page_config(page_title="Home - NEO Monitor", page_icon=icone, layout="wide")

# Fundo escuro com estrelas + animações de entrada
aplicar_tema_espacial()

# Renderiza a barra lateral padrão customizada
render_sidebar()

try:
    df = carregar_asteroides()
except Exception as e:
    st.error("Não foi possível carregar os dados. Use a barra lateral para atualizar.")
    st.stop()

# Seção de capa com a Imagem Astronômica do Dia da NASA (APOD)
renderizar_hero(
    "Painel de Monitoramento de Asteroides",
    "Sistema de Análise de Objetos Próximos à Terra (NEOs)",
)

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de NEOs", len(df))

with col2:
    perigosos = len(df[df['perigoso'] == True])
    st.metric("Objetos Perigosos", perigosos, delta=f"{perigosos/len(df)*100:.1f}%")

with col3:
    st.metric("Maior Diâmetro", f"{df['diametro_max_km'].max():.2f} km")

with col4:
    st.metric("Velocidade Máxima", f"{df['velocidade_kmh'].max():,.0f} km/h")

# Cards de métrica em "vidro" com acento ciano
style_metric_cards(
    background_color="rgba(20, 27, 46, 0.55)",
    border_left_color="#00F0FF",
    border_color="rgba(0, 240, 255, 0.25)",
    box_shadow=True,
)

st.divider()

col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("Mapa de Risco // Distância × Diâmetro", divider="blue")

    # Scatter plot no lugar do donut anterior: em vez de repetir a mesma
    # informação já mostrada no card "Objetos Perigosos" (só 2 números),
    # mostra a relação real entre distância de aproximação e tamanho do
    # objeto — bem mais informativo, e lembra um radar/mapa de campo.
    fig_scatter = px.scatter(
        df,
        x='distancia_lunar',
        y='diametro_max_km',
        color='perigoso',
        color_discrete_map={True: '#FF2A5F', False: '#00F0FF'},
        labels={
            'distancia_lunar': 'Distância (distâncias lunares)',
            'diametro_max_km': 'Diâmetro estimado (km)',
            'perigoso': 'Perigoso',
        },
        hover_name='nome',
        opacity=0.8,
    )
    fig_scatter.update_traces(
        marker=dict(size=10, line=dict(width=1, color='rgba(255,255,255,0.3)'))
    )
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#E8E8E8',
        font_family='JetBrains Mono, monospace',
        legend_title_text='',
        xaxis=dict(gridcolor='rgba(0,240,255,0.08)'),
        yaxis=dict(gridcolor='rgba(0,240,255,0.08)'),
        margin=dict(t=10, b=10, l=10, r=10),
    )
    st.plotly_chart(fig_scatter, width='stretch')

with col_dir:
    st.subheader("Top 5 // Maiores Objetos Detectados", divider="blue")

    # Injeta o CSS apontando para a key 'top5_container'
    st.markdown("""
        <style>
        .st-key-top5_container {
            border: 1px solid rgba(0, 240, 255, 0.25);
            border-radius: 0.75rem;
            padding: 1.2rem 1.5rem;
            background-color: rgba(20, 27, 46, 0.55);
            backdrop-filter: blur(6px);
            box-shadow: 0 0 16px rgba(0, 240, 255, 0.06);
        }
        </style>
    """, unsafe_allow_html=True)

    # Card de vidro com acento ciano usando o container nativo
    with st.container(key="top5_container"):
        top5 = df.nlargest(5, 'diametro_max_km')[['nome', 'diametro_max_km', 'perigoso']]
        for idx, row in top5.iterrows():
            if row['perigoso']:
                tag = hud_tag("PERIGOSO", cor="#FF2A5F")
            else:
                tag = hud_tag("SEGURO", cor="#00F0FF")
            st.markdown(
                f"{tag} &nbsp; **{row['nome']}** — {row['diametro_max_km']:.3f} km",
                unsafe_allow_html=True,
            )

st.divider()

# Próximas aproximações
st.subheader("Próximas Aproximações // Janela de 7 Dias", divider="blue")
proximos = df.head(10)[['nome', 'data_aproximacao', 'distancia_lunar', 'perigoso']]
st.dataframe(proximos, width='stretch', hide_index=True)