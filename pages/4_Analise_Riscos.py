import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils import carregar_asteroides, render_sidebar
from analise_riscos import AnalisadorRiscos
from modelo_ia import prever_risco_ia
from curiosidades_ia import GeradorCuriosidades

st.set_page_config(page_title="Análise de Riscos - NEO Monitor", page_icon="⚠️", layout="wide")
render_sidebar()

try:
    df = carregar_asteroides()
except Exception as e:
    st.error("Não foi possível carregar os dados.")
    st.stop()

st.title("⚠️ Análise de Riscos dos Asteroides")

# Gerar análise completa
with st.spinner("Analisando riscos..."):
    df_riscos = AnalisadorRiscos.gerar_relatorio_completo(df.drop_duplicates(subset=['nome']))
    
    # Juntar dados Originais
    df_completo = df.merge(
        df_riscos[['nome', 'energia_megatons', 'raio_destruicao_km', 'indice_risco', 'nivel_indice', 'cor_indice', 'classificacao']],
        on='nome',
        how='left'
    )

# ========== MÉTRICAS GERAIS ==========
st.subheader("📊 Panorama Geral de Riscos")

col1, col2, col3, col4 = st.columns(4)

with col1:
    risco_alto = len(df_completo[df_completo['indice_risco'] >= 60])
    st.metric("🔴 Alto Risco", risco_alto, delta=f"{risco_alto/len(df)*100:.1f}%")

with col2:
    energia_max = df_riscos['energia_megatons'].max()
    st.metric("💥 Maior Energia", f"{energia_max:.2f} MT")

with col3:
    raio_max = df_riscos['raio_destruicao_km'].max()
    st.metric("📏 Maior Raio", f"{raio_max:.1f} km")

with col4:
    indice_medio = df_riscos['indice_risco'].mean()
    st.metric("📈 Índice Médio", f"{indice_medio:.1f}/100")

st.divider()

# ========== DISTRIBUIÇÃO DE RISCOS ==========
st.subheader("📊 Distribuição por Categoria de Risco")

col1, col2 = st.columns(2)

with col1:
    # Gráfico de pizza - Níveis de risco
    contagem_niveis = df_riscos['nivel_indice'].value_counts()
    fig_pizza = px.pie(
        values=contagem_niveis.values,
        names=contagem_niveis.index,
        title="Distribuição por Nível de Risco",
        color_discrete_sequence=['#00ff00', '#88ff00', '#ffff00', '#ff8800', '#ff0000']
    )
    st.plotly_chart(fig_pizza, width='stretch')

with col2:
    # Gráfico de barras - Categorias
    categorias = df_completo['classificacao'].apply(lambda x: x['categoria']).value_counts()
    fig_bar = px.bar(
        x=categorias.index,
        y=categorias.values,
        title="Distribuição por Categoria de Impacto",
        labels={'x': 'Categoria', 'y': 'Quantidade'},
        color=categorias.values,
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_bar, width='stretch')

st.divider()

# ========== ESCALA DE IMPACTOS ==========
st.subheader("📏 Escala de Severidade de Impactos")

# Criar tabela de categorias
categorias_info = []
for size in [0.010, 0.050, 0.300, 2.0, 10.0]:
    info = AnalisadorRiscos.classificar_por_tamanho(size)
    categorias_info.append({
        'Diâmetro': f"~{size*1000:.0f}m",
        'Categoria': info['categoria'],
        'Nível': info['nivel_risco'],
        'Dano': info['dano_potencial'],
        'Área Afetada': info['area_afetada'],
        'Frequência': info['frequencia'],
        'Exemplo': info['exemplo_historico']
    })

df_categorias = pd.DataFrame(categorias_info)
st.dataframe(df_categorias, width='stretch', hide_index=True)

st.divider()

# ========== TOP 10 MAIS PERIGOSOS ==========
st.subheader("🚨 Top 10 Asteroides Mais Perigosos")

top_perigosos = df_completo.nlargest(10, 'indice_risco')[
    ['nome', 'indice_risco', 'nivel_indice', 'diametro_max_km', 'energia_megatons', 'raio_destruicao_km', 'distancia_lunar']
].copy()

# Formatar valores
top_perigosos['diametro_max_km'] = top_perigosos['diametro_max_km'].apply(lambda x: f"{x:.3f}")
top_perigosos['energia_megatons'] = top_perigosos['energia_megatons'].apply(lambda x: f"{x:.2f}")
top_perigosos['raio_destruicao_km'] = top_perigosos['raio_destruicao_km'].apply(lambda x: f"{x:.1f}")
top_perigosos['distancia_lunar'] = top_perigosos['distancia_lunar'].apply(lambda x: f"{x:.2f}")

# Renomear colunas
top_perigosos.columns = ['Nome', 'Índice de Risco', 'Nível', 'Diâmetro (km)', 'Energia (MT)', 'Raio Dest. (km)', 'Distância (Luas)']

st.dataframe(
    top_perigosos,
    width='stretch',
    hide_index=True
)

st.divider()

# ========== DETALHES DE UM ASTEROIDE ==========
st.subheader("🔍 Análise Detalhada de Asteroide")

asteroide_selecionado = st.selectbox(
    "Selecione um asteroide:",
    options=df_completo['nome'].tolist()
)

if asteroide_selecionado:
    dados = df_completo[df_completo['nome'] == asteroide_selecionado].iloc[0]
    classificacao = dados['classificacao']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {dados['nome']}")
        st.markdown(f"**Índice de Risco:** {dados['indice_risco']:.1f}/100")
        st.markdown(f"**Nível:** {dados['nivel_indice']}")
        st.markdown(f"**Categoria:** {classificacao['categoria']}")
        st.markdown(f"**Perigoso (NASA):** {'🚨 SIM' if dados['perigoso'] else '✅ NÃO'}")
        
    with col2:
        st.markdown("### Características Físicas")
        st.markdown(f"**Diâmetro:** {dados['diametro_max_km']:.3f} km ({dados['diametro_max_km']*1000:.0f} metros)")
        st.markdown(f"**Velocidade:** {dados['velocidade_kmh']:,.0f} km/h")
        st.markdown(f"**Distância:** {dados['distancia_lunar']:.2f} distâncias lunares")
    
    st.divider()
    
    # Análise de impacto
    st.markdown("### 💥 Cenário de Impacto Hipotético")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Energia de Impacto", f"{dados['energia_megatons']:.2f} MT")
        
        # Comparação
        analise = AnalisadorRiscos.analisar_asteroide(dados)
        st.caption(analise['comparacao_energia'])
    
    with col2:
        st.metric("Raio de Destruição", f"{dados['raio_destruicao_km']:.1f} km")
        area_km2 = np.pi * (dados['raio_destruicao_km'] ** 2)
        st.caption(f"Área afetada: ~{area_km2:,.0f} km²")
    
    with col3:
        st.metric("Dano Potencial", classificacao['nivel_risco'])
        st.caption(classificacao['dano_potencial'])
    
    # Aviso importante
    st.warning(f"""
    ⚠️ **Importante:** Este é um cenário HIPOTÉTICO baseado em cálculos físicos. 
    A probabilidade real de impacto é **extremamente baixa** para a maioria dos asteroides monitorados.
    
    📏 **Distância atual:** {dados['distancia_lunar']:.2f} distâncias lunares 
    (~ {dados['distancia_km']:,.0f} km da Terra)
    """)
    
    # Frequência de eventos
    st.info(f"""
    📊 **Frequência estatística de eventos deste tipo:**  
    {classificacao['frequencia']}
    
    📖 **Exemplo histórico:** {classificacao['exemplo_historico']}
    """)
    
    st.divider()
    
    # --- MÓDULO EDUCACIONAL E INTELIGÊNCIA ARTIFICIAL (QP4) ---
    st.subheader("🧠 Insights da Inteligência Artificial (Módulo Educacional)")
    
    with st.spinner("A IA está analisando os dados..."):
        # 1. Previsão do Modelo de Machine Learning
        score_ia = prever_risco_ia(
            diametro_max=dados['diametro_max_km'],
            velocidade=dados['velocidade_kmh'],
            distancia=dados['distancia_km']
        )
        
        # 2. Geração do texto educacional dinâmico
        texto_educacional = GeradorCuriosidades.gerar_fatos_educacionais(
            nome=dados['nome'],
            diametro_km=dados['diametro_max_km'],
            velocidade_kmh=dados['velocidade_kmh'],
            distancia_lunar=dados['distancia_lunar'],
            score_ia=score_ia
        )
        
        st.markdown(texto_educacional)

st.divider()

# ========== GRÁFICO: RISCO vs TAMANHO ==========
st.subheader("📈 Relação: Índice de Risco vs Tamanho")

fig_scatter = px.scatter(
    df_completo,
    x='diametro_max_km',
    y='indice_risco',
    color='nivel_indice',
    size='energia_megatons',
    hover_data=['nome', 'distancia_lunar', 'velocidade_kmh'],
    title="Índice de Risco vs Diâmetro do Asteroide",
    labels={
        'diametro_max_km': 'Diâmetro (km)',
        'indice_risco': 'Índice de Risco (0-100)',
        'nivel_indice': 'Nível'
    },
    color_discrete_map={
        'MUITO BAIXO': '#00ff00',
        'BAIXO': '#88ff00',
        'MÉDIO': '#ffff00',
        'ALTO': '#ff8800',
        'CRÍTICO': '#ff0000'
    }
)
st.plotly_chart(fig_scatter, width='stretch')

st.divider()

# ========== METODOLOGIA ==========
with st.expander("📖 Metodologia de Cálculo"):
    st.markdown("""
    ### Como Calculamos o Risco
    
    #### 1. Índice de Risco Proprietário (0-100)
    Ponderação multifatorial:
    - **40% Tamanho:** Diâmetro do asteroide (normalizado até 1km)
    - **30% Distância:** Proximidade da Terra (quanto mais perto, maior o risco)
    - **20% Velocidade:** Velocidade de aproximação (normalizada até 100.000 km/h)
    - **10% Classificação NASA:** Se é potencialmente perigoso segundo a NASA
    
    #### 2. Energia de Impacto
    Fórmula: `E = 0.5 × m × v²`
    - Massa calculada assumindo densidade de 2.600 kg/m³ (rocha típica)
    - Velocidade de impacto real do asteroide
    - Resultado em megatons de TNT (1 MT = 4.184×10¹⁵ joules)
    
    #### 3. Raio de Destruição
    Fórmula empírica: `R ≈ 2.2 × E^0.33`
    - R: raio em km
    - E: energia em megatons
    
    #### 4. Categorias de Impacto
    Baseadas em estudos científicos e eventos históricos:
    - **< 25m:** Meteorito (queima na atmosfera)
    - **25-140m:** Impacto local
    - **140m-1km:** Impacto regional
    - **1-5km:** Impacto continental
    - **> 5km:** Evento de extinção
    
    **Fontes:**
    - NASA NEO Program
    - JPL Center for NEO Studies
    - Papers científicos sobre impactos históricos
    """)