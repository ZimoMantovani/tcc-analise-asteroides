import streamlit as st
from utils import carregar_asteroides, render_sidebar
from estilo import aplicar_tema_espacial, renderizar_hero, hud_tag
from streamlit_extras.stylable_container import stylable_container
import warnings
from PIL import Image

icone = Image.open("images/logo.png")

warnings.simplefilter(action='ignore', category=FutureWarning)

# Configuração da página
st.set_page_config(page_title="Explorador - NEO Monitor", page_icon=icone, layout="wide")

# Aplica o tema visual padronizado
aplicar_tema_espacial()
render_sidebar()

try:
    df = carregar_asteroides()
except Exception as e:
    st.error("Não foi possível carregar os dados. Use a barra lateral para atualizar.")
    st.stop()

# Capa da página
renderizar_hero(
    "Explorador de Asteroides",
    "Filtre, pesquise e analise o dossiê detalhado dos objetos"
)

st.divider()

# Painel de Filtros estilo HUD
st.subheader("Filtros de Varredura", divider="blue")
col1, col2, col3 = st.columns(3)

with col1:
    filtro_perigoso = st.selectbox("Classificação de Risco:", ["Todos", "Perigosos", "Seguros"])
with col2:
    tamanho_min = st.number_input("Diâmetro mínimo (km):", value=0.0, step=0.01)
with col3:
    velocidade_min = st.number_input("Velocidade mínima (km/h):", value=0.0, step=1000.0)

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

st.markdown(f"**{len(df_filtrado)} asteroides detectados nos parâmetros atuais.**")
st.write("")

if len(df_filtrado) > 0:
    st.subheader("Destaques da Varredura (Top 12 Maiores)", divider="blue")
    
    # Pega os 12 maiores do dataframe filtrado para exibir como cards
    df_cards = df_filtrado.nlargest(12, 'diametro_max_km')
    
    # Cria um grid de 3 colunas
    cols = st.columns(3)
    
    for idx, (index, row) in enumerate(df_cards.iterrows()):
        col_atual = cols[idx % 3]
        
        cor_borda = "rgba(255, 42, 95, 0.4)" if row['perigoso'] else "rgba(0, 240, 255, 0.3)"
        cor_sombra = "rgba(255, 42, 95, 0.1)" if row['perigoso'] else "rgba(0, 240, 255, 0.05)"
        tag_texto = "PERIGOSO" if row['perigoso'] else "SEGURO"
        tag_cor = "#FF2A5F" if row['perigoso'] else "#00F0FF"
        icone = "⚠️" if row['perigoso'] else "☄️"
        
        with col_atual:
            # Card customizado para cada asteroide
            with stylable_container(
                key=f"card_{idx}",
                css_styles=f"""
                    {{
                        border: 1px solid {cor_borda};
                        border-radius: 0.75rem;
                        padding: 1.2rem;
                        background-color: rgba(20, 27, 46, 0.55);
                        backdrop-filter: blur(6px);
                        box-shadow: 0 0 15px {cor_sombra};
                        margin-bottom: 1.5rem;
                    }}
                """
            ):
                st.markdown(f"#### {icone} {row['nome']}")
                st.markdown(hud_tag(tag_texto, cor=tag_cor), unsafe_allow_html=True)
                st.write("")
                st.markdown(f"**Diâmetro:** {row['diametro_max_km']:.3f} km")
                st.markdown(f"**Velocidade:** {row['velocidade_kmh']:,.0f} km/h")
                st.markdown(f"**Distância:** {row['distancia_lunar']:.2f} LD")
                st.markdown(f"**Aproximação:** {row['data_aproximacao']}")
    
    st.write("")
    
    # Expander com a tabela completa para análise detalhada de todos os dados
    with st.expander("📂 VER BASE DE DADOS COMPLETA (TABELA)"):
        st.dataframe(
            df_filtrado[['nome', 'data_aproximacao', 'diametro_max_km', 'velocidade_kmh', 'distancia_lunar', 'perigoso']], 
            use_container_width=True, 
            height=400,
            hide_index=True
        )
else:
    st.warning("Nenhum asteroide encontrado com os filtros selecionados. Tente reduzir o diâmetro ou a velocidade.")