import streamlit as st
import plotly.express as px
from utils import carregar_asteroides, render_sidebar

# Configuração da página (deve ser a primeira chamada Streamlit)
st.set_page_config(page_title="Home - NEO Monitor", page_icon="🏠", layout="wide")

# Renderiza a barra lateral padrão
render_sidebar()

try:
    df = carregar_asteroides()
except Exception as e:
    st.error("Não foi possível carregar os dados. Use a barra lateral para atualizar.")
    st.stop()

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
    st.plotly_chart(fig_pizza, width='stretch')

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
st.dataframe(proximos, width='stretch', hide_index=True)
