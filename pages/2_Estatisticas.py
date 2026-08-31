import streamlit as st
import plotly.express as px
from utils import carregar_asteroides, render_sidebar
from estilo import aplicar_tema_espacial, renderizar_hero
import warnings
from PIL import Image

icone = Image.open("images/logo.png")
warnings.simplefilter(action='ignore', category=FutureWarning)

# Configuração da página
st.set_page_config(page_title="Estatísticas - NEO Monitor", page_icon=icone, layout="wide")

# Fundo escuro com estrelas + animações de entrada
aplicar_tema_espacial()

# Renderiza a barra lateral
render_sidebar()

try:
    df = carregar_asteroides()
except Exception as e:
    st.error("Não foi possível carregar os dados. Use a barra lateral para atualizar.")
    st.stop()

# Substitui o st.title pelo Hero (Capa) padronizado
renderizar_hero(
    "Estatísticas Detalhadas",
    "Análise de Distribuição e Comportamento dos NEOs"
)

st.divider()

# Dicionário de cores padrão para manter a consistência visual
mapa_cores = {True: '#FF2A5F', False: '#00F0FF'}

# Layout padrão para os gráficos do Plotly ficarem com o visual "Glassmorphism/HUD"
layout_espacial = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#E8E8E8',
    font_family='JetBrains Mono, monospace',
    legend_title_text='',
    xaxis=dict(gridcolor='rgba(0,240,255,0.08)'),
    yaxis=dict(gridcolor='rgba(0,240,255,0.08)'),
    margin=dict(t=50, b=10, l=10, r=10),
)

tab1, tab2, tab3 = st.tabs(["Tamanhos", "Velocidades", "Distâncias"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribuição de Tamanhos", divider="blue")
        fig_hist = px.histogram(
            df, 
            x='diametro_max_km', 
            nbins=30, 
            color='perigoso',
            color_discrete_map=mapa_cores,
            labels={'diametro_max_km': 'Diâmetro Máximo (km)', 'count': 'Quantidade'}
        )
        fig_hist.update_layout(**layout_espacial)
        st.plotly_chart(fig_hist, width='stretch')
        
    with col2:
        st.subheader("Top 10 Maiores", divider="blue")
        top10 = df.nlargest(10, 'diametro_max_km')
        fig_bar = px.bar(
            top10, 
            x='nome', 
            y='diametro_max_km', 
            color='perigoso', 
            color_discrete_map=mapa_cores,
            labels={'nome': 'Asteroide', 'diametro_max_km': 'Diâmetro (km)'}
        )
        fig_bar.update_layout(**layout_espacial)
        st.plotly_chart(fig_bar, width='stretch')

with tab2:
    st.subheader("Relação // Tamanho × Velocidade", divider="blue")
    fig_scatter = px.scatter(
        df, 
        x='diametro_max_km', 
        y='velocidade_kmh', 
        color='perigoso',
        color_discrete_map=mapa_cores,
        hover_data=['nome'],
        labels={
            'diametro_max_km': 'Diâmetro Máximo (km)', 
            'velocidade_kmh': 'Velocidade (km/h)',
            'perigoso': 'Perigoso'
        },
        opacity=0.8
    )
    # Adicionando contorno aos marcadores (igual na home)
    fig_scatter.update_traces(
        marker=dict(size=10, line=dict(width=1, color='rgba(255,255,255,0.3)'))
    )
    fig_scatter.update_layout(**layout_espacial)
    st.plotly_chart(fig_scatter, width='stretch')

with tab3:
    st.subheader("Distribuição de Distâncias Lunares", divider="blue")
    fig_box = px.box(
        df, 
        x='perigoso', 
        y='distancia_lunar', 
        color='perigoso',
        color_discrete_map=mapa_cores,
        labels={
            'perigoso': 'Classificação de Perigo',
            'distancia_lunar': 'Distância (Distâncias Lunares)'
        }
    )
    fig_box.update_layout(**layout_espacial)
    # Remove o eixo X do boxplot para ficar mais limpo já que a cor e legenda já indicam
    fig_box.update_xaxes(showticklabels=False)
    st.plotly_chart(fig_box, width='stretch')