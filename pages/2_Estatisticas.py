import streamlit as st
import plotly.express as px
from utils import carregar_asteroides, render_sidebar

st.set_page_config(page_title="Estatísticas - NEO Monitor", page_icon="📊", layout="wide")
render_sidebar()

try:
    df = carregar_asteroides()
except Exception as e:
    st.error("Não foi possível carregar os dados.")
    st.stop()

st.title("📊 Estatísticas Detalhadas")

tab1, tab2, tab3 = st.tabs(["Tamanhos", "Velocidades", "Distâncias"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        fig_hist = px.histogram(df, x='diametro_max_km', nbins=30, title="Distribuição de Tamanhos")
        st.plotly_chart(fig_hist, width='stretch')
    with col2:
        top10 = df.nlargest(10, 'diametro_max_km')
        fig_bar = px.bar(top10, x='nome', y='diametro_max_km', color='perigoso', title="Top 10 Maiores")
        st.plotly_chart(fig_bar, width='stretch')

with tab2:
    fig_scatter = px.scatter(df, x='diametro_max_km', y='velocidade_kmh', color='perigoso',
                             title="Tamanho vs Velocidade", hover_data=['nome'])
    st.plotly_chart(fig_scatter, width='stretch')

with tab3:
    fig_box = px.box(df, x='perigoso', y='distancia_lunar', color='perigoso',
                     title="Distribuição de Distâncias")
    st.plotly_chart(fig_box, width='stretch')
