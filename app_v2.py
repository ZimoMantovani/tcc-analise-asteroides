"""
Apenas para teste
"""
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

# ========== CONFIGURAÇÃO DA PÁGINA ==========
st.set_page_config(
    page_title="NEO Monitor",
    page_icon="🌍",
    layout="wide"
)

# ========== FUNÇÃO PARA CONECTAR NO BANCO ==========
@st.cache_resource  # Cache: conecta 1 vez só, não toda hora
def get_database_connection():
    """
    Cria conexão com PostgreSQL
    """
    usuario = "postgres"
    senha = os.getenv('DB_PASSWORD', 'postgres123')
    host = "localhost"
    porta = "5432"
    banco = "tcc_asteroides"
    
    connection_string = f"postgresql://{usuario}:{quote_plus(senha)}@{host}:{porta}/{banco}?client_encoding=utf8"
    engine = create_engine(connection_string, connect_args={'client_encoding': 'utf8'})
    return engine

# ========== FUNÇÃO PARA CARREGAR DADOS ==========
@st.cache_data(ttl=300)  # Cache por 5 minutos (300 segundos)
def carregar_asteroides():
    """
    Carrega asteroides do banco
    """
    engine = get_database_connection()
    query = "SELECT * FROM asteroides ORDER BY data_aproximacao"
    df = pd.read_sql(query, engine)
    return df

# ========== INTERFACE ==========

st.title("🌍 Monitoramento de Asteroides - NEO Watch")
st.subheader("Sistema de Análise de Objetos Próximos à Terra")

# Botão para recarregar dados
if st.button("🔄 Atualizar Dados"):
    st.cache_data.clear()  # Limpa o cache
    st.rerun()  # Recarrega a página

st.divider()

# ========== CARREGAR DADOS ==========
try:
    with st.spinner("Carregando dados do banco..."):
        df = carregar_asteroides()
    
    st.success(f"✅ {len(df)} asteroides carregados!")
    
except Exception as e:
    st.error(f"❌ Erro ao conectar no banco: {e}")
    st.info("💡 Verifique se o PostgreSQL está rodando e se as credenciais estão corretas.")
    st.stop()  # Para a execução aqui

# ========== MÉTRICAS REAIS ==========
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total de Asteroides",
        value=len(df)
    )

with col2:
    perigosos = len(df[df['perigoso'] == True])
    st.metric(
        label="🚨 Potencialmente Perigosos",
        value=perigosos,
        delta=f"{perigosos/len(df)*100:.1f}%"
    )

with col3:
    maior_diametro = df['diametro_max_km'].max()
    st.metric(
        label="📏 Maior Asteroide",
        value=f"{maior_diametro:.3f} km"
    )

with col4:
    velocidade_media = df['velocidade_kmh'].mean()
    st.metric(
        label="🏃 Velocidade Média",
        value=f"{velocidade_media:,.0f} km/h"
    )

st.divider()

# ========== TABELA DE DADOS ==========
st.subheader("📋 Próximas Aproximações")

# Selecionar apenas colunas importantes para exibir
colunas_exibir = ['nome', 'data_aproximacao', 'diametro_max_km', 'distancia_km', 'velocidade_kmh', 'perigoso']

# Filtrar apenas as colunas que existem
colunas_disponiveis = [col for col in colunas_exibir if col in df.columns]

df_exibir = df[colunas_disponiveis].copy()

# Renomear colunas para ficar mais legível
df_exibir.columns = [
    'Nome',
    'Data de Aproximação',
    'Diâmetro (km)',
    'Distância (km)',
    'Velocidade (km/h)',
    'Perigoso'
]

# Formatar números
df_exibir['Diâmetro (km)'] = df_exibir['Diâmetro (km)'].apply(lambda x: f"{x:.3f}")
df_exibir['Distância (km)'] = df_exibir['Distância (km)'].apply(lambda x: f"{x:,.0f}")
df_exibir['Velocidade (km/h)'] = df_exibir['Velocidade (km/h)'].apply(lambda x: f"{x:,.0f}")

# Exibir tabela
st.dataframe(
    df_exibir,
    use_container_width=True,  # Usa toda a largura
    height=400  # Altura da tabela
)

st.divider()

# ========== PREVIEW DOS DADOS BRUTOS ==========
with st.expander("🔍 Ver Dados Brutos (Debug)"):
    st.write("Primeiras 5 linhas do DataFrame:")
    st.dataframe(df.head())
    
    st.write("Informações do DataFrame:")
    st.write(f"- Total de linhas: {len(df)}")
    st.write(f"- Total de colunas: {len(df.columns)}")
    st.write(f"- Colunas: {', '.join(df.columns)}")