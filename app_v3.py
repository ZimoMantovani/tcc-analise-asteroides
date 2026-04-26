"""
Apenas para teste
"""
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
    page_title="NEO Monitor",
    page_icon="🌍",
    layout="wide"
)

# ========== FUNÇÕES ==========
@st.cache_resource
def get_database_connection():
    usuario = "postgres"
    senha = os.getenv('DB_PASSWORD', 'postgres123')
    connection_string = f"postgresql://{usuario}:{quote_plus(senha)}@localhost:5432/tcc_asteroides?client_encoding=utf8"
    engine = create_engine(connection_string, connect_args={'client_encoding': 'utf8'})
    return engine

@st.cache_data(ttl=300)
def carregar_asteroides():
    engine = get_database_connection()
    query = "SELECT * FROM asteroides ORDER BY data_aproximacao"
    df = pd.read_sql(query, engine)
    return df

# ========== INTERFACE ==========
st.title("🌍 Monitoramento de Asteroides - NEO Watch")
st.markdown("**Sistema de Análise de Objetos Próximos à Terra**")

# Botão de atualização na sidebar
with st.sidebar:
    st.header("⚙️ Controles")
    if st.button("🔄 Atualizar Dados", width='stretch'):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    st.info("💡 **Dica:** Use os filtros abaixo para explorar os dados")

# ========== CARREGAR DADOS ==========
try:
    with st.spinner("Carregando dados..."):
        df = carregar_asteroides()
    st.success(f"✅ {len(df)} asteroides carregados!")
except Exception as e:
    st.error(f"❌ Erro: {e}")
    st.stop()

# ========== MÉTRICAS ==========
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total", len(df))

with col2:
    perigosos = len(df[df['perigoso'] == True])
    st.metric("🚨 Perigosos", perigosos, delta=f"{perigosos/len(df)*100:.1f}%")

with col3:
    st.metric("📏 Maior", f"{df['diametro_max_km'].max():.3f} km")

with col4:
    st.metric("🏃 Vel. Média", f"{df['velocidade_kmh'].mean():,.0f} km/h")

st.divider()

# ========== GRÁFICOS ==========

# Seção de Gráficos
tab1, tab2, tab3 = st.tabs(["📊 Distribuição de Tamanhos", "🏃 Velocidades", "🌍 Distâncias"])

with tab1:
    st.subheader("Distribuição de Tamanhos dos Asteroides")
    
    # Histograma
    fig_tamanho = px.histogram(
        df,
        x='diametro_max_km',
        nbins=30,
        title="Frequência por Tamanho (km)",
        labels={'diametro_max_km': 'Diâmetro Máximo (km)', 'count': 'Quantidade'},
        color_discrete_sequence=['#1f77b4']
    )
    fig_tamanho.update_layout(showlegend=False)
    st.plotly_chart(fig_tamanho, width='stretch')
    
    # Top 10 maiores
    st.subheader("🏆 Top 10 Maiores Asteroides")
    top10 = df.nlargest(10, 'diametro_max_km')[['nome', 'diametro_max_km', 'perigoso']]
    
    fig_top10 = px.bar(
        top10,
        x='nome',
        y='diametro_max_km',
        color='perigoso',
        title="",
        labels={'diametro_max_km': 'Diâmetro (km)', 'nome': 'Asteroide'},
        color_discrete_map={True: '#ff4444', False: '#44ff44'}
    )
    st.plotly_chart(fig_top10, width='stretch')

with tab2:
    st.subheader("Análise de Velocidades")
    
    # Gráfico de dispersão: Velocidade vs Tamanho
    fig_vel = px.scatter(
        df,
        x='diametro_max_km',
        y='velocidade_kmh',
        color='perigoso',
        size='diametro_max_km',
        hover_data=['nome'],
        title="Relação Tamanho vs Velocidade",
        labels={
            'diametro_max_km': 'Diâmetro (km)',
            'velocidade_kmh': 'Velocidade (km/h)',
            'perigoso': 'Perigoso'
        },
        color_discrete_map={True: 'red', False: 'blue'}
    )
    st.plotly_chart(fig_vel, width='stretch')

with tab3:
    st.subheader("Distâncias de Aproximação")
    
    # Box plot de distâncias
    fig_dist = px.box(
        df,
        x='perigoso',
        y='distancia_lunar',
        color='perigoso',
        title="Distribuição de Distâncias (em distâncias lunares)",
        labels={
            'distancia_lunar': 'Distância (Luas)',
            'perigoso': 'Potencialmente Perigoso'
        },
        color_discrete_map={True: 'red', False: 'green'}
    )
    st.plotly_chart(fig_dist, width='stretch')
    
    st.info("📏 **Referência:** 1 distância lunar = ~384.400 km (distância Terra-Lua)")

st.divider()

# ========== FILTROS INTERATIVOS ==========
st.subheader("🔍 Explorador de Asteroides")

col_filtro1, col_filtro2 = st.columns(2)

with col_filtro1:
    # Filtro de periculosidade
    filtro_perigoso = st.selectbox(
        "Mostrar asteroides:",
        ["Todos", "Apenas Perigosos", "Apenas Seguros"]
    )

with col_filtro2:
    # Filtro de tamanho
    tamanho_min = st.slider(
        "Diâmetro mínimo (km):",
        min_value=float(df['diametro_min_km'].min()),
        max_value=float(df['diametro_max_km'].max()),
        value=float(df['diametro_min_km'].min()),
        step=0.01
    )

# Aplicar filtros
df_filtrado = df.copy()

if filtro_perigoso == "Apenas Perigosos":
    df_filtrado = df_filtrado[df_filtrado['perigoso'] == True]
elif filtro_perigoso == "Apenas Seguros":
    df_filtrado = df_filtrado[df_filtrado['perigoso'] == False]

df_filtrado = df_filtrado[df_filtrado['diametro_max_km'] >= tamanho_min]

# Exibir tabela filtrada
st.write(f"**{len(df_filtrado)} asteroides encontrados**")

# Preparar dados para exibição
colunas_exibir = ['nome', 'data_aproximacao', 'diametro_max_km', 'distancia_lunar', 'velocidade_kmh', 'perigoso']
df_exibir = df_filtrado[colunas_exibir].copy()

# Renomear e formatar
df_exibir.columns = ['Nome', 'Data', 'Diâmetro (km)', 'Distância (Luas)', 'Velocidade (km/h)', 'Perigoso']
df_exibir['Diâmetro (km)'] = df_exibir['Diâmetro (km)'].apply(lambda x: f"{x:.3f}")
df_exibir['Distância (Luas)'] = df_exibir['Distância (Luas)'].apply(lambda x: f"{x:.2f}")
df_exibir['Velocidade (km/h)'] = df_exibir['Velocidade (km/h)'].apply(lambda x: f"{x:,.0f}")

st.dataframe(df_exibir, width='stretch', height=400)

# ========== FOOTER ==========
st.divider()
st.markdown("---")
st.caption("🚀 Dados fornecidos pela NASA NeoWs API | Desenvolvido para TCC - Engenharia de Computação")