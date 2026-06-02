import streamlit as st
from utils import carregar_asteroides, render_sidebar

st.set_page_config(page_title="Explorador - NEO Monitor", page_icon="🔍", layout="wide")
render_sidebar()

try:
    df = carregar_asteroides()
except Exception as e:
    st.error("Não foi possível carregar os dados.")
    st.stop()

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
             width='stretch', height=500)
