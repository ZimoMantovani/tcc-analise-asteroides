import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="NEO Monitor - Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== FUNÇÕES AUXILIARES ==========
@st.cache_resource
def get_database_connection():
    usuario = "postgres"
    senha = os.getenv('DB_PASSWORD', 'postgres123')
    connection_string = f"postgresql://{usuario}:{quote_plus(senha)}@localhost:5432/tcc_asteroides?client_encoding=utf8"
    return create_engine(connection_string, connect_args={'client_encoding': 'utf8'})

@st.cache_data(ttl=300)
def carregar_asteroides():
    engine = get_database_connection()
    df = pd.read_sql("SELECT * FROM asteroides ORDER BY data_aproximacao", engine)
    return df

# ========== SIDEBAR ==========
with st.sidebar:
    st.image("https://www.nasa.gov/wp-content/uploads/2023/03/nasa-logo-web-rgb.png", width=200)
    st.title("🌍 NEO Monitor")
    st.markdown("**Near Earth Objects**")
    
    st.divider()
    
    # Menu de navegação
    pagina = st.radio(
        "Navegação:",
        ["🏠 Home", "📊 Estatísticas", "🔍 Explorador", "ℹ️ Sobre"]
    )
    
    st.divider()
    
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # Informações do sistema
    st.caption("**Status do Sistema:**")
    try:
        df_test = carregar_asteroides()
        st.success(f"✅ {len(df_test)} asteroides")
        st.caption(f"Última atualização: {pd.Timestamp.now().strftime('%H:%M:%S')}")
    except:
        st.error("❌ Erro de conexão")

# ========== CARREGAR DADOS ==========
try:
    df = carregar_asteroides()
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.stop()

# ========== PÁGINAS ==========

if pagina == "🏠 Home":
    st.title("🌍 Painel de Monitoramento de Asteroides")
    st.markdown("### Sistema de Análise de Objetos Próximos à Terra (NEOs)")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total de NEOs", len(df))
    
    with col2:
        perigosos = len(df[df['perigoso'] == True])
        st.metric("🚨 Perigosos", perigosos, delta=f"{perigosos/len(df)*100:.1f}%")
    
    with col3:
        st.metric("📏 Maior", f"{df['diametro_max_km'].max():.2f} km")
    
    with col4:
        st.metric("⚡ Mais Rápido", f"{df['velocidade_kmh'].max():,.0f} km/h")
    
    st.divider()
    
    # Gráfico de pizza: Perigosos vs Seguros
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        st.subheader("📊 Classificação de Periculosidade")
        contagem = df['perigoso'].value_counts()
        fig_pizza = px.pie(
            values=contagem.values,
            names=['Seguro', 'Perigoso'],
            color_discrete_sequence=['#00cc66', '#ff4444']
        )
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    with col_dir:
        st.subheader("🏆 Top 5 Maiores Asteroides")
        top5 = df.nlargest(5, 'diametro_max_km')[['nome', 'diametro_max_km', 'perigoso']]
        for idx, row in top5.iterrows():
            icone = "🚨" if row['perigoso'] else "✅"
            st.write(f"{icone} **{row['nome']}** - {row['diametro_max_km']:.3f} km")
    
    st.divider()
    
    # Próximas aproximações
    st.subheader("📅 Próximas Aproximações (7 dias)")
    proximos = df.head(10)[['nome', 'data_aproximacao', 'distancia_lunar', 'perigoso']]
    st.dataframe(proximos, use_container_width=True, hide_index=True)

elif pagina == "📊 Estatísticas":
    st.title("📊 Estatísticas Detalhadas")
    
    tab1, tab2, tab3 = st.tabs(["Tamanhos", "Velocidades", "Distâncias"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig_hist = px.histogram(df, x='diametro_max_km', nbins=30, title="Distribuição de Tamanhos")
            st.plotly_chart(fig_hist, use_container_width=True)
        with col2:
            top10 = df.nlargest(10, 'diametro_max_km')
            fig_bar = px.bar(top10, x='nome', y='diametro_max_km', color='perigoso', title="Top 10 Maiores")
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        fig_scatter = px.scatter(df, x='diametro_max_km', y='velocidade_kmh', color='perigoso',
                                 title="Tamanho vs Velocidade", hover_data=['nome'])
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab3:
        fig_box = px.box(df, x='perigoso', y='distancia_lunar', color='perigoso',
                         title="Distribuição de Distâncias")
        st.plotly_chart(fig_box, use_container_width=True)

elif pagina == "🔍 Explorador":
    st.title("🔍 Explorador de Asteroides")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_perigoso = st.selectbox("Tipo:", ["Todos", "Perigosos", "Seguros"])
    with col2:
        tamanho_min = st.number_input("Diâmetro mín (km):", value=0.0, step=0.01)
    with col3:
        velocidade_min = st.number_input("Velocidade mín (km/h):", value=0.0, step=1000.0)
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if filtro_perigoso == "Perigosos":
        df_filtrado = df_filtrado[df_filtrado['perigoso'] == True]
    elif filtro_perigoso == "Seguros":
        df_filtrado = df_filtrado[df_filtrado['perigoso'] == False]
    
    df_filtrado = df_filtrado[
        (df_filtrado['diametro_max_km'] >= tamanho_min) &
        (df_filtrado['velocidade_kmh'] >= velocidade_min)
    ]
    
    st.write(f"**{len(df_filtrado)} asteroides encontrados**")
    st.dataframe(df_filtrado[['nome', 'data_aproximacao', 'diametro_max_km', 'velocidade_kmh', 'distancia_lunar', 'perigoso']], 
                 use_container_width=True, height=500)

else:  # Sobre
    st.title("Sobre o Projeto")
    st.markdown("""
    ### NEO Monitor - Sistema de Monitoramento de Asteroides
        
    #### Objetivo
    Monitorar e analisar objetos próximos à Terra (NEOs - Near Earth Objects) utilizando 
    dados da NASA NeoWs API, processamento ETL em Python e visualização interativa.
    
    #### Tecnologias
    - **Backend:** Python, SQLAlchemy, Pandas
    - **Frontend:** Streamlit, Plotly
    - **Banco de Dados:** PostgreSQL
    - **API:** NASA NeoWs
    
    #### Funcionalidades
    - Coleta automatizada de dados da NASA
    - Armazenamento histórico em banco de dados
    - Análise estatística de asteroides
    - Visualizações interativas
    - Classificação de periculosidade
    
    #### Fonte de Dados
    [NASA NeoWs API](https://api.nasa.gov/)
    
    ---
    **Desenvolvido por:** Symon O. Mantovani
    **Instituição:** IFSP PRC
    **Ano:** 2026
    """)