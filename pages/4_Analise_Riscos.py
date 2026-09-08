import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from src.utils import carregar_asteroides, render_sidebar
from src.analise_riscos import AnalisadorRiscos
from src.modelo_ml import prever_risco_ia
from src.gerador_insights import GeradorInsights
from src.estilo import aplicar_tema_espacial, renderizar_hero, hud_tag
from streamlit_extras.metric_cards import style_metric_cards
from PIL import Image

icone = Image.open("assets/logo.png")
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

st.set_page_config(page_title="Análise de Riscos - NEO Monitor", page_icon=icone, layout="wide")

# Aplica a identidade visual
aplicar_tema_espacial()
render_sidebar()

try:
    df = carregar_asteroides()
except Exception as e:
    st.error("Não foi possível carregar os dados. Use a barra lateral para atualizar.")
    st.stop()

# Capa padronizada
renderizar_hero(
    "Avaliação de Ameaças Estelares",
    "Análise de Risco, Simulação de Impacto e Previsões com Machine Learning"
)

# Gerar análise completa
with st.spinner("Sintetizando cálculos orbitais e análise de risco..."):
    df_riscos = AnalisadorRiscos.gerar_relatorio_completo(df.drop_duplicates(subset=['nome']))
    
    # Juntar dados Originais
    df_completo = df.merge(
        df_riscos[['nome', 'energia_megatons', 'raio_destruicao_km', 'indice_risco', 'nivel_indice', 'cor_indice', 'classificacao']],
        on='nome',
        how='left'
    )

# Layout espacial padrão para os gráficos
layout_espacial = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#E8E8E8',
    font_family='JetBrains Mono, monospace',
    xaxis=dict(gridcolor='rgba(0,240,255,0.08)'),
    yaxis=dict(gridcolor='rgba(0,240,255,0.08)'),
    margin=dict(t=40, b=20, l=20, r=20),
)

# Paleta de cores para os níveis de risco (HUD style)
cores_risco = ['#00F0FF', '#00FF9D', '#FFE600', '#FF8000', '#FF2A5F']
mapa_cores_risco = {
    'MUITO BAIXO': cores_risco[0],
    'BAIXO': cores_risco[1],
    'MÉDIO': cores_risco[2],
    'ALTO': cores_risco[3],
    'CRÍTICO': cores_risco[4]
}

# ========== MÉTRICAS GERAIS ==========
st.subheader("Panorama Tático de Riscos", divider="blue")

col1, col2, col3, col4 = st.columns(4)

with col1:
    risco_alto = len(df_completo[df_completo['indice_risco'] >= 60])
    st.metric("🔴 Ameaças de Alto Risco", risco_alto, delta=f"{risco_alto/len(df)*100:.1f}%")

with col2:
    energia_max = df_riscos['energia_megatons'].max()
    st.metric("💥 Maior Energia (MT)", f"{energia_max:,.2f}")

with col3:
    raio_max = df_riscos['raio_destruicao_km'].max()
    st.metric("📏 Maior Raio Destrutivo", f"{raio_max:,.1f} km")

with col4:
    indice_medio = df_riscos['indice_risco'].mean()
    st.metric("📈 Índice de Risco Médio", f"{indice_medio:.1f}/100")

# Aplica o estilo de vidro aos cards de métricas
style_metric_cards(
    background_color="rgba(20, 27, 46, 0.55)",
    border_left_color="#FF2A5F",
    border_color="rgba(255, 42, 95, 0.25)",
    box_shadow=True,
)

st.write("")

# ========== DISTRIBUIÇÃO DE RISCOS ==========
col1, col2 = st.columns(2)

with col1:
    # Gráfico de pizza - Níveis de risco
    contagem_niveis = df_riscos['nivel_indice'].value_counts().reset_index()
    contagem_niveis.columns = ['Nível', 'Quantidade']
    
    fig_pizza = px.pie(
        contagem_niveis,
        values='Quantidade',
        names='Nível',
        title="Distribuição por Nível de Risco",
        color='Nível',
        color_discrete_map=mapa_cores_risco,
        hole=0.4
    )
    fig_pizza.update_traces(marker=dict(line=dict(color='#0B101E', width=2)))
    fig_pizza.update_layout(**layout_espacial)
    st.plotly_chart(fig_pizza, width='stretch')

with col2:
    # Gráfico de barras - Categorias
    df_completo['Categoria_Impacto'] = df_completo['classificacao'].apply(lambda x: x['categoria'])
    categorias = df_completo['Categoria_Impacto'].value_counts().reset_index()
    categorias.columns = ['Categoria', 'Quantidade']
    
    fig_bar = px.bar(
        categorias,
        x='Categoria',
        y='Quantidade',
        title="Distribuição por Categoria de Impacto",
        color='Quantidade',
        color_continuous_scale=['#00F0FF', '#FF2A5F']
    )
    fig_bar.update_layout(**layout_espacial)
    st.plotly_chart(fig_bar, width='stretch')

st.divider()

# ========== DETALHES DE UM ASTEROIDE ==========
st.subheader("Simulador de Cenário de Impacto", divider="blue")

col_sel, _ = st.columns([1, 2])
with col_sel:
    asteroide_selecionado = st.selectbox(
        "Selecione um alvo para análise detalhada:",
        options=df_completo['nome'].tolist()
    )

if asteroide_selecionado:
    dados = df_completo[df_completo['nome'] == asteroide_selecionado].iloc[0]
    classificacao = dados['classificacao']
    
    nivel = dados['nivel_indice']
    cor_alvo = mapa_cores_risco.get(nivel, "#00F0FF")
    
    st.markdown(f"""
        <style>
        .st-key-dossie_impacto {{
            border: 1px solid {cor_alvo}80;
            border-radius: 0.75rem;
            padding: 1.5rem;
            background-color: rgba(20, 27, 46, 0.7);
            backdrop-filter: blur(10px);
            box-shadow: 0 0 20px {cor_alvo}20;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }}
        </style>
    """, unsafe_allow_html=True)

    with st.container(key="dossie_impacto"):
        col_cabecalho, col_tags = st.columns([2, 1])
        with col_cabecalho:
            st.markdown(f"## 🎯 ALVO: {dados['nome']}")
        with col_tags:
            tag_texto = "PERIGOSO (NASA)" if dados['perigoso'] else "SEGURO (NASA)"
            tag_cor = "#FF2A5F" if dados['perigoso'] else "#00F0FF"
            st.markdown(hud_tag(tag_texto, cor=tag_cor) + "&nbsp;" + hud_tag(nivel, cor=cor_alvo), unsafe_allow_html=True)
        
        st.write("")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"**Índice de Risco:**\n### {dados['indice_risco']:.1f}/100")
        c2.markdown(f"**Diâmetro Estimado:**\n### {dados['diametro_max_km']:.3f} km")
        c3.markdown(f"**Velocidade Relativa:**\n### {dados['velocidade_kmh']:,.0f} km/h")
        c4.markdown(f"**Distância de Interceptação:**\n### {dados['distancia_lunar']:.2f} LD")

        st.markdown("---")
        
        # Cenário de Impacto
        st.markdown(f"### 💥 Cenário de Impacto: {classificacao['categoria']}")
        
        col_impacto1, col_impacto2, col_impacto3 = st.columns(3)
        analise = AnalisadorRiscos.analisar_asteroide(dados)
        
        with col_impacto1:
            st.metric("Energia Liberada", f"{dados['energia_megatons']:,.2f} MT")
            st.caption(f"*{analise['comparacao_energia']}*")
        
        with col_impacto2:
            st.metric("Raio de Devastação", f"{dados['raio_destruicao_km']:.1f} km")
            area_km2 = np.pi * (dados['raio_destruicao_km'] ** 2)
            st.caption(f"*Área totalmente afetada: ~{area_km2:,.0f} km²*")
        
        with col_impacto3:
            st.metric("Nível de Severidade", classificacao['nivel_risco'])
            st.caption(f"*{classificacao['dano_potencial']}*")
            
        st.info(f"**Frequência estatística:** {classificacao['frequencia']} | **Exemplo Histórico:** {classificacao['exemplo_historico']}", icon="ℹ️")

    # --- SEPARAÇÃO VISUAL: MACHINE LEARNING vs. NLG ---
    st.write("")
    col_ml, col_nlg = st.columns([1, 1])

    with col_ml:
        st.subheader("🤖 Predição (Machine Learning)", divider="violet")
        with st.spinner("Computando inferência no modelo Random Forest..."):
            magnitude = dados.get('magnitude_absoluta')
            if magnitude is None or pd.isna(magnitude):
                magnitude = 20.0

            probabilidade_perigo = prever_risco_ia(
                diametro_max=dados['diametro_max_km'],
                velocidade=dados['velocidade_kmh'],
                distancia=dados['distancia_km'],
                magnitude_absoluta=magnitude
            )
            
            chance_pct = probabilidade_perigo * 100
            
            st.write("**Probabilidade do asteroide ser categorizado como Hazardous (Perigoso):**")
            # Barra de progresso visual simulando telemetria
            st.progress(probabilidade_perigo, text=f"{chance_pct:.1f}%")
            
            if chance_pct < 10:
                st.success("Veredito do Modelo: **RISCO QUASE NULO**. O objeto apresenta características consistentes com a vasta maioria dos asteroides inofensivos.")
            elif chance_pct < 50:
                st.warning("Veredito do Modelo: **ALERTA MODERADO**. O objeto possui anomalias na velocidade ou no tamanho que requerem monitoramento.")
            else:
                st.error("Veredito do Modelo: **ALTO RISCO DE IMPACTO**. Padrões orbitais e físicos coincidem criticamente com ameaças registradas no banco de dados!")

    with col_nlg:
        st.subheader("📝 Resumo Interpretativo (NLG)", divider="gray")
        with st.spinner("Gerando relatório..."):
            texto_educacional = GeradorInsights.gerar_resumo_nlg(
                nome=dados['nome'],
                id_neo=dados['id_neo'],
                diametro_km=dados['diametro_max_km'],
                velocidade_kmh=dados['velocidade_kmh'],
                distancia_lunar=dados['distancia_lunar']
            )
            st.info(texto_educacional, icon="💡")

st.divider()

# ========== GRÁFICO: RISCO vs TAMANHO ==========
st.subheader("Dispersão Analítica: Risco vs Tamanho", divider="blue")

fig_scatter = px.scatter(
    df_completo,
    x='diametro_max_km',
    y='indice_risco',
    color='nivel_indice',
    size='energia_megatons',
    hover_data=['nome', 'distancia_lunar', 'velocidade_kmh'],
    labels={
        'diametro_max_km': 'Diâmetro (km)',
        'indice_risco': 'Índice de Risco (0-100)',
        'nivel_indice': 'Classificação',
        'energia_megatons': 'Energia (MT)'
    },
    color_discrete_map=mapa_cores_risco
)
fig_scatter.update_traces(
    marker=dict(line=dict(width=1, color='rgba(255,255,255,0.4)')),
    opacity=0.85
)
fig_scatter.update_layout(**layout_espacial)
st.plotly_chart(fig_scatter, width='stretch')

st.write("")

# ========== TOP 10 MAIS PERIGOSOS & METODOLOGIA ==========
col_tabela, col_metodo = st.columns([2, 1])

with col_tabela:
    st.subheader("🚨 Top 10 Ameaças Detectadas")
    top_perigosos = df_completo.nlargest(10, 'indice_risco')[
        ['nome', 'indice_risco', 'nivel_indice', 'diametro_max_km', 'distancia_lunar']
    ].copy()

    top_perigosos['diametro_max_km'] = top_perigosos['diametro_max_km'].apply(lambda x: f"{x:.3f}")
    top_perigosos['distancia_lunar'] = top_perigosos['distancia_lunar'].apply(lambda x: f"{x:.2f}")
    top_perigosos.columns = ['Nome do Objeto', 'Índice (0-100)', 'Nível', 'Diâmetro (km)', 'Distância (LD)']

    st.dataframe(top_perigosos, width='stretch', hide_index=True)

with col_metodo:
    st.subheader("📖 Metodologia")
    with st.expander("COMO O RISCO É CALCULADO?", expanded=True):
        st.markdown("""
        **Índice de Risco Proprietário (0-100)**
        - **40% Tamanho:** Diâmetro do asteroide
        - **30% Distância:** Proximidade da Terra
        - **20% Velocidade:** Velocidade de aproximação
        - **10% Classificação NASA:** Status de perigo
        
        **Energia de Impacto (MT)**
        Fórmula: `E = 0.5 × m × v²`
        Assumindo densidade de 2.600 kg/m³ (rocha).
        
        **Raio de Destruição (km)**
        Fórmula empírica: `R ≈ 2.2 × E^0.33`
        """)